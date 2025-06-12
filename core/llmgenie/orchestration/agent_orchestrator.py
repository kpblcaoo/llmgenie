"""
Agent Orchestrator for Multi-Agent Task Coordination

Epic 5 Phase 3.1: Multi-Agent Orchestration implementation
Extends existing TaskRouter/ModelRouter with orchestration capabilities.

Design principle: Composition over inheritance - leverages existing components.
"""

from typing import Dict, List, Optional, Union, Any
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
import asyncio
import json

# Import existing Epic 5 components
from ..task_router import (
    TaskClassifier, 
    ModelRouter, 
    ModelChoice, 
    RoutingDecision,
    QualityValidator,
    QualityResult
)


class ExecutionMode(Enum):
    """Multi-Agent execution patterns from Epic 5 checklist"""
    PARALLEL = "parallel"        # Parallel task execution (documentation + code generation)
    SEQUENTIAL = "sequential"    # Sequential handoffs (design → implementation → review)
    COLLABORATIVE = "collaborative"  # Collaborative problem solving (multiple models, best result)


class AgentCoordination(Enum):
    """Agent coordination strategies"""
    INDEPENDENT = "independent"  # Agents work independently
    SYNCHRONIZED = "synchronized"  # Agents synchronize results
    HIERARCHICAL = "hierarchical"  # Lead agent coordinates others


@dataclass
class OrchestrationTask:
    """Task for multi-agent orchestration"""
    task_id: str
    query: str
    context: Optional[Dict] = None
    execution_mode: ExecutionMode = ExecutionMode.PARALLEL
    coordination: AgentCoordination = AgentCoordination.INDEPENDENT
    subtasks: Optional[List[str]] = None
    priority: int = 1
    timeout_seconds: int = 300


@dataclass 
class OrchestrationResult:
    """Result of multi-agent orchestration"""
    task_id: str
    status: str  # "completed", "partial", "failed"
    results: Dict[str, Any]  # Results from individual agents
    execution_time: float
    quality_score: Optional[float] = None
    coordination_efficiency: Optional[float] = None
    error: Optional[str] = None
    metadata: Optional[Dict] = None


class AgentOrchestrator:
    """
    Multi-Agent Orchestrator for Epic 5 Phase 3 Production Ready
    
    Coordinates multiple TaskRouter instances for complex multi-agent workflows.
    Implements patterns from Epic 5 checklist: parallel, sequential, collaborative execution.
    
    Design: Composition with existing TaskRouter/ModelRouter components
    """
    
    def __init__(self):
        """Initialize orchestrator with TaskRouter components"""
        # Leverage existing Epic 5 components
        self.classifier = TaskClassifier()
        self.quality_validator = QualityValidator()
        
        # Orchestration state
        self.active_tasks: Dict[str, OrchestrationTask] = {}
        self.agent_routers: Dict[str, ModelRouter] = {}
        self.coordination_log: List[Dict] = []
        
        # Initialize multiple ModelRouter instances for multi-agent coordination
        self._initialize_agent_routers()
    
    def _initialize_agent_routers(self):
        """Initialize specialized ModelRouter instances for different agent roles"""
        # Primary agents based on Epic 5 architecture
        self.agent_routers = {
            "primary": ModelRouter(self.classifier),       # Main task execution
            "secondary": ModelRouter(self.classifier),     # Backup/validation  
            "specialist": ModelRouter(self.classifier),    # Specialized tasks
        }
    
    async def coordinate_multi_agent_tasks(self, complex_task: OrchestrationTask) -> OrchestrationResult:
        """
        Main coordination method for multi-agent tasks
        
        Epic 5 Phase 3.1 requirement: coordinate_multi_agent_tasks
        """
        start_time = datetime.now()
        self.active_tasks[complex_task.task_id] = complex_task
        
        try:
            # Task decomposition based on execution mode
            if complex_task.execution_mode == ExecutionMode.PARALLEL:
                result = await self._execute_parallel(complex_task)
            elif complex_task.execution_mode == ExecutionMode.SEQUENTIAL:
                result = await self._execute_sequential(complex_task)
            elif complex_task.execution_mode == ExecutionMode.COLLABORATIVE:
                result = await self._execute_collaborative(complex_task)
            else:
                raise ValueError(f"Unknown execution mode: {complex_task.execution_mode}")
            
            # Calculate metrics
            execution_time = (datetime.now() - start_time).total_seconds()
            result.execution_time = execution_time
            
            # Quality validation using existing QualityValidator
            result.quality_score = await self._calculate_quality_score(result)
            
            # Log coordination event
            self._log_coordination_event(complex_task, result)
            
            return result
            
        except Exception as e:
            error_result = OrchestrationResult(
                task_id=complex_task.task_id,
                status="failed",
                results={},
                execution_time=(datetime.now() - start_time).total_seconds(),
                error=str(e)
            )
            return error_result
        
        finally:
            # Cleanup
            self.active_tasks.pop(complex_task.task_id, None)
    
    async def _execute_parallel(self, task: OrchestrationTask) -> OrchestrationResult:
        """
        Parallel task execution pattern
        
        Epic 5 example: documentation + code generation simultaneously
        """
        if not task.subtasks or len(task.subtasks) < 2:
            # Decompose task automatically if subtasks not provided
            subtasks = await self._decompose_task(task.query, "parallel")
        else:
            subtasks = task.subtasks
        
        # Execute subtasks in parallel using different agents
        async def execute_subtask(router_name: str, subtask: str) -> Dict[str, Any]:
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
                "subtask": subtask,
                "router": router_name,
                "result": execution_result,
                "routing_decision": routing_decision
            }
        
        # Parallel execution with different agents
        tasks_to_execute = []
        router_names = list(self.agent_routers.keys())
        
        for i, subtask in enumerate(subtasks[:len(router_names)]):
            router_name = router_names[i]
            tasks_to_execute.append(execute_subtask(router_name, subtask))
        
        # Wait for all parallel tasks to complete
        parallel_results = await asyncio.gather(*tasks_to_execute, return_exceptions=True)
        
        # Process results
        results = {}
        success_count = 0
        
        for i, result in enumerate(parallel_results):
            if isinstance(result, Exception):
                results[f"subtask_{i}"] = {"status": "failed", "error": str(result)}
            else:
                results[f"subtask_{i}"] = result
                success_count += 1
        
        # Determine overall status
        status = "completed" if success_count == len(parallel_results) else "partial"
        
        return OrchestrationResult(
            task_id=task.task_id,
            status=status,
            results=results,
            execution_time=0,  # Will be set by caller
            coordination_efficiency=success_count / len(parallel_results)
        )
    
    async def _execute_sequential(self, task: OrchestrationTask) -> OrchestrationResult:
        """
        Sequential handoffs pattern
        
        Epic 5 example: design → implementation → review
        """
        if not task.subtasks:
            # Decompose task for sequential execution
            subtasks = await self._decompose_task(task.query, "sequential")
        else:
            subtasks = task.subtasks
        
        results = {}
        context = task.context or {}
        
        # Execute tasks sequentially, passing context forward
        for i, subtask in enumerate(subtasks):
            router_name = list(self.agent_routers.keys())[i % len(self.agent_routers)]
            router = self.agent_routers[router_name]
            
            try:
                # Route task with accumulated context
                routing_decision = await router.route_task(
                    query=subtask,
                    context=context,
                    model_preference=ModelChoice.AUTO
                )
                
                # Execute with selected model
                execution_result = await router.execute_with_model(
                    query=subtask,
                    model_choice=routing_decision.selected_model,
                    context=context
                )
                
                # Store result and update context for next step
                step_result = {
                    "subtask": subtask,
                    "router": router_name,
                    "result": execution_result,
                    "routing_decision": routing_decision
                }
                
                results[f"step_{i+1}"] = step_result
                
                # Add result to context for next step (handoff)
                context[f"previous_step_{i+1}"] = execution_result.get("result", "")
                
            except Exception as e:
                results[f"step_{i+1}"] = {
                    "subtask": subtask,
                    "status": "failed", 
                    "error": str(e)
                }
                # Break sequential chain on failure
                break
        
        # Determine status based on completion
        completed_steps = len([r for r in results.values() if r.get("status") != "failed"])
        status = "completed" if completed_steps == len(subtasks) else "partial"
        
        return OrchestrationResult(
            task_id=task.task_id,
            status=status,
            results=results,
            execution_time=0,  # Will be set by caller
            coordination_efficiency=completed_steps / len(subtasks)
        )
    
    async def _execute_collaborative(self, task: OrchestrationTask) -> OrchestrationResult:
        """
        Collaborative problem solving pattern
        
        Epic 5 example: multiple models, best result selection
        """
        # Execute same task with multiple agents/models
        collaborative_results = {}
        
        for router_name, router in self.agent_routers.items():
            try:
                # Each agent attempts the full task
                routing_decision = await router.route_task(
                    query=task.query,
                    context=task.context,
                    model_preference=ModelChoice.AUTO
                )
                
                execution_result = await router.execute_with_model(
                    query=task.query,
                    model_choice=routing_decision.selected_model,
                    context=task.context
                )
                
                # Validate quality using existing QualityValidator
                quality_result = await self._validate_result_quality(execution_result, task)
                
                collaborative_results[router_name] = {
                    "result": execution_result,
                    "routing_decision": routing_decision,
                    "quality_score": quality_result.overall_score if quality_result else 0.0
                }
                
            except Exception as e:
                collaborative_results[router_name] = {
                    "status": "failed",
                    "error": str(e),
                    "quality_score": 0.0
                }
        
        # Select best result based on quality scores
        best_result = max(
            collaborative_results.items(),
            key=lambda x: x[1].get("quality_score", 0.0)
        )
        
        # Aggregate results with best result highlighted
        final_results = {
            "best_result": {
                "agent": best_result[0],
                "result": best_result[1]
            },
            "all_results": collaborative_results
        }
        
        return OrchestrationResult(
            task_id=task.task_id,
            status="completed",
            results=final_results,
            execution_time=0,  # Will be set by caller
            quality_score=best_result[1].get("quality_score", 0.0)
        )
    
    async def _decompose_task(self, query: str, mode: str) -> List[str]:
        """
        Automatic task decomposition using TaskClassifier
        
        AI-assisted task decomposition from Epic 5 checklist
        """
        # Use existing TaskClassifier to understand task type
        classification = self.classifier.classify_task(query, context={})
        
        # Simple decomposition based on task type and mode
        if mode == "parallel":
            if "code" in query.lower():
                return [
                    f"Generate code for: {query}",
                    f"Create documentation for: {query}",
                    f"Write tests for: {query}"
                ]
            else:
                return [
                    f"Analyze: {query}",
                    f"Plan solution for: {query}",
                    f"Validate approach for: {query}"
                ]
        
        elif mode == "sequential":
            return [
                f"Design approach for: {query}",
                f"Implement solution for: {query}",
                f"Review and validate: {query}"
            ]
        
        else:  # Default fallback
            return [query]
    
    async def _calculate_quality_score(self, result: OrchestrationResult) -> float:
        """Calculate quality score using existing QualityValidator"""
        try:
            # Extract main result content for quality analysis
            if "best_result" in result.results:
                # Collaborative mode
                main_result = result.results["best_result"]["result"]
            elif "step_1" in result.results:
                # Sequential mode - use final step
                step_keys = [k for k in result.results.keys() if k.startswith("step_")]
                final_step = max(step_keys)
                main_result = result.results[final_step]["result"]
            else:
                # Parallel mode - aggregate results
                all_results = [r.get("result", {}) for r in result.results.values()]
                main_result = {"aggregated_results": all_results}
            
            # Use existing QualityValidator
            quality_result = await self._validate_result_quality(main_result, None)
            return quality_result.overall_score if quality_result else 0.5
            
        except Exception:
            return 0.5  # Default score if quality calculation fails
    
    async def _validate_result_quality(self, execution_result: Dict, task: Optional[OrchestrationTask]) -> Optional[QualityResult]:
        """Validate result quality using existing Epic 5 QualityValidator"""
        try:
            result_content = execution_result.get("result", "")
            result_type = "text"  # Default, could be enhanced based on task type
            
            return self.quality_validator.validate_output(result_content, result_type)
        except Exception:
            return None
    
    def _log_coordination_event(self, task: OrchestrationTask, result: OrchestrationResult):
        """Log coordination event for analysis and improvement"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "task_id": task.task_id,
            "execution_mode": task.execution_mode.value,
            "coordination": task.coordination.value,
            "status": result.status,
            "execution_time": result.execution_time,
            "quality_score": result.quality_score,
            "coordination_efficiency": result.coordination_efficiency
        }
        self.coordination_log.append(log_entry)
        
        # Keep log size manageable
        if len(self.coordination_log) > 1000:
            self.coordination_log = self.coordination_log[-500:]
    
    def get_coordination_metrics(self) -> Dict[str, Any]:
        """Get coordination performance metrics"""
        if not self.coordination_log:
            return {"message": "No coordination events logged yet"}
        
        recent_events = self.coordination_log[-100:]  # Last 100 events
        
        return {
            "total_events": len(self.coordination_log),
            "recent_events": len(recent_events),
            "average_execution_time": sum(e.get("execution_time", 0) for e in recent_events) / len(recent_events),
            "average_quality_score": sum(e.get("quality_score", 0) for e in recent_events if e.get("quality_score")) / len([e for e in recent_events if e.get("quality_score")]),
            "success_rate": len([e for e in recent_events if e.get("status") == "completed"]) / len(recent_events),
            "mode_usage": {
                mode.value: len([e for e in recent_events if e.get("execution_mode") == mode.value])
                for mode in ExecutionMode
            }
        }
    
    # Additional methods for Epic 5 Phase 3.1 requirements
    
    async def manage_parallel_execution(self, task_list: List[OrchestrationTask]) -> List[OrchestrationResult]:
        """
        Manage multiple parallel executions
        
        Epic 5 Phase 3.1 requirement: manage_parallel_execution
        """
        parallel_tasks = [
            self.coordinate_multi_agent_tasks(task) 
            for task in task_list
        ]
        
        results = await asyncio.gather(*parallel_tasks, return_exceptions=True)
        
        # Process results and handle exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                error_result = OrchestrationResult(
                    task_id=task_list[i].task_id,
                    status="failed",
                    results={},
                    execution_time=0,
                    error=str(result)
                )
                processed_results.append(error_result)
            else:
                processed_results.append(result)
        
        return processed_results
    
    async def handle_inter_agent_communication(self, sender_agent: str, receiver_agent: str, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle communication between agents
        
        Epic 5 Phase 3.1 requirement: handle_inter_agent_communication
        """
        communication_log = {
            "timestamp": datetime.now().isoformat(),
            "sender": sender_agent,
            "receiver": receiver_agent,
            "message_type": message.get("type", "unknown"),
            "message": message
        }
        
        # Log communication for debugging and analysis
        self.coordination_log.append({
            "event_type": "inter_agent_communication",
            **communication_log
        })
        
        # Simple message passing implementation
        # In production, this would integrate with message queue system
        response = {
            "status": "message_delivered",
            "timestamp": datetime.now().isoformat(),
            "sender": sender_agent,
            "receiver": receiver_agent,
            "response": f"Message received by {receiver_agent}"
        }
        
        return response 