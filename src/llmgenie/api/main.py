"""
FastAPI main application for llmgenie
Provides REST API for multi-agent orchestration and workflow management
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import json
import os
from datetime import datetime

# Initialize FastAPI app
app = FastAPI(
    title="llmgenie API",
    description="Multi-agent orchestration and workflow management API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str

class ProjectStateResponse(BaseModel):
    project: str
    components: Dict
    status: str

class AgentRequest(BaseModel):
    agent_type: str
    task: str
    context: Optional[Dict] = None

class AgentResponse(BaseModel):
    agent_id: str
    status: str
    result: Optional[Dict] = None
    error: Optional[str] = None

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="0.1.0"
    )

# Project state endpoint
@app.get("/project/state", response_model=ProjectStateResponse)
async def get_project_state():
    """Get current project state"""
    try:
        # Load project_state.json
        with open("project_state.json", "r", encoding="utf-8") as f:
            state = json.load(f)
        
        return ProjectStateResponse(
            project=state.get("overview", {}).get("project", "llmgenie"),
            components=state.get("details", {}),
            status="active"
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Project state file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading project state: {str(e)}")

# Agent orchestration endpoints
@app.post("/agents/execute", response_model=AgentResponse)
async def execute_agent_task(request: AgentRequest):
    """Execute a task with specified agent"""
    # TODO: Implement actual agent orchestration
    # For now, return a mock response
    
    agent_id = f"{request.agent_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    return AgentResponse(
        agent_id=agent_id,
        status="completed",
        result={
            "message": f"Task '{request.task}' executed by {request.agent_type}",
            "context": request.context
        }
    )

@app.get("/agents/status/{agent_id}")
async def get_agent_status(agent_id: str):
    """Get status of specific agent"""
    # TODO: Implement actual agent status tracking
    return {
        "agent_id": agent_id,
        "status": "running",
        "progress": "50%"
    }

# Rules and workflow endpoints
@app.get("/rules/manifest")
async def get_rules_manifest():
    """Get rules manifest"""
    try:
        with open("rules_manifest.json", "r", encoding="utf-8") as f:
            manifest = json.load(f)
        return manifest
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Rules manifest not found")

@app.get("/workflow/modes")
async def get_workflow_modes():
    """Get available workflow modes"""
    return {
        "modes": [
            "discuss", "meta", "code", "debug", "docs", "test"
        ],
        "description": "Available workflow modes for context switching"
    }

# MCP integration placeholder
@app.post("/mcp/tools/execute")
async def execute_mcp_tool(tool_name: str, parameters: Dict):
    """Execute MCP tool (placeholder)"""
    # TODO: Implement actual MCP integration
    return {
        "tool": tool_name,
        "status": "not_implemented",
        "message": "MCP integration coming in Phase 2"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 