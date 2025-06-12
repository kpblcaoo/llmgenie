"""
Test OrchestrationTask and OrchestrationResult models

Epic 5 Phase 3.2: Modular core tests
Single responsibility: Test task dataclass models only
"""

import pytest
from datetime import datetime
from src.llmgenie.orchestration.core import (
    OrchestrationTask, 
    OrchestrationResult,
    ExecutionMode,
    AgentCoordination
)


class TestOrchestrationTask:
    """Test OrchestrationTask dataclass"""
    
    def test_orchestration_task_creation(self):
        """Test basic task creation"""
        task = OrchestrationTask(
            task_id="test_123",
            query="Test query"
        )
        
        assert task.task_id == "test_123"
        assert task.query == "Test query"
        assert task.context is None
        assert task.execution_mode == ExecutionMode.PARALLEL
        assert task.coordination == AgentCoordination.INDEPENDENT
        assert task.subtasks is None
        assert task.priority == 1
        assert task.timeout_seconds == 300
        assert task.metadata == {}
        assert isinstance(task.created_at, datetime)
    
    def test_orchestration_task_with_context(self):
        """Test task creation with context"""
        context = {"language": "python", "complexity": "high"}
        task = OrchestrationTask(
            task_id="test_context",
            query="Code generation task",
            context=context
        )
        
        assert task.context == context
        assert task.context["language"] == "python"
    
    def test_orchestration_task_with_subtasks(self):
        """Test task creation with predefined subtasks"""
        subtasks = ["Design", "Implement", "Test"]
        task = OrchestrationTask(
            task_id="test_subtasks",
            query="Development workflow",
            subtasks=subtasks
        )
        
        assert task.subtasks == subtasks
        assert len(task.subtasks) == 3


class TestOrchestrationResult:
    """Test OrchestrationResult dataclass"""
    
    def test_orchestration_result_creation(self):
        """Test basic result creation"""
        result = OrchestrationResult(
            task_id="test_123",
            status="completed",
            results={"step1": "done"},
            execution_time=1.5,
            coordination_efficiency=0.8,
            agents_used=["agent1", "agent2"]
        )
        
        assert result.task_id == "test_123"
        assert result.status == "completed"
        assert result.execution_time == 1.5
        assert result.coordination_efficiency == 0.8
        assert len(result.agents_used) == 2
    
    def test_orchestration_result_with_quality_score(self):
        """Test result creation with quality metrics"""
        result = OrchestrationResult(
            task_id="quality_test",
            status="completed",
            results={"output": "high quality result"},
            execution_time=2.1,
            coordination_efficiency=1.0,
            agents_used=["agent1"],
            quality_score=0.95
        )
        
        assert result.quality_score == 0.95
        assert result.coordination_efficiency == 1.0
    
    def test_orchestration_result_metadata(self):
        """Test result with comprehensive metadata"""
        metadata = {
            "execution_mode": "COLLABORATIVE",
            "coordination_type": "HIERARCHICAL",
            "agent_count": 3
        }
        
        result = OrchestrationResult(
            task_id="metadata_test",
            status="partial",
            results={"partial": "result"},
            execution_time=0.5,
            coordination_efficiency=0.6,
            agents_used=["agent1"],
            metadata=metadata
        )
        
        assert result.metadata == metadata
        assert result.metadata["execution_mode"] == "COLLABORATIVE"
        assert result.status == "partial"
    
    def test_orchestration_result_status_values(self):
        """Test valid status values"""
        valid_statuses = ["completed", "partial", "failed"]
        
        for status in valid_statuses:
            result = OrchestrationResult(
                task_id=f"test_{status}",
                status=status,
                results={},
                execution_time=1.0,
                coordination_efficiency=0.5,
                agents_used=[]
            )
            assert result.status == status
    
    def test_orchestration_result_efficiency_bounds(self):
        """Test coordination efficiency is properly bounded"""
        # Test efficiency values
        efficiencies = [0.0, 0.5, 1.0]
        
        for eff in efficiencies:
            result = OrchestrationResult(
                task_id="efficiency_test",
                status="completed",
                results={},
                execution_time=1.0,
                coordination_efficiency=eff,
                agents_used=[]
            )
            assert 0.0 <= result.coordination_efficiency <= 1.0 