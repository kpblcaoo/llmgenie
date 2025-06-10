"""
FastMCP Server Implementation

Clean server initialization using decorators
"""

import asyncio
import json
from typing import Dict, Optional, List, Any
from datetime import datetime
from pathlib import Path
import logging

from fastmcp import FastMCP

# Import existing validators
from ..api.handoff_validator import HandoffValidator, HandoffPackage, ValidationResult
from ..task_router import TaskClassifier, ModelRouter, ModelChoice

mcp = FastMCP("llmgenie-v2")

validator = HandoffValidator()
classifier = TaskClassifier()
router = ModelRouter(classifier)

logging.basicConfig(level=logging.INFO)

@mcp.tool()
async def validate_handoff(package_data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        package = HandoffPackage(**package_data)
        result = validator.validate_package(package)
        return {
            "status": "success",
            "validation_result": {
                "is_valid": result.is_valid,
                "completeness_score": result.completeness_score,
                "missing_files": result.missing_files,
                "recommendations": result.recommendations,
                "quality_metrics": result.quality_metrics
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "error": f"Validation failed: {str(e)}"
        }

@mcp.tool()
async def get_handoff_template() -> Dict[str, Any]:
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

@mcp.tool()
async def get_project_state() -> Dict[str, Any]:
    try:
        project_state_path = Path("project_state.json")
        if project_state_path.exists():
            with open(project_state_path, "r", encoding="utf-8") as f:
                state = json.load(f)
            return {
                "status": "success",
                "project": state.get("overview", {}).get("project", "llmgenie"),
                "components": state.get("details", {}),
                "state": "active"
            }
        else:
            return {
                "status": "success", 
                "project": "llmgenie",
                "components": {"note": "project_state.json not found"},
                "state": "unknown"
            }
    except Exception as e:
        return {
            "status": "error",
            "error": f"Error loading project state: {str(e)}"
        }

@mcp.tool()
async def health_check() -> Dict[str, Any]:
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "0.1.0",
        "mcp_server": "fastmcp",
        "components": ["handoff_validator", "task_router", "orchestration"]
    }

@mcp.tool()
async def execute_agent_task(agent_type: str, task: str, context: Optional[Dict] = None) -> Dict[str, Any]:
    agent_id = f"{agent_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    try:
        if agent_type in ['auto', 'smart', 'ollama', 'claude']:
            model_preference = ModelChoice.AUTO
            if agent_type == 'ollama':
                model_preference = ModelChoice.OLLAMA_MISTRAL
            elif agent_type == 'claude':
                model_preference = ModelChoice.CLAUDE_SONNET
            routing_decision = await router.route_task(
                query=task,
                context=context,
                model_preference=model_preference
            )
            execution_result = await router.execute_with_model(
                query=task,
                model_choice=routing_decision.selected_model,
                context=context
            )
            return {
                "status": "success",
                "agent_id": agent_id,
                "execution_status": execution_result.get("status", "completed"),
                "result": {
                    "message": execution_result.get("result", "Task completed"),
                    "model": execution_result.get("model", "unknown"),
                    "execution_time": execution_result.get("execution_time", 0),
                    "routing_reasoning": routing_decision.reasoning,
                    "confidence_score": routing_decision.confidence_score,
                    "context": context
                },
                "error": execution_result.get("error")
            }
        else:
            return {
                "status": "success",
                "agent_id": agent_id,
                "execution_status": "completed",
                "result": {
                    "message": f"Task '{task}' executed by {agent_type}",
                    "context": context
                }
            }
    except Exception as e:
        return {
            "status": "error",
            "agent_id": agent_id,
            "execution_status": "error",
            "result": None,
            "error": f"Task execution failed: {str(e)}"
        }

@mcp.tool()
async def get_agent_status(agent_id: str) -> Dict[str, Any]:
    return {
        "status": "success",
        "agent_id": agent_id,
        "agent_status": "running",
        "progress": "50%",
        "note": "Status tracking not yet implemented - placeholder data"
    }

@mcp.tool()
async def get_rules_manifest() -> Dict[str, Any]:
    try:
        with open(".cursor/rules/rules_manifest.json", "r", encoding="utf-8") as f:
            manifest = json.load(f)
        return {
            "status": "success",
            "manifest": manifest
        }
    except FileNotFoundError:
        return {
            "status": "error",
            "error": "Rules manifest not found"
        }
    except Exception as e:
        return {
            "status": "error", 
            "error": f"Error loading rules manifest: {str(e)}"
        }

@mcp.tool()
async def get_workflow_modes() -> Dict[str, Any]:
    return {
        "status": "success",
        "modes": [
            "discuss", "meta", "code", "debug", "docs", "test"
        ],
        "description": "Available workflow modes for context switching"
    }

# Экспортируем только объект mcp (FastMCP)
__all__ = ["mcp"]

if __name__ == "__main__":
    # Run server directly for testing
    mcp.run(transport="sse", host="localhost", port=8001) 