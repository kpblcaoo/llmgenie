"""
Task Router Module for LLMGenie

Intelligent task routing between Claude and Ollama based on:
- Task complexity analysis
- Model capability matching  
- Performance optimization
- Quality requirements

Integrates with existing FastAPI agent infrastructure.
"""

from .task_classifier import TaskClassifier, TaskType, ComplexityLevel
from .model_router import ModelRouter, ModelChoice, RoutingDecision
from .quality_validator import QualityValidator, QualityScore, QualityResult

__all__ = [
    "TaskClassifier",
    "TaskType", 
    "ComplexityLevel",
    "ModelRouter",
    "ModelChoice",
    "RoutingDecision", 
    "QualityValidator",
    "QualityScore",
    "QualityResult"
] 