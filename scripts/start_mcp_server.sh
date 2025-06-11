#!/bin/bash
# MCP Server startup script for Cursor
# Ensures proper environment activation

set -e  # Exit on any error

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🚀 Starting MCP Server for Cursor..."
echo "📁 Project root: $PROJECT_ROOT"

# Kill any existing MCP servers to avoid conflicts  
echo "🔄 Checking for existing MCP servers..."
if pgrep -f "rag_context.interfaces.mcp_server" > /dev/null; then
    echo "🛑 Killing existing MCP servers..."
    pkill -f "rag_context.interfaces.mcp_server" || true
    sleep 2
    echo "✅ Existing servers terminated"
else
    echo "✅ No existing servers found"
fi

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

# Check if struct.json exists, offer to create if missing
if [ ! -f "$PROJECT_ROOT/struct.json" ]; then
    echo "⚠️  struct.json not found"
    echo "🔧 Generating struct.json for current project..."
    
    # Try to generate struct.json using llmstruct if available
    if command -v lmstruct &> /dev/null; then
        echo "📊 Running: lmstruct parse --modular-index --include-ranges --include-hashes src/ -o struct.json"
        lmstruct parse --modular-index --include-ranges --include-hashes src/ -o struct.json || {
            echo "⚠️  Failed to generate struct.json with lmstruct, continuing without it..."
            echo "💡 MCP server will work with reduced functionality"
        }
    else
        echo "⚠️  lmstruct not available, continuing without struct.json..."
        echo "💡 MCP server will work with reduced functionality"
        echo "💡 To enable struct.json features, install lmstruct and rerun this script"
    fi
else
    echo "✅ struct.json found"
fi

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
echo "🔗 Server will be available for Cursor IDE integration"
echo ""

# Start the server
python -m rag_context.interfaces.mcp_server 