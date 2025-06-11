"""
MCP Server для интеграции с Cursor, VSCode, Claude Desktop
Объединяет RAG (5 инструментов) + Struct Tools (6 инструментов)
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

# Импорт struct_tools для архитектурного анализа
try:
    from ...struct_tools.structure_analyzer import StructureAnalyzer, StructureConfig
    STRUCT_TOOLS_AVAILABLE = True
except ImportError:
    # Пробуем абсолютный импорт как fallback
    try:
        from struct_tools.structure_analyzer import StructureAnalyzer, StructureConfig
        STRUCT_TOOLS_AVAILABLE = True
    except ImportError:
        STRUCT_TOOLS_AVAILABLE = False
        StructureAnalyzer = None
        StructureConfig = None


class MCPServer:
    """MCP Server для универсального доступа к RAG системе + Struct Tools"""
    
    def __init__(self, config: Optional[RAGConfig] = None):
        if not MCP_AVAILABLE:
            raise ImportError("MCP library required: pip install mcp")
        
        self.config = config or RAGConfig()
        self.enhancer = PromptEnhancer(self.config)
        
        # Инициализируем struct_tools если доступны
        if STRUCT_TOOLS_AVAILABLE:
            struct_config = StructureConfig(
                project_root=Path("."),
                struct_json_path=self.config.struct_json or Path("struct.json")
            )
            self.struct_analyzer = StructureAnalyzer(struct_config)
        else:
            self.struct_analyzer = None
        
        # Создаем MCP сервер
        self.server = Server("llmgenie-rag-struct")
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Настройка MCP handlers"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[types.Tool]:
            """Список доступных инструментов"""
            tools = [
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
                        "properties": {
                            "random_string": {
                                "type": "string",
                                "description": "Dummy parameter for no-parameter tools"
                            }
                        },
                        "required": ["random_string"]
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
            
            # Добавляем struct_tools если доступны
            if STRUCT_TOOLS_AVAILABLE and self.struct_analyzer:
                tools.extend([
                    types.Tool(
                        name="struct_generate",
                        description="Generate project structure analysis (struct.json + modular index)",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "target_dir": {
                                    "type": "string",
                                    "description": "Directory to analyze",
                                    "default": "src"
                                },
                                "force": {
                                    "type": "boolean",
                                    "description": "Force regeneration even if files are fresh",
                                    "default": False
                                }
                            }
                        }
                    ),
                    types.Tool(
                        name="struct_overview",
                        description="Get project statistics and overview",
                        inputSchema={
                            "type": "object",
                            "properties": {},
                            "required": []
                        }
                    ),
                    types.Tool(
                        name="struct_analyze_module",
                        description="Analyze specific module: dependencies, complexity, refactoring impact",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "module_path": {
                                    "type": "string",
                                    "description": "Path to module to analyze"
                                },
                                "include_dependencies": {
                                    "type": "boolean",
                                    "description": "Include dependency analysis",
                                    "default": True
                                },
                                "include_complexity": {
                                    "type": "boolean",
                                    "description": "Include complexity metrics",
                                    "default": True
                                },
                                "include_impact": {
                                    "type": "boolean",
                                    "description": "Include refactoring impact analysis",
                                    "default": True
                                }
                            },
                            "required": ["module_path"]
                        }
                    ),
                    types.Tool(
                        name="struct_search_functions",
                        description="Search for functions by pattern in their names",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "pattern": {
                                    "type": "string",
                                    "description": "Pattern to search for in function names"
                                }
                            },
                            "required": ["pattern"]
                        }
                    ),
                    types.Tool(
                        name="struct_find_callers",
                        description="Find functions that call a specific function",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "function_name": {
                                    "type": "string",
                                    "description": "Name of function to find callers for"
                                },
                                "module_filter": {
                                    "type": "string",
                                    "description": "Optional module filter",
                                    "default": None
                                }
                            },
                            "required": ["function_name"]
                        }
                    ),
                    types.Tool(
                        name="struct_generate_report",
                        description="Generate comprehensive architecture report",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "output_file": {
                                    "type": "string",
                                    "description": "Output file path",
                                    "default": "architecture_report.md"
                                }
                            }
                        }
                    )
                ])
            
            return tools
        
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
                    try:
                        if not self.config.has_struct_support:
                            return [types.TextContent(type="text", text=json.dumps({
                                "warning": "struct.json not available",
                                "suggestion": "Run 'lmstruct parse src/ -o struct.json' to generate project structure",
                                "status": "struct features disabled"
                            }, indent=2, ensure_ascii=False))]
                        
                        with open(self.config.struct_json, 'r', encoding='utf-8') as f:
                            struct_data = json.load(f)
                        
                        return [types.TextContent(type="text", text=json.dumps(struct_data, indent=2, ensure_ascii=False))]
                    except Exception as e:
                        return [types.TextContent(type="text", text=json.dumps({"error": str(e)}, indent=2, ensure_ascii=False))]
                
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
                
                # Обработчики struct_tools
                elif name.startswith("struct_") and self.struct_analyzer:
                    return await self._handle_struct_tool(name, arguments)
                
                else:
                    return [types.TextContent(type="text", text=f'Error: Unknown tool "{name}"')]
            
            except Exception as e:
                return [types.TextContent(type="text", text=f'Error: {str(e)}')]
    
    async def _handle_struct_tool(self, name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Обработка struct_tools инструментов"""
        try:
            if name == "struct_generate":
                target_dir = arguments.get("target_dir", "src")
                force = arguments.get("force", False)
                
                success = self.struct_analyzer.generate_structure(target_dir, force)
                
                result = {
                    "action": "generate_structure",
                    "success": success,
                    "target_dir": target_dir
                }
                
                if success:
                    # Загружаем и добавляем обзор
                    if self.struct_analyzer.load_structure():
                        overview = self.struct_analyzer.get_project_overview()
                        result.update({
                            "overview": overview,
                            "message": f"Generated structure with {overview['total_modules']} modules, "
                                      f"{overview['total_functions']} functions, {overview['total_classes']} classes"
                        })
                    else:
                        result["message"] = "Structure generated but failed to load for overview"
                else:
                    result["message"] = "Failed to generate structure"
                
                return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "struct_overview":
                if not self.struct_analyzer.load_structure():
                    return [types.TextContent(
                        type="text",
                        text=json.dumps({
                            "error": "Failed to load structure. Run struct_generate first."
                        }, indent=2)
                    )]
                
                overview = self.struct_analyzer.get_project_overview()
                overview["action"] = "project_overview"
                
                return [types.TextContent(type="text", text=json.dumps(overview, indent=2))]
            
            elif name == "struct_analyze_module":
                if not self.struct_analyzer.load_structure():
                    return [types.TextContent(
                        type="text",
                        text=json.dumps({
                            "error": "Failed to load structure. Run struct_generate first."
                        }, indent=2)
                    )]
                
                module_path = arguments["module_path"]
                result = {
                    "action": "analyze_module",
                    "module_path": module_path
                }
                
                # Анализ зависимостей
                if arguments.get("include_dependencies", True):
                    deps = self.struct_analyzer.analyze_module_dependencies(module_path)
                    result["dependencies"] = deps
                
                # Метрики сложности
                if arguments.get("include_complexity", True):
                    complexity = self.struct_analyzer.get_module_complexity_metrics(module_path)
                    result["complexity"] = complexity
                
                # Анализ влияния рефакторинга
                if arguments.get("include_impact", True):
                    impact = self.struct_analyzer.get_refactoring_impact(module_path)
                    result["refactoring_impact"] = impact
                
                return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "struct_search_functions":
                if not self.struct_analyzer.load_structure():
                    return [types.TextContent(
                        type="text",
                        text=json.dumps({
                            "error": "Failed to load structure. Run struct_generate first."
                        }, indent=2)
                    )]
                
                pattern = arguments["pattern"]
                results = self.struct_analyzer.search_functions_by_pattern(pattern)
                
                response = {
                    "action": "search_functions",
                    "pattern": pattern,
                    "found_count": len(results),
                    "results": results
                }
                
                return [types.TextContent(type="text", text=json.dumps(response, indent=2))]
            
            elif name == "struct_find_callers":
                if not self.struct_analyzer.load_structure():
                    return [types.TextContent(
                        type="text",
                        text=json.dumps({
                            "error": "Failed to load structure. Run struct_generate first."
                        }, indent=2)
                    )]
                
                function_name = arguments["function_name"]
                module_filter = arguments.get("module_filter")
                
                callers = self.struct_analyzer.find_function_callers(function_name, module_filter)
                
                response = {
                    "action": "find_callers",
                    "function_name": function_name,
                    "module_filter": module_filter,
                    "callers_count": len(callers),
                    "callers": callers
                }
                
                return [types.TextContent(type="text", text=json.dumps(response, indent=2))]
            
            elif name == "struct_generate_report":
                if not self.struct_analyzer.load_structure():
                    return [types.TextContent(
                        type="text",
                        text=json.dumps({
                            "error": "Failed to load structure. Run struct_generate first."
                        }, indent=2)
                    )]
                
                output_file = arguments.get("output_file", "architecture_report.md")
                success = self.struct_analyzer.generate_architecture_report(output_file)
                
                result = {
                    "action": "generate_report",
                    "success": success,
                    "output_file": output_file,
                    "message": f"Report generated: {output_file}" if success else "Failed to generate report"
                }
                
                return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
            
            else:
                return [types.TextContent(
                    type="text", 
                    text=json.dumps({"error": f"Unknown struct tool: {name}"}, indent=2)
                )]
                
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=json.dumps({"error": f"Struct tool {name} failed: {str(e)}"}, indent=2)
            )]
    
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