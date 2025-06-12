"""
Multi-Agent Orchestration Package

Epic 5 Phase 3.1: Complete orchestration system
- AgentOrchestrator: Main orchestration class
- Core: ExecutionMode, AgentCoordination, OrchestrationTask, OrchestrationResult
- Executors: ParallelExecutor, SequentialExecutor, CollaborativeExecutor
"""

# Main orchestrator
from .orchestrator import AgentOrchestrator

# Core types and models
from .core import (
    ExecutionMode, 
    AgentCoordination, 
    OrchestrationTask, 
    OrchestrationResult
)

# Execution strategies
from .executors import (
    ParallelExecutor, 
    SequentialExecutor, 
    CollaborativeExecutor
)

__all__ = [
    # Main orchestrator
    "AgentOrchestrator",
    
    # Core types
    "ExecutionMode",
    "AgentCoordination", 
    "OrchestrationTask",
    "OrchestrationResult",
    
    # Executors
    "ParallelExecutor",
    "SequentialExecutor", 
    "CollaborativeExecutor"
] 