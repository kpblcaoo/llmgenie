"""
Sequential execution strategy

Epic 5 Phase 3.1: Sequential handoffs execution
Single responsibility: Execute tasks in sequence with context handoffs
"""

from typing import Dict, List, Any
from datetime import datetime

from ..core import OrchestrationTask, OrchestrationResult
from ...task_router import ModelRouter, ModelChoice


class SequentialExecutor:
    """
    Sequential handoffs execution strategy
    
    Epic 5 example: design → implementation → review
    Benefit: Context preservation, logical workflow
    """
    
    def __init__(self, agent_routers: Dict[str, ModelRouter]):
        """Initialize with available ModelRouter instances"""
        self.agent_routers = agent_routers
        
    async def execute(self, task: OrchestrationTask) -> OrchestrationResult:
        """
        Execute task using sequential strategy
        
        Executes subtasks in order, passing context between steps
        """
        start_time = datetime.now()
        
        # Get or decompose subtasks for sequential execution
        subtasks = task.subtasks or await self._decompose_sequential_task(task.query)
        
        results = {}
        context = task.context.copy() if task.context else {}
        router_names = list(self.agent_routers.keys())
        agents_used = []
        completed_steps = 0
        
        # Execute tasks sequentially, passing context forward
        for i, subtask in enumerate(subtasks):
            step_name = f"step_{i+1}"
            router_name = router_names[i % len(router_names)]
            
            try:
                # Execute step with accumulated context
                step_result = await self._execute_step(
                    router_name, subtask, context, step_name
                )
                
                results[step_name] = step_result
                agents_used.append(router_name)
                completed_steps += 1
                
                # Add result to context for next step (handoff)
                if step_result.get("status") == "completed":
                    context[f"previous_{step_name}"] = step_result.get("result", {})
                    context[f"handoff_from_{step_name}"] = {
                        "summary": self._extract_summary(step_result),
                        "key_outputs": self._extract_key_outputs(step_result)
                    }
                else:
                    # Break sequential chain on failure (option: continue with error context)
                    break
                    
            except Exception as e:
                results[step_name] = {
                    "status": "failed",
                    "subtask": subtask,
                    "router": router_name,
                    "error": str(e)
                }
                # Break sequential chain on exception
                break
        
        # Calculate metrics
        execution_time = (datetime.now() - start_time).total_seconds()
        coordination_efficiency = completed_steps / len(subtasks) if subtasks else 0.0
        
        # Determine overall status
        if completed_steps == len(subtasks):
            status = "completed"
        elif completed_steps > 0:
            status = "partial"
        else:
            status = "failed"
            
        return OrchestrationResult(
            task_id=task.task_id,
            status=status,
            results=results,
            execution_time=execution_time,
            coordination_efficiency=coordination_efficiency,
            agents_used=agents_used,
            metadata={
                "sequential_steps": len(subtasks),
                "completed_steps": completed_steps,
                "context_handoffs": completed_steps - 1 if completed_steps > 1 else 0
            }
        )
    
    async def _execute_step(self, router_name: str, subtask: str, context: Dict, step_name: str) -> Dict[str, Any]:
        """Execute single sequential step with context"""
        try:
            router = self.agent_routers[router_name]
            
            # Enhance subtask with context information for better handoff
            enhanced_query = self._enhance_query_with_context(subtask, context, step_name)
            
            # Route task using existing TaskRouter logic
            routing_decision = await router.route_task(
                query=enhanced_query,
                context=context,
                model_preference=ModelChoice.AUTO
            )
            
            # Execute with selected model
            execution_result = await router.execute_with_model(
                query=enhanced_query,
                model_choice=routing_decision.selected_model,
                context=context
            )
            
            return {
                "status": "completed",
                "subtask": subtask,
                "enhanced_query": enhanced_query,
                "router": router_name,
                "result": execution_result,
                "routing_decision": {
                    "selected_model": routing_decision.selected_model.value,
                    "reasoning": routing_decision.reasoning,
                    "confidence_score": routing_decision.confidence_score
                },
                "context_used": list(context.keys())
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "subtask": subtask,
                "router": router_name,
                "error": str(e)
            }
    
    def _enhance_query_with_context(self, subtask: str, context: Dict, step_name: str) -> str:
        """Enhance query with context from previous steps for better handoff"""
        if not context or step_name == "step_1":
            return subtask
            
        # Find previous step results for context enhancement
        previous_outputs = []
        for key, value in context.items():
            if key.startswith("handoff_from_"):
                summary = value.get("summary", "")
                if summary:
                    previous_outputs.append(f"Previous: {summary}")
        
        if previous_outputs:
            context_prefix = " | ".join(previous_outputs[:2])  # Limit context size
            return f"{subtask}\n\nContext from previous steps: {context_prefix}"
        
        return subtask
    
    def _extract_summary(self, step_result: Dict[str, Any]) -> str:
        """Extract summary from step result for context handoff"""
        result_data = step_result.get("result", {})
        
        if isinstance(result_data, dict):
            # Look for result text in common keys
            for key in ["result", "message", "content", "output"]:
                if key in result_data:
                    content = str(result_data[key])
                    # Return first 200 chars as summary
                    return content[:200] + "..." if len(content) > 200 else content
        
        # Fallback to string representation
        result_str = str(result_data)
        return result_str[:200] + "..." if len(result_str) > 200 else result_str
    
    def _extract_key_outputs(self, step_result: Dict[str, Any]) -> List[str]:
        """Extract key outputs for next step context"""
        key_outputs = []
        result_data = step_result.get("result", {})
        
        if isinstance(result_data, dict):
            # Extract specific information that might be useful for next steps
            for key in ["model", "execution_time", "routing_reasoning"]:
                if key in result_data:
                    key_outputs.append(f"{key}: {result_data[key]}")
        
        return key_outputs
    
    async def _decompose_sequential_task(self, query: str) -> List[str]:
        """
        Decompose task into sequential steps
        
        Epic 5 pattern: design → implementation → review
        """
        query_lower = query.lower()
        
        # Code development workflow
        if any(word in query_lower for word in ["develop", "create", "build", "implement"]):
            return [
                f"Design and plan approach for: {query}",
                f"Implement solution for: {query}",
                f"Review and validate implementation: {query}"
            ]
        
        # Analysis workflow
        elif any(word in query_lower for word in ["analyze", "investigate", "research"]):
            return [
                f"Initial investigation: {query}",
                f"Detailed analysis: {query}",
                f"Summary and recommendations: {query}"
            ]
        
        # Problem solving workflow
        elif any(word in query_lower for word in ["solve", "fix", "debug", "troubleshoot"]):
            return [
                f"Identify problem: {query}",
                f"Develop solution: {query}",
                f"Test and verify solution: {query}"
            ]
        
        # General sequential workflow
        else:
            return [
                f"Planning phase: {query}",
                f"Execution phase: {query}",
                f"Validation phase: {query}"
            ] 