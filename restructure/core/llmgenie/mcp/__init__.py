"""
FastMCP Server Implementation

Epic 5 Completion: Modular MCP architecture using FastMCP
- Better initialization handling
- Cleaner tool separation
- Stable SSE transport
"""

# from .server import create_mcp_server  # Удалено, так как функции больше нет
from .tools import HandoffTools, ProjectTools, AgentTools

__all__ = [
    "HandoffTools", 
    "ProjectTools",
    "AgentTools"
] 