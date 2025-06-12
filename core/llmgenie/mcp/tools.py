"""
MCP Tools Implementation

Modular tools architecture:
- HandoffTools: Context transfer validation
- ProjectTools: Project state management  
- AgentTools: Agent orchestration
"""

import json
from typing import Dict, Optional, List, Any
from datetime import datetime
from pathlib import Path

from fastmcp import FastMCP
from pydantic import BaseModel

# Import existing validators
from ..api.handoff_validator import HandoffValidator, HandoffPackage, ValidationResult
from ..task_router import TaskClassifier, ModelRouter, ModelChoice


class HandoffTools:
    """Tools for handoff validation and context transfer"""
    
    def __init__(self, mcp: FastMCP):
        self.validator = HandoffValidator()
        self.mcp = mcp
        self._register_tools()
    
    def _register_tools(self):
        """Register all handoff tools with MCP server"""
        self.mcp.add_tool(self.validate_handoff)
        self.mcp.add_tool(self.get_handoff_template)
    
    async def validate_handoff(self, package_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate handoff package completeness for context transfer between AI sessions
        
        Args:
            package_data: Handoff package with from_role, to_role, files, etc.
            
        Returns:
            Validation result with completeness score and recommendations
        """
        try:
            # Convert dict to HandoffPackage
            package = HandoffPackage(**package_data)
            result = self.validator.validate_package(package)
            
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
    
    async def get_handoff_template(self) -> Dict[str, Any]:
        """Get handoff package template with required files and validation criteria"""
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


class ProjectTools:
    """Tools for project state and workflow management"""
    
    def __init__(self, mcp: FastMCP):
        self.mcp = mcp
        self._register_tools()
    
    def _register_tools(self):
        """Register all project tools with MCP server"""
        self.mcp.add_tool(self.get_project_state)
        self.mcp.add_tool(self.get_rules_manifest)
        self.mcp.add_tool(self.get_workflow_modes)
        self.mcp.add_tool(self.health_check)
    
    async def get_project_state(self) -> Dict[str, Any]:
        """Get current project state"""
        try:
            # Try to load project_state.json
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
    
    async def get_rules_manifest(self) -> Dict[str, Any]:
        """Get rules manifest"""
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
    
    async def get_workflow_modes(self) -> Dict[str, Any]:
        """Get available workflow modes"""
        return {
            "status": "success",
            "modes": [
                "discuss", "meta", "code", "debug", "docs", "test"
            ],
            "description": "Available workflow modes for context switching"
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check endpoint"""
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "0.1.0",
            "mcp_server": "fastmcp",
            "components": ["handoff_validator", "task_router", "orchestration"]
        }


class AgentTools:
    """Tools for agent orchestration and task execution"""
    
    def __init__(self, mcp: FastMCP):
        self.classifier = TaskClassifier()
        self.router = ModelRouter(self.classifier)
        self.mcp = mcp
        self._register_tools()
    
    def _register_tools(self):
        """Register all agent tools with MCP server"""
        self.mcp.add_tool(self.execute_agent_task)
        self.mcp.add_tool(self.get_agent_status)
    
    async def execute_agent_task(self, agent_type: str, task: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Execute a task with specified agent - Enhanced with Ollama/Claude routing
        
        Args:
            agent_type: Type of agent (auto, smart, ollama, claude)
            task: Task description to execute
            context: Optional context data
            
        Returns:
            Agent execution result with routing decision and metrics
        """
        agent_id = f"{agent_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            # Route task intelligently if agent_type supports it
            if agent_type in ['auto', 'smart', 'ollama', 'claude']:
                
                # Map agent_type to model preference
                model_preference = ModelChoice.AUTO
                if agent_type == 'ollama':
                    model_preference = ModelChoice.OLLAMA_MISTRAL
                elif agent_type == 'claude':
                    model_preference = ModelChoice.CLAUDE_SONNET
                
                # Get routing decision
                routing_decision = await self.router.route_task(
                    query=task,
                    context=context,
                    model_preference=model_preference
                )
                
                # Execute with selected model
                execution_result = await self.router.execute_with_model(
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
                # Legacy agent execution for backward compatibility
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
    
    async def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """Get status of specific agent
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            Agent status information
        """
        # TODO: Implement actual agent status tracking
        return {
            "status": "success",
            "agent_id": agent_id,
            "agent_status": "running",
            "progress": "50%",
            "note": "Status tracking not yet implemented - placeholder data"
        } 