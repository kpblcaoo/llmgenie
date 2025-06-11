#!/bin/bash
# MCP Server startup script for Cursor (silent version)
# Ensures proper environment activation without verbose output

set -e  # Exit on any error

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Kill any existing MCP servers to avoid conflicts (silent)
pkill -f "rag_context.interfaces.mcp_server" 2>/dev/null || true
sleep 1

# Check if venv exists
if [ ! -d "$PROJECT_ROOT/venv" ]; then
    echo "Error: Virtual environment not found" >&2
    exit 1
fi

# Activate virtual environment
source "$PROJECT_ROOT/venv/bin/activate"

# Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$PROJECT_ROOT/src"

# Change to project directory
cd "$PROJECT_ROOT"

# Try to generate struct.json if missing (silent)
if [ ! -f "$PROJECT_ROOT/struct.json" ] && command -v lmstruct &> /dev/null; then
    lmstruct parse --modular-index --include-ranges --include-hashes src/ -o struct.json 2>/dev/null || true
fi

# Verify module availability
if ! python -c "import rag_context.interfaces.mcp_server" 2>/dev/null; then
    echo "Error: RAG module not accessible" >&2
    exit 1
fi

# Start the server (Cursor expects stdio MCP protocol)
exec python -m rag_context.interfaces.mcp_server 