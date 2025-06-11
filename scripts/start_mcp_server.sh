#!/bin/bash
# MCP Server startup script for Cursor
# Ensures proper environment activation

set -e  # Exit on any error

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🚀 Starting MCP Server for Cursor..."
echo "📁 Project root: $PROJECT_ROOT"

# Check if venv exists
if [ ! -d "$PROJECT_ROOT/venv" ]; then
    echo "❌ Error: Virtual environment not found at $PROJECT_ROOT/venv"
    echo "💡 Please run: python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source "$PROJECT_ROOT/venv/bin/activate"

# Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$PROJECT_ROOT/src"
echo "📚 PYTHONPATH set to include: $PROJECT_ROOT/src"

# Change to project directory
cd "$PROJECT_ROOT"

# Verify module availability
echo "🔍 Checking RAG module availability..."
if ! python -c "import rag_context.interfaces.mcp_server" 2>/dev/null; then
    echo "❌ Error: RAG module not accessible"
    echo "💡 Please check your installation and PYTHONPATH"
    exit 1
fi

echo "✅ Environment ready!"
echo "🎯 Starting MCP Server..."
echo "📡 Cursor should see 5 RAG tools once connected"
echo ""

# Start the server
python -m rag_context.interfaces.mcp_server 