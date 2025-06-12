"""
Task data models for orchestration

Epic 5 Phase 3.1: Orchestration task modeling
Single responsibility: Define task and result data structures
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime

from .execution_modes import ExecutionMode
from .coordination_types import AgentCoordination


@dataclass
class OrchestrationTask:
    """
    Task for multi-agent orchestration
    
    Encapsulates all information needed for multi-agent task execution
    """
    task_id: str
    """Unique identifier for the task"""
    
    query: str  
    """Main task description/query to be executed"""
    
    context: Optional[Dict] = None
    """Additional context information for task execution"""
    
    execution_mode: ExecutionMode = ExecutionMode.PARALLEL
    """How the task should be executed (parallel/sequential/collaborative)"""
    
    coordination: AgentCoordination = AgentCoordination.INDEPENDENT
    """How agents should coordinate during execution"""
    
    subtasks: Optional[List[str]] = None
    """Predefined subtasks (if None, will be auto-decomposed)"""
    
    priority: int = 1
    """Task priority (1=highest, higher numbers=lower priority)"""
    
    timeout_seconds: int = 300
    """Maximum execution time in seconds"""
    
    metadata: Dict[str, Any] = field(default_factory=dict)
    """Additional metadata for the task"""
    
    created_at: datetime = field(default_factory=datetime.now)
    """When the task was created"""
    
    def __post_init__(self):
        """Validate task configuration after initialization"""
        # Validate mode and coordination compatibility
        if not self.coordination.is_suitable_for_mode(self.execution_mode):
            raise ValueError(
                f"Coordination {self.coordination.value} not suitable for "
                f"execution mode {self.execution_mode.value}"
            )
        
        # Ensure task_id is set
        if not self.task_id:
            self.task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    
    def get_estimated_agents_needed(self) -> int:
        """Estimate number of agents needed for this task"""
        if self.execution_mode == ExecutionMode.PARALLEL:
            return len(self.subtasks) if self.subtasks else 3  # Default 3 for parallel
        elif self.execution_mode == ExecutionMode.SEQUENTIAL:
            return 1  # Sequential uses one agent at a time
        elif self.execution_mode == ExecutionMode.COLLABORATIVE:
            return 3  # Default 3 agents for collaboration
        return 1
    
    def get_estimated_duration(self) -> int:
        """Estimate task duration in seconds"""
        base_time = 60  # Base 1 minute
        
        # Adjust based on execution mode
        if self.execution_mode == ExecutionMode.PARALLEL:
            return base_time  # Parallel is fastest
        elif self.execution_mode == ExecutionMode.SEQUENTIAL:
            return base_time * (len(self.subtasks) if self.subtasks else 3)
        elif self.execution_mode == ExecutionMode.COLLABORATIVE:
            return base_time * 2  # Collaborative takes longer due to comparison
            
        return base_time


@dataclass
class OrchestrationResult:
    """
    Result of multi-agent orchestration
    
    Contains execution results and performance metrics
    """
    task_id: str
    """ID of the task that was executed"""
    
    status: str
    """Execution status: 'completed', 'partial', 'failed'"""
    
    results: Dict[str, Any]  
    """Results from individual agents/steps"""
    
    execution_time: float
    """Total execution time in seconds"""
    
    quality_score: Optional[float] = None
    """Overall quality score (0.0-1.0)"""
    
    coordination_efficiency: Optional[float] = None
    """How efficiently agents coordinated (0.0-1.0)"""
    
    error: Optional[str] = None
    """Error message if execution failed"""
    
    metadata: Optional[Dict] = None
    """Additional result metadata"""
    
    completed_at: datetime = field(default_factory=datetime.now)
    """When the execution completed"""
    
    agents_used: List[str] = field(default_factory=list)
    """List of agents that participated in execution"""
    
    def is_successful(self) -> bool:
        """Check if the orchestration was successful"""
        return self.status in ['completed', 'partial']
    
    def get_summary(self) -> str:
        """Get a human-readable summary of the result"""
        if self.status == 'completed':
            return f"✅ Task {self.task_id} completed successfully in {self.execution_time:.2f}s"
        elif self.status == 'partial':
            return f"⚠️ Task {self.task_id} partially completed in {self.execution_time:.2f}s"
        else:
            return f"❌ Task {self.task_id} failed: {self.error}"
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for analysis"""
        return {
            "execution_time": self.execution_time,
            "quality_score": self.quality_score,
            "coordination_efficiency": self.coordination_efficiency,
            "agents_count": len(self.agents_used),
            "success": self.is_successful()
        } 