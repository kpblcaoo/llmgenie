"""
RAG Context Interfaces - универсальные интерфейсы для доступа к RAG системе

Поддерживаемые интерфейсы:
- MCP: для Cursor, VSCode, Claude Desktop
- HTTP API: для веб-приложений, сервисов
- CLI: для командной строки и скриптов
- WebSocket: для real-time приложений
- Python Library: для прямого использования
"""

from .mcp_server import MCPServer
from .http_api import HTTPAPIServer  
from .cli_tool import CLITool
from .websocket_server import WebSocketServer

__all__ = ["MCPServer", "HTTPAPIServer", "CLITool", "WebSocketServer"] 