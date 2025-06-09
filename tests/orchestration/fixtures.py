"""
Shared test fixtures for orchestration testing

Epic 5 Phase 3.2: Modular test utilities
Single responsibility: Common test setup utilities
"""

import pytest
from unittest.mock import Mock, AsyncMock
from dataclasses import dataclass

from src.llmgenie.task_router import ModelRouter, ModelChoice, RoutingDecision


def create_mock_router(model_name: str) -> Mock:
    """Create standardized mock ModelRouter for testing"""
    router = Mock(spec=ModelRouter)
    router.route_task = AsyncMock()
    router.execute_with_model = AsyncMock()
    
    # Standard routing decision
    router.route_task.return_value = RoutingDecision(
        selected_model=ModelChoice.OLLAMA_MISTRAL,
        reasoning=f"Selected {model_name} for task",
        confidence_score=0.8,
        fallback_model=ModelChoice.CLAUDE_SONNET,
        estimated_latency=1.5,
        quality_threshold=0.7
    )
    
    # Standard execution result
    router.execute_with_model.return_value = {
        "result": f"Task completed by {model_name}",
        "model": model_name,
        "execution_time": 1.2,
        "status": "success"
    }
    
    return router


@dataclass
class MockClassification:
    """Mock classification result for testing"""
    task_type: str
    confidence: float
    reasoning: str


def create_mock_classification(task_type: str = "analysis", confidence: float = 0.85) -> MockClassification:
    """Create standardized mock classification for testing"""
    return MockClassification(
        task_type=task_type,
        confidence=confidence,
        reasoning=f"Classified as {task_type}"
    )


@pytest.fixture
def mock_agent_routers():
    """Standard set of mock agent routers for testing"""
    return {
        "mistral": create_mock_router("mistral:7b-instruct"),
        "codellama": create_mock_router("codellama:7b-instruct"),
        "llama3": create_mock_router("llama3:latest")
    }


@pytest.fixture
def sample_task():
    """Standard orchestration task for testing"""
    from src.llmgenie.orchestration.core import OrchestrationTask
    
    return OrchestrationTask(
        task_id="test_task_123",
        query="Analyze this code for bugs and performance issues",
        context={"language": "python"},
        subtasks=["Check for syntax errors", "Analyze performance bottlenecks"]
    ) 