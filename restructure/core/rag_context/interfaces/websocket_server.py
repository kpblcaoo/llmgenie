"""
WebSocket Server для real-time интеграций
"""

import asyncio
import json
import websockets
from typing import Dict, Any, Optional, Set
from pathlib import Path

try:
    import websockets
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    print("Warning: websockets not installed. Install with: pip install websockets")
    WEBSOCKETS_AVAILABLE = False

from ..enhancer import PromptEnhancer
from ..config import RAGConfig


class WebSocketServer:
    """WebSocket Server для real-time доступа к RAG системе"""
    
    def __init__(self, config: Optional[RAGConfig] = None, port: int = 8002):
        if not WEBSOCKETS_AVAILABLE:
            raise ImportError("websockets library required: pip install websockets")
        
        self.config = config or RAGConfig()
        self.port = port
        self.enhancer = PromptEnhancer(self.config)
        
        # Активные соединения
        self.connections: Set[websockets.WebSocketServerProtocol] = set()
    
    async def register_connection(self, websocket):
        """Регистрация нового соединения"""
        self.connections.add(websocket)
        print(f"Client connected. Total connections: {len(self.connections)}")
    
    async def unregister_connection(self, websocket):
        """Удаление соединения"""
        self.connections.discard(websocket)
        print(f"Client disconnected. Total connections: {len(self.connections)}")
    
    async def broadcast_message(self, message: Dict[str, Any]):
        """Отправка сообщения всем подключенным клиентам"""
        if self.connections:
            message_str = json.dumps(message, ensure_ascii=False)
            await asyncio.gather(
                *[websocket.send(message_str) for websocket in self.connections],
                return_exceptions=True
            )
    
    async def handle_message(self, websocket, message_str: str) -> Dict[str, Any]:
        """Обработка входящего сообщения"""
        try:
            message = json.loads(message_str)
            
            if not isinstance(message, dict) or "action" not in message:
                return {
                    "error": "Invalid message format. Expected JSON with 'action' field.",
                    "message_id": message.get("id")
                }
            
            action = message["action"]
            params = message.get("params", {})
            message_id = message.get("id")
            
            # Инициализируем если нужно
            if not self.enhancer._initialized:
                await self.enhancer.initialize()
            
            # Обрабатываем действие
            if action == "enhance_prompt":
                query = params.get("query", "")
                max_context = params.get("max_context", 2000)
                
                if max_context != self.config.max_context_length:
                    self.config.max_context_length = max_context
                
                enhanced = await self.enhancer.enhance(query)
                
                return {
                    "action": "enhance_prompt_response",
                    "message_id": message_id,
                    "result": {
                        "enhanced_query": enhanced,
                        "original_query": query,
                        "added_context_length": len(enhanced) - len(query)
                    }
                }
            
            elif action == "search_rules":
                query = params.get("query", "")
                max_rules = params.get("max_rules", 3)
                
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
                
                return {
                    "action": "search_rules_response",
                    "message_id": message_id,
                    "result": {
                        "rules": rules,
                        "total_found": len(rules)
                    }
                }
            
            elif action == "get_project_structure":
                if self.config.struct_json.exists():
                    with open(self.config.struct_json, 'r', encoding='utf-8') as f:
                        struct_data = json.load(f)
                    return {
                        "action": "get_project_structure_response",
                        "message_id": message_id,
                        "result": struct_data
                    }
                else:
                    return {
                        "action": "get_project_structure_response",
                        "message_id": message_id,
                        "error": "struct.json not found"
                    }
            
            elif action == "get_stats":
                stats = self.enhancer.get_stats()
                return {
                    "action": "get_stats_response",
                    "message_id": message_id,
                    "result": stats
                }
            
            elif action == "refresh_index":
                success = await self.enhancer.refresh_index()
                return {
                    "action": "refresh_index_response",
                    "message_id": message_id,
                    "result": {
                        "status": "success" if success else "error",
                        "message": "Index refreshed successfully" if success else "Failed to refresh index"
                    }
                }
            
            elif action == "ping":
                return {
                    "action": "pong",
                    "message_id": message_id,
                    "timestamp": asyncio.get_event_loop().time()
                }
            
            else:
                return {
                    "error": f"Unknown action: {action}",
                    "message_id": message_id
                }
        
        except json.JSONDecodeError:
            return {
                "error": "Invalid JSON format"
            }
        except Exception as e:
            return {
                "error": f"Internal server error: {str(e)}",
                "message_id": message.get("id") if 'message' in locals() else None
            }
    
    async def handle_connection(self, websocket, path):
        """Обработка WebSocket соединения"""
        await self.register_connection(websocket)
        
        try:
            # Отправляем приветственное сообщение
            welcome = {
                "action": "welcome",
                "message": "Connected to LLMGenie RAG WebSocket Server",
                "server_info": {
                    "name": "llmgenie-rag",
                    "version": "1.0.0",
                    "capabilities": ["enhance_prompt", "search_rules", "get_project_structure", "get_stats", "refresh_index"]
                }
            }
            await websocket.send(json.dumps(welcome, ensure_ascii=False))
            
            # Обрабатываем сообщения
            async for message in websocket:
                response = await self.handle_message(websocket, message)
                if response:
                    await websocket.send(json.dumps(response, ensure_ascii=False))
        
        except websockets.exceptions.ConnectionClosed:
            pass
        except Exception as e:
            print(f"Error handling connection: {e}")
        finally:
            await self.unregister_connection(websocket)
    
    async def run(self, host: str = "localhost"):
        """Запуск WebSocket сервера"""
        print(f"Starting WebSocket Server on {host}:{self.port}...")
        
        # Инициализируем RAG систему
        await self.enhancer.initialize()
        
        # Запускаем сервер
        server = await websockets.serve(
            self.handle_connection,
            host,
            self.port
        )
        
        print(f"WebSocket RAG server running on ws://{host}:{self.port}")
        print("Available actions: enhance_prompt, search_rules, get_project_structure, get_stats, refresh_index, ping")
        
        # Ждем завершения
        await server.wait_closed()
    
    def get_client_example(self) -> str:
        """Возвращает пример клиентского кода"""
        return f"""
// JavaScript WebSocket Client Example
const ws = new WebSocket('ws://localhost:{self.port}');

ws.onopen = function() {{
    console.log('Connected to RAG server');
}};

ws.onmessage = function(event) {{
    const response = JSON.parse(event.data);
    console.log('Received:', response);
}};

// Enhance prompt
ws.send(JSON.stringify({{
    "id": "req-1",
    "action": "enhance_prompt",
    "params": {{
        "query": "Create new API endpoint",
        "max_context": 2000
    }}
}}));

// Search rules
ws.send(JSON.stringify({{
    "id": "req-2", 
    "action": "search_rules",
    "params": {{
        "query": "authentication",
        "max_rules": 3
    }}
}}));
"""


async def main():
    """Главная функция для запуска WebSocket сервера"""
    import sys
    
    # Парсим аргументы командной строки
    host = "localhost"
    port = 8002
    
    if "--host" in sys.argv:
        host_idx = sys.argv.index("--host") + 1
        if host_idx < len(sys.argv):
            host = sys.argv[host_idx]
    
    if "--port" in sys.argv:
        port_idx = sys.argv.index("--port") + 1
        if port_idx < len(sys.argv):
            port = int(sys.argv[port_idx])
    
    if "--example" in sys.argv:
        server = WebSocketServer(port=port)
        print("Client Example Code:")
        print("=" * 50)
        print(server.get_client_example())
        return
    
    # Создаем и запускаем сервер
    server = WebSocketServer(port=port)
    try:
        await server.run(host=host)
    except KeyboardInterrupt:
        print("\nShutting down WebSocket server...")


if __name__ == "__main__":
    asyncio.run(main()) 