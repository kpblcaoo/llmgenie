"""
Test ParallelExecutor implementation

Epic 5 Phase 3.2: Modular executor tests
Single responsibility: Test ParallelExecutor only
"""

import pytest
import asyncio
from unittest.mock import Mock

from src.llmgenie.orchestration.executors import ParallelExecutor
from ..fixtures import create_mock_router, sample_task


class TestParallelExecutor:
    """Test parallel execution strategy"""
    
    @pytest.fixture
    def parallel_executor(self):
        """Create ParallelExecutor with mock routers"""
        mock_routers = {
            "agent1": create_mock_router("agent1"),
            "agent2": create_mock_router("agent2")
        }
        return ParallelExecutor(mock_routers)
    
    @pytest.mark.asyncio
    async def test_parallel_execution_success(self, parallel_executor, sample_task):
        """Test successful parallel execution"""
        result = await parallel_executor.execute(sample_task)
        
        assert result.task_id == sample_task.task_id
        assert result.status == "completed"
        assert len(result.results) == 2  # Two agents
        assert len(result.agents_used) == 2
        assert result.coordination_efficiency == 1.0  # All succeeded
    
    @pytest.mark.asyncio
    async def test_parallel_execution_partial_failure(self, parallel_executor, sample_task):
        """Test parallel execution with one agent failing"""
        # Make one agent fail
        parallel_executor.agent_routers["agent1"].route_task.side_effect = Exception("Network error")
        
        result = await parallel_executor.execute(sample_task)
        
        assert result.status == "partial"
        # Check that at least one subtask failed
        failed_subtasks = [k for k, v in result.results.items() if v["status"] == "failed"]
        assert len(failed_subtasks) >= 1
        
        # Check that the error is recorded
        failed_subtask = result.results[failed_subtasks[0]]
        assert "Network error" in failed_subtask["error"]
        assert result.coordination_efficiency < 1.0  # Not all succeeded
    
    @pytest.mark.asyncio
    async def test_subtask_decomposition(self, parallel_executor):
        """Test automatic subtask decomposition"""
        query = "Create a web application with frontend and backend"
        subtasks = await parallel_executor._decompose_task(query)
        
        assert len(subtasks) >= 2
        assert any("frontend" in subtask.lower() for subtask in subtasks)
        assert any("backend" in subtask.lower() for subtask in subtasks)
    
    @pytest.mark.asyncio
    async def test_timing_efficiency(self, parallel_executor, sample_task):
        """Test that parallel execution is actually parallel"""
        # Add delays to execution
        async def delayed_execute(*args, **kwargs):
            await asyncio.sleep(0.05)  # 50ms delay
            return {"result": "delayed result"}
        
        for router in parallel_executor.agent_routers.values():
            router.execute_with_model = delayed_execute
        
        import time
        start = time.time()
        result = await parallel_executor.execute(sample_task)
        elapsed = time.time() - start
        
        # Should take ~50ms (parallel), not ~100ms (sequential)
        assert elapsed < 0.08  # Some overhead expected
        assert result.status == "completed" 