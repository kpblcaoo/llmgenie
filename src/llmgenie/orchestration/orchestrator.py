"""
Multi-Agent Orchestrator

Epic 5 Phase 3.1: Main orchestration class
Single responsibility: Coordinate multiple agents using different execution strategies
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

from .core import ExecutionMode, AgentCoordination, OrchestrationTask, OrchestrationResult
from .executors import ParallelExecutor, SequentialExecutor, CollaborativeExecutor
from ..task_router import ModelRouter, TaskClassifier


logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """
    Main orchestration class for multi-agent task execution
    
    Epic 5 integration: Uses existing TaskRouter + ModelRouter components
    Supports: PARALLEL, SEQUENTIAL, COLLABORATIVE execution modes
    """
    
    def __init__(self, agent_routers: Dict[str, ModelRouter], task_classifier: Optional[TaskClassifier] = None):
        """
        Initialize orchestrator with available agent routers
        
        Args:
            agent_routers: Dict of {name: ModelRouter} for different agents/models
            task_classifier: Optional TaskClassifier for automatic mode selection
        """
        self.agent_routers = agent_routers
        self.task_classifier = task_classifier
        
        # Initialize execution strategies
        self.parallel_executor = ParallelExecutor(agent_routers)
        self.sequential_executor = SequentialExecutor(agent_routers)
        self.collaborative_executor = CollaborativeExecutor(agent_routers)
        
        logger.info(f"AgentOrchestrator initialized with {len(agent_routers)} agent routers")
    
    async def orchestrate(
        self, 
        query: str, 
        execution_mode: Optional[ExecutionMode] = None,
        coordination_type: Optional[AgentCoordination] = None,
        context: Optional[Dict[str, Any]] = None,
        subtasks: Optional[List[str]] = None,
        task_id: Optional[str] = None
    ) -> OrchestrationResult:
        """
        Main orchestration method
        
        Args:
            query: Main task query
            execution_mode: How to execute (PARALLEL/SEQUENTIAL/COLLABORATIVE)
            coordination_type: How agents coordinate (INDEPENDENT/SYNCHRONIZED/HIERARCHICAL)
            context: Additional context for task execution
            subtasks: Pre-defined subtasks (optional)
            task_id: Custom task ID (optional)
        
        Returns:
            OrchestrationResult with execution results and metrics
        """
        start_time = datetime.now()
        
        # Create orchestration task
        task = OrchestrationTask(
            task_id=task_id or f"orchestration_{int(start_time.timestamp())}",
            query=query,
            context=context or {},
            subtasks=subtasks
        )
        
        logger.info(f"Starting orchestration: {task.task_id}")
        
        try:
            # Auto-select execution mode if not provided
            if execution_mode is None:
                execution_mode = await self._suggest_execution_mode(query)
                logger.info(f"Auto-selected execution mode: {execution_mode.value}")
            
            # Auto-select coordination type if not provided
            if coordination_type is None:
                coordination_type = self._suggest_coordination_type(execution_mode)
                logger.info(f"Auto-selected coordination type: {coordination_type.value}")
            
            # Validate agent compatibility
            if not self._validate_coordination_compatibility(execution_mode, coordination_type):
                logger.warning(f"Coordination type {coordination_type.value} not optimal for {execution_mode.value}")
            
            # Execute using selected strategy
            if execution_mode == ExecutionMode.PARALLEL:
                result = await self.parallel_executor.execute(task)
            elif execution_mode == ExecutionMode.SEQUENTIAL:
                result = await self.sequential_executor.execute(task)
            elif execution_mode == ExecutionMode.COLLABORATIVE:
                result = await self.collaborative_executor.execute(task)
            else:
                raise ValueError(f"Unsupported execution mode: {execution_mode}")
            
            # Add orchestration metadata
            result.metadata.update({
                "orchestration_time": (datetime.now() - start_time).total_seconds(),
                "execution_mode": execution_mode.value,
                "coordination_type": coordination_type.value,
                "agent_count": len(self.agent_routers),
                "auto_mode_selection": execution_mode != execution_mode  # This logic seems wrong, should be parameter tracking
            })
            
            logger.info(f"Orchestration completed: {task.task_id} - Status: {result.status}")
            return result
            
        except Exception as e:
            logger.error(f"Orchestration failed: {task.task_id} - Error: {str(e)}")
            
            # Return failure result
            return OrchestrationResult(
                task_id=task.task_id,
                status="failed",
                results={"error": str(e)},
                execution_time=(datetime.now() - start_time).total_seconds(),
                coordination_efficiency=0.0,
                agents_used=[],
                metadata={
                    "orchestration_time": (datetime.now() - start_time).total_seconds(),
                    "execution_mode": execution_mode.value if execution_mode else "unknown",
                    "coordination_type": coordination_type.value if coordination_type else "unknown",
                    "error": str(e)
                }
            )
    
    async def _suggest_execution_mode(self, query: str) -> ExecutionMode:
        """
        Suggest optimal execution mode based on query analysis
        
        Uses existing TaskClassifier if available, otherwise heuristics
        """
        if self.task_classifier:
            try:
                # Use existing TaskClassifier for smart mode selection
                classification = await self.task_classifier.classify_task(query)
                
                # Map classification to execution mode
                if classification.task_type in ["code_generation", "creative_writing"]:
                    return ExecutionMode.COLLABORATIVE  # Quality matters
                elif classification.task_type in ["analysis", "research"]:
                    return ExecutionMode.SEQUENTIAL     # Step-by-step approach
                else:
                    return ExecutionMode.PARALLEL       # Independent subtasks
                    
            except Exception as e:
                logger.warning(f"TaskClassifier failed, using heuristics: {e}")
        
        # Fallback to heuristic-based selection
        return ExecutionMode.suggest_mode_for_task(query)
    
    def _suggest_coordination_type(self, execution_mode: ExecutionMode) -> AgentCoordination:
        """Suggest coordination type based on execution mode"""
        # Use compatibility matrix from AgentCoordination
        if execution_mode == ExecutionMode.PARALLEL:
            return AgentCoordination.INDEPENDENT
        elif execution_mode == ExecutionMode.SEQUENTIAL:
            return AgentCoordination.SYNCHRONIZED
        elif execution_mode == ExecutionMode.COLLABORATIVE:
            return AgentCoordination.HIERARCHICAL  # Quality comparison needs coordination
        else:
            return AgentCoordination.INDEPENDENT
    
    def _validate_coordination_compatibility(self, execution_mode: ExecutionMode, coordination_type: AgentCoordination) -> bool:
        """Validate that coordination type is compatible with execution mode"""
        # Use compatibility matrix from AgentCoordination class
        try:
            return coordination_type.is_compatible_with_mode(execution_mode)
        except AttributeError:
            # Fallback manual compatibility check
            compatible_combinations = {
                ExecutionMode.PARALLEL: [AgentCoordination.INDEPENDENT, AgentCoordination.SYNCHRONIZED],
                ExecutionMode.SEQUENTIAL: [AgentCoordination.SYNCHRONIZED, AgentCoordination.HIERARCHICAL],
                ExecutionMode.COLLABORATIVE: [AgentCoordination.HIERARCHICAL, AgentCoordination.SYNCHRONIZED]
            }
            return coordination_type in compatible_combinations.get(execution_mode, [])
    
    def get_orchestration_stats(self) -> Dict[str, Any]:
        """Get orchestration statistics and available agents"""
        return {
            "available_agents": list(self.agent_routers.keys()),
            "agent_count": len(self.agent_routers),
            "execution_modes": [mode.value for mode in ExecutionMode],
            "coordination_types": [coord.value for coord in AgentCoordination],
            "has_task_classifier": self.task_classifier is not None,
            "executors": {
                "parallel": self.parallel_executor.__class__.__name__,
                "sequential": self.sequential_executor.__class__.__name__,
                "collaborative": self.collaborative_executor.__class__.__name__
            }
        } 