"""
Test ExecutionMode enum and smart suggestions

Epic 5 Phase 3.2: Modular core tests
Single responsibility: Test ExecutionMode functionality only
"""

import pytest
from src.llmgenie.orchestration.core import ExecutionMode


class TestExecutionMode:
    """Test ExecutionMode enum functionality"""
    
    def test_execution_mode_values(self):
        """Test that all execution modes have correct values"""
        assert ExecutionMode.PARALLEL.value == "parallel"
        assert ExecutionMode.SEQUENTIAL.value == "sequential" 
        assert ExecutionMode.COLLABORATIVE.value == "collaborative"
    
    def test_suggest_mode_for_collaborative_tasks(self):
        """Test mode suggestion for collaborative tasks"""
        collaborative_queries = [
            "Create complex solution",
            "Generate optimal algorithm", 
            "Write critical code component"
        ]
        
        for query in collaborative_queries:
            mode = ExecutionMode.suggest_mode(query)
            assert mode == ExecutionMode.COLLABORATIVE
    
    def test_suggest_mode_for_sequential_tasks(self):
        """Test mode suggestion for sequential tasks"""
        sequential_queries = [
            "Design then implement step by step",
            "Plan workflow and execute",
            "Review this implementation"
        ]
        
        for query in sequential_queries:
            mode = ExecutionMode.suggest_mode(query)
            assert mode == ExecutionMode.SEQUENTIAL
    
    def test_suggest_mode_for_parallel_tasks(self):
        """Test mode suggestion for parallel tasks"""
        parallel_queries = [
            "Process multiple files and generate reports",
            "Handle several requests plus documentation",
            "Debug components in bulk"
        ]
        
        for query in parallel_queries:
            mode = ExecutionMode.suggest_mode(query)
            assert mode == ExecutionMode.PARALLEL
    
    def test_mode_descriptions(self):
        """Test mode descriptions are available"""
        for mode in ExecutionMode:
            description = mode.get_description()
            assert isinstance(description, str)
            assert len(description) > 10
    
    def test_mode_use_cases(self):
        """Test use cases are available for each mode"""
        for mode in ExecutionMode:
            use_cases = mode.get_use_cases()
            assert isinstance(use_cases, list)
            assert len(use_cases) >= 2
    
    def test_mode_enum_completeness(self):
        """Test that we have expected number of execution modes"""
        modes = list(ExecutionMode)
        assert len(modes) == 3
        assert ExecutionMode.PARALLEL in modes
        assert ExecutionMode.SEQUENTIAL in modes
        assert ExecutionMode.COLLABORATIVE in modes 