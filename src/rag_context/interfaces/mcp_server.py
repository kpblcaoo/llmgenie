"""
MCP Server для интеграции с Cursor, VSCode, Claude Desktop
Использует официальный MCP Python SDK
"""

import asyncio
import json
from typing import Dict, Any, Optional, List
from pathlib import Path

try:
    from mcp.server.models import InitializationOptions
    from mcp.server import NotificationOptions, Server
    import mcp.server.stdio
    import mcp.types as types
    MCP_AVAILABLE = True
except ImportError:
    print("Warning: MCP library not installed. Install with: pip install mcp")
    MCP_AVAILABLE = False

from ..enhancer import PromptEnhancer
from ..config import RAGConfig


class MCPServer:
    """MCP Server для универсального доступа к RAG системе"""
    
    def __init__(self, config: Optional[RAGConfig] = None):
        if not MCP_AVAILABLE:
            raise ImportError("MCP library required: pip install mcp")
        
        self.config = config or RAGConfig()
        self.enhancer = PromptEnhancer(self.config)
        
        # Создаем MCP сервер
        self.server = Server("llmgenie-rag")
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Настройка MCP handlers"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[types.Tool]:
            """Список доступных инструментов"""
            return [
                types.Tool(
                    name="enhance_prompt",
                    description="Улучшает промпт добавлением релевантного контекста из правил проекта",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Исходный запрос/задача"
                            },
                            "max_context": {
                                "type": "integer", 
                                "description": "Максимальная длина добавляемого контекста",
                                "default": 2000
                            }
                        },
                        "required": ["query"]
                    }
                ),
                types.Tool(
                    name="get_relevant_rules",
                    description="Возвращает релевантные правила для запроса",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Запрос для поиска правил"
                            },
                            "max_rules": {
                                "type": "integer",
                                "description": "Максимальное количество правил",
                                "default": 3
                            }
                        },
                        "required": ["query"]
                    }
                ),
                types.Tool(
                    name="get_project_structure",
                    description="Возвращает структуру проекта из struct.json",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                types.Tool(
                    name="get_system_stats",
                    description="Возвращает статистику RAG системы",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                types.Tool(
                    name="refresh_index",
                    description="Обновляет индекс документов RAG системы",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict) -> List[types.TextContent]:
            """Обработка вызовов инструментов"""
            try:
                if name == "enhance_prompt":
                    query = arguments["query"]
                    max_context = arguments.get("max_context", 2000)
                    
                    # Обновляем конфигурацию если нужно
                    if max_context != self.config.max_context_length:
                        self.config.max_context_length = max_context
                    
                    enhanced = await self.enhancer.enhance(query)
                    return [types.TextContent(type="text", text=enhanced)]
                
                elif name == "get_relevant_rules":
                    query = arguments["query"]
                    max_rules = arguments.get("max_rules", 3)
                    
                    # Инициализируем если нужно
                    if not self.enhancer._initialized:
                        await self.enhancer.initialize()
                    
                    # Получаем результаты поиска
                    results = self.enhancer.retriever.retrieve(query, max_rules)
                    
                    rules = []
                    for result in results:
                        rule = {
                            "title": result.document.metadata.get("title", "Untitled"),
                            "content": result.document.content[:500] + "..." if len(result.document.content) > 500 else result.document.content,
                            "source": result.document.source,
                            "score": round(result.score, 3),
                            "type": result.document.doc_type
                        }
                        rules.append(rule)
                    
                    response = {
                        "rules": rules,
                        "total_found": len(rules)
                    }
                    return [types.TextContent(type="text", text=json.dumps(response, indent=2, ensure_ascii=False))]
                
                elif name == "get_project_structure":
                    if self.config.struct_json.exists():
                        with open(self.config.struct_json, 'r', encoding='utf-8') as f:
                            struct_data = json.load(f)
                        return [types.TextContent(type="text", text=json.dumps(struct_data, indent=2, ensure_ascii=False))]
                    else:
                        return [types.TextContent(type="text", text='{"error": "struct.json not found"}')]
                
                elif name == "get_system_stats":
                    stats = self.enhancer.get_stats()
                    return [types.TextContent(type="text", text=json.dumps(stats, indent=2, ensure_ascii=False))]
                
                elif name == "refresh_index":
                    success = await self.enhancer.refresh_index()
                    result = {
                        "status": "success" if success else "error",
                        "message": "Index refreshed successfully" if success else "Failed to refresh index"
                    }
                    return [types.TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
                
                else:
                    return [types.TextContent(type="text", text=f'Error: Unknown tool "{name}"')]
            
            except Exception as e:
                return [types.TextContent(type="text", text=f'Error: {str(e)}')]
    
    async def run_stdio(self):
        """Запуск MCP сервера в stdio режиме (для Cursor)"""
        print("Starting MCP Server in stdio mode...")
        await self.enhancer.initialize()
        
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="llmgenie-rag",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )
    
    def get_cursor_config(self) -> Dict[str, Any]:
        """Генерирует конфигурацию для Cursor"""
        return {
            "mcpServers": {
                "llmgenie-rag": {
                    "command": "python",
                    "args": ["-m", "rag_context.interfaces.mcp_server"],
                    "env": {
                        "PYTHONPATH": "."
                    }
                }
            }
        }
    
    def get_vscode_config(self) -> Dict[str, Any]:
        """Генерирует конфигурацию для VSCode"""
        # VSCode может использовать тот же формат что и Cursor
        return self.get_cursor_config()
    
    def save_cursor_config(self, config_path: Optional[Path] = None):
        """Сохраняет конфигурацию для Cursor"""
        if config_path is None:
            config_path = Path.cwd() / ".cursor" / "mcp.json"
        
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.get_cursor_config(), f, indent=2)
        
        print(f"Cursor MCP config saved to: {config_path}")


async def main():
    """Главная функция для запуска MCP сервера"""
    import sys
    
    # Создаем и запускаем сервер
    server = MCPServer()
    
    # Сохраняем конфигурацию если нужно
    if "--save-config" in sys.argv:
        server.save_cursor_config()
        print("Configuration saved. Exiting.")
        return
    
    # Запускаем сервер
    await server.run_stdio()


if __name__ == "__main__":
    asyncio.run(main()) 