#!/usr/bin/env python3
"""
FastMCP Server Test Script

Test new FastMCP implementation independently of the main API
"""

import sys
import asyncio
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from llmgenie.mcp.server import run_server


async def main():
    """Run FastMCP server on port 8001 for testing"""
    print("🧪 Testing FastMCP Server...")
    print("📍 Port 8001 (separate from main API on 8000)")
    print("🔄 Ctrl+C to stop")
    
    try:
        await run_server(port=8001, host="localhost")
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")


if __name__ == "__main__":
    asyncio.run(main()) 