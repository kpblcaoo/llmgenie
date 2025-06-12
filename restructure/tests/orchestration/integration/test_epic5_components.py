"""
Test integration with Epic 5 components

Epic 5 Phase 3.2: Modular integration tests
Single responsibility: Test Epic 5 TaskRouter/ModelRouter integration only
"""

import pytest
from unittest.mock import Mock, AsyncMock

from src.llmgenie.orchestration import AgentOrchestrator, ExecutionMode
from src.llmgenie.task_router import TaskClassifier
from ..fixtures import create_mock_router, create_mock_classification


class TestEpic5Integration:
    """Test integration with Epic 5 TaskRouter components"""
    
    @pytest.fixture
    def orchestrator_with_classifier(self):
        """Create orchestrator with TaskClassifier integration"""
        routers = {
            "mistral": create_mock_router("mistral:7b-instruct"),
            "codellama": create_mock_router("codellama:7b-instruct")
        }
        
        # Mock TaskClassifier
        classifier = Mock(spec=TaskClassifier)
        classifier.classify_task = AsyncMock()
        classifier.classify_task.return_value = create_mock_classification()
        
        return AgentOrchestrator(agent_routers=routers, task_classifier=classifier)
    
    @pytest.mark.asyncio
    async def test_auto_mode_selection(self, orchestrator_with_classifier):
        """Test automatic mode selection using TaskClassifier"""
        # Mock classification for code generation
        orchestrator_with_classifier.task_classifier.classify_task.return_value = create_mock_classification(
            task_type="code_generation", 
            confidence=0.9
        )
        
        result = await orchestrator_with_classifier.orchestrate("Create a Python function")
        
        # Should auto-select COLLABORATIVE for code generation
        assert result.metadata["execution_mode"] == ExecutionMode.COLLABORATIVE.value
        orchestrator_with_classifier.task_classifier.classify_task.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_model_router_interface_compliance(self):
        """Test that orchestration correctly uses ModelRouter interface"""
        router = create_mock_router("test_model")
        orchestrator = AgentOrchestrator({"test": router})
        
        result = await orchestrator.orchestrate(
            query="Test task",
            execution_mode=ExecutionMode.PARALLEL
        )
        
        # Verify ModelRouter methods were called correctly
        router.route_task.assert_called()
        router.execute_with_model.assert_called()
        
        # Verify that calls were made with proper arguments
        assert router.route_task.call_count >= 1
        assert router.execute_with_model.call_count >= 1
        
        # Check that result has expected structure
        assert result.task_id is not None
        assert result.status in ["completed", "partial", "failed"]
    
    def test_orchestrator_stats_with_classifier(self, orchestrator_with_classifier):
        """Test orchestrator stats when TaskClassifier is available"""
        stats = orchestrator_with_classifier.get_orchestration_stats()
        
        assert stats["has_task_classifier"] is True
        assert stats["agent_count"] == 2
        assert "execution_modes" in stats
        assert len(stats["execution_modes"]) == 3
    
    def test_orchestrator_stats_without_classifier(self):
        """Test orchestrator stats when TaskClassifier is not available"""
        routers = {"agent1": create_mock_router("agent1")}
        orchestrator = AgentOrchestrator(routers)
        
        stats = orchestrator.get_orchestration_stats()
        
        assert stats["has_task_classifier"] is False
        assert stats["agent_count"] == 1
        assert "executors" in stats 