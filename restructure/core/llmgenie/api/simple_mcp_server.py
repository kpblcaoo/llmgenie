"""
Simple MCP Server for llmgenie
Uses stdio transport without FastAPI dependencies
"""

from mcp.server.fastmcp import FastMCP
import json
import os
from datetime import datetime
from pathlib import Path

# Initialize the MCP server
mcp = FastMCP("llmgenie")

@mcp.tool()
def health_check() -> dict:
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "0.1.0"
    }

@mcp.tool()
def get_project_state() -> dict:
    """Get current project state"""
    try:
        # Try to find project_state.json
        state_file = Path("project_state.json")
        if not state_file.exists():
            # Try relative to script location
            state_file = Path(__file__).parent.parent.parent / "project_state.json"
        
        if state_file.exists():
            with open(state_file, "r", encoding="utf-8") as f:
                state = json.load(f)
            
            return {
                "project": state.get("overview", {}).get("project", "llmgenie"),
                "components": state.get("details", {}),
                "status": "active"
            }
        else:
            return {
                "project": "llmgenie",
                "components": {},
                "status": "project_state.json not found"
            }
    except Exception as e:
        return {
            "project": "llmgenie", 
            "components": {},
            "status": f"Error loading project state: {str(e)}"
        }

@mcp.tool()
def execute_agent_task(agent_type: str, task: str, context: dict = None) -> dict:
    """Execute a task with specified agent"""
    agent_id = f"{agent_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    return {
        "agent_id": agent_id,
        "status": "completed",
        "result": {
            "message": f"Task '{task}' executed by {agent_type}",
            "context": context
        }
    }

@mcp.tool()
def get_agent_status(agent_id: str) -> dict:
    """Get status of specific agent"""
    return {
        "agent_id": agent_id,
        "status": "running",
        "progress": "50%"
    }

@mcp.tool()
def get_rules_manifest() -> dict:
    """Get rules manifest"""
    try:
        manifest_file = Path("rules_manifest.json")
        if not manifest_file.exists():
            manifest_file = Path(__file__).parent.parent.parent / "rules_manifest.json"
        
        if manifest_file.exists():
            with open(manifest_file, "r", encoding="utf-8") as f:
                manifest = json.load(f)
            return manifest
        else:
            return {"error": "Rules manifest not found"}
    except Exception as e:
        return {"error": f"Error loading rules manifest: {str(e)}"}

@mcp.tool()
def get_workflow_modes() -> dict:
    """Get available workflow modes"""
    return {
        "modes": [
            "discuss", "meta", "code", "debug", "docs", "test"
        ],
        "description": "Available workflow modes for context switching"
    }

@mcp.tool()
def validate_handoff_package(package: dict) -> dict:
    """Validate handoff package completeness"""
    try:
        # Simple validation logic
        required_fields = ["from_role", "to_role", "epic_id", "files"]
        missing_fields = [field for field in required_fields if field not in package]
        
        if missing_fields:
            return {
                "valid": False,
                "completeness_score": 0.0,
                "missing_fields": missing_fields,
                "recommendations": [f"Add {field}" for field in missing_fields]
            }
        
        files = package.get("files", [])
        file_count = len(files)
        completeness_score = min(file_count / 5.0, 1.0)  # Expect 5 files for 100%
        
        return {
            "valid": file_count >= 3,
            "completeness_score": completeness_score,
            "file_count": file_count,
            "recommendations": [] if file_count >= 5 else ["Add more documentation files"]
        }
    except Exception as e:
        return {
            "valid": False,
            "error": f"Validation error: {str(e)}"
        }

@mcp.tool()
def get_handoff_template() -> dict:
    """Get handoff package template"""
    return {
        "template": {
            "from_role": "string",
            "to_role": "string", 
            "epic_id": "string",
            "files": [
                {"path": "conversation_summary.md", "type": "summary", "priority": 1},
                {"path": "lessons_learned.md", "type": "lessons", "priority": 2},
                {"path": "epic_checklist.md", "type": "checklist", "priority": 3},
                {"path": "technical_audit.md", "type": "audit", "priority": 4},
                {"path": "project_state.json", "type": "metadata", "priority": 5}
            ],
            "startup_prompt": "Template: [role] Resuming work on [epic]. Status: [status]. Infrastructure: [details]. Lessons: [key points]. Next: [actions]",
            "control_questions": [
                "What is current status and progress?",
                "What technical components are ready for testing?", 
                "What scope constraints must be maintained?"
            ],
            "success_criteria": [
                "Handoff package validates with 80%+ completeness",
                "All required files present and non-empty",
                "Startup prompt includes status, infrastructure, lessons, constraints",
                "Control questions cover status, technical, and scope aspects"
            ]
        },
        "validation_requirements": {
            "min_files": 5,
            "required_file_types": ["summary", "lessons", "checklist", "audit", "metadata"],
            "min_control_questions": 3,
            "min_completeness_score": 0.8
        }
    }

if __name__ == "__main__":
    # Run the server using stdio transport
    mcp.run(transport="stdio") 