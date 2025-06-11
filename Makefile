# RAG Interfaces
.PHONY: mcp-server http-api cli websocket

mcp-server:
	@echo "🚀 Starting MCP Server for Cursor..."
	@./scripts/start_mcp_server.sh

http-api:
	@echo "🌐 Starting HTTP API server..."
	@source venv/bin/activate && export PYTHONPATH="$(PYTHONPATH):$(PWD)/src" && python -m rag_context.interfaces.http_api

cli:
	@echo "💻 RAG CLI tool usage:"
	@source venv/bin/activate && export PYTHONPATH="$(PYTHONPATH):$(PWD)/src" && python -m rag_context.interfaces.cli_tool --help

websocket:
	@echo "⚡ Starting WebSocket server..."
	@source venv/bin/activate && export PYTHONPATH="$(PYTHONPATH):$(PWD)/src" && python -m rag_context.interfaces.websocket_server 