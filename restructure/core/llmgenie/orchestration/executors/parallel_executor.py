"""
Parallel execution strategy

Epic 5 Phase 3.1: Parallel task execution 
Single responsibility: Execute multiple subtasks simultaneously
"""

import asyncio
from typing import Dict, List, Any
from datetime import datetime

from ..core import OrchestrationTask, OrchestrationResult
from ...task_router import ModelRouter, ModelChoice


class ParallelExecutor:
    """
    Parallel task execution strategy
    
    Epic 5 example: documentation + code generation simultaneously
    Benefit: Maximum speed, resource utilization
    """
    
    def __init__(self, agent_routers: Dict[str, ModelRouter]):
        """Initialize with available ModelRouter instances"""
        self.agent_routers = agent_routers
    
    async def execute(self, task: OrchestrationTask) -> OrchestrationResult:
        """
        Execute task using parallel strategy
        
        Splits task into subtasks and executes them simultaneously
        """
        start_time = datetime.now()
        
        # Get or decompose subtasks
        subtasks = task.subtasks or await self._decompose_task(task.query)
        
        # Execute subtasks in parallel using different agents
        parallel_tasks = []
        router_names = list(self.agent_routers.keys())
        
        for i, subtask in enumerate(subtasks):
            # Cycle through available routers
            router_name = router_names[i % len(router_names)]
            parallel_tasks.append(self._execute_subtask(router_name, subtask, task))
        
        # Wait for all parallel tasks to complete
        parallel_results = await asyncio.gather(*parallel_tasks, return_exceptions=True)
        
        # Process results
        results = {}
        success_count = 0
        agents_used = []
        
        for i, result in enumerate(parallel_results):
            task_key = f"subtask_{i+1}"
            
            if isinstance(result, Exception):
                results[task_key] = {
                    "status": "failed", 
                    "error": str(result),
                    "subtask": subtasks[i] if i < len(subtasks) else "unknown"
                }
            else:
                results[task_key] = result
                if result.get("status") != "failed":
                    success_count += 1
                agents_used.append(result.get("router", "unknown"))
        
        # Calculate metrics
        execution_time = (datetime.now() - start_time).total_seconds()
        coordination_efficiency = success_count / len(parallel_results) if parallel_results else 0.0
        
        # Determine overall status
        if success_count == len(parallel_results):
            status = "completed"
        elif success_count > 0:
            status = "partial"
        else:
            status = "failed"
        
        return OrchestrationResult(
            task_id=task.task_id,
            status=status,
            results=results,
            execution_time=execution_time,
            coordination_efficiency=coordination_efficiency,
            agents_used=list(set(agents_used))  # Remove duplicates
        )
    
    async def _execute_subtask(self, router_name: str, subtask: str, task: OrchestrationTask) -> Dict[str, Any]:
        """Execute single subtask with specified router"""
        try:
            router = self.agent_routers[router_name]
            
            # Route subtask using existing TaskRouter logic
            routing_decision = await router.route_task(
                query=subtask,
                context=task.context,
                model_preference=ModelChoice.AUTO
            )
            
            # Execute with selected model
            execution_result = await router.execute_with_model(
                query=subtask,
                model_choice=routing_decision.selected_model,
                context=task.context
            )
            
            return {
                "status": "completed",
                "subtask": subtask,
                "router": router_name,
                "result": execution_result,
                "routing_decision": {
                    "selected_model": routing_decision.selected_model.value,
                    "reasoning": routing_decision.reasoning,
                    "confidence_score": routing_decision.confidence_score
                }
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "subtask": subtask,
                "router": router_name,
                "error": str(e)
            }
    
    async def _decompose_task(self, query: str) -> List[str]:
        """
        Decompose task into parallel subtasks
        
        Simple decomposition - can be enhanced with TaskClassifier
        """
        query_lower = query.lower()
        
        # Code-related decomposition
        if any(word in query_lower for word in ["code", "function", "class", "implement"]):
            return [
                f"Generate code for: {query}",
                f"Create documentation for: {query}",
                f"Write tests for: {query}"
            ]
        
        # Analysis-related decomposition  
        elif any(word in query_lower for word in ["analyze", "review", "evaluate"]):
            return [
                f"Technical analysis: {query}",
                f"Quality assessment: {query}",
                f"Recommendations for: {query}"
            ]
        
        # General decomposition
        else:
            return [
                f"Primary analysis: {query}",
                f"Secondary validation: {query}",
                f"Summary and conclusions: {query}"
            ] 