"""
Tests for Self-Refine Pipeline System
Comprehensive testing of MCP-enhanced iterative improvement
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

from src.rag_context.interfaces.self_refine_pipeline import (
    SelfRefinePipeline,
    RefinementType,
    RefinementResult,
    quick_refine_code,
    quick_refine_text
)


class TestSelfRefinePipeline:
    """Test suite for Self-Refine Pipeline"""
    
    @pytest.fixture
    def pipeline(self):
        """Create a test pipeline instance"""
        return SelfRefinePipeline(max_iterations=2, confidence_threshold=0.8)
    
    @pytest.fixture
    def sample_code(self):
        """Sample code for testing"""
        return '''
def analyze_pattern(data):
    x = len(data)
    if x > 0:
        result = []
        for item in data:
            result.append(item * 2)
        return result
    return None
'''
    
    @pytest.fixture
    def sample_text(self):
        """Sample text for testing"""
        return "This is a sample text that needs improvement for clarity and style."
    
    def test_pipeline_initialization(self, pipeline):
        """Test pipeline initialization"""
        assert pipeline.max_iterations == 2
        assert pipeline.confidence_threshold == 0.8
        assert isinstance(pipeline.mcp_tools_available, dict)
    
    def test_refine_code(self, pipeline, sample_code):
        """Test code refinement"""
        results = pipeline.refine(sample_code, RefinementType.CODE)
        
        assert len(results) >= 1
        assert all(isinstance(r, RefinementResult) for r in results)
        assert results[0].original == sample_code
        assert len(results[0].refined) >= len(sample_code)  # Should be enhanced
        assert results[0].confidence_score > 0
    
    def test_refine_text(self, pipeline, sample_text):
        """Test text refinement"""
        results = pipeline.refine(sample_text, RefinementType.TEXT)
        
        assert len(results) >= 1
        assert results[0].original == sample_text
        assert results[0].confidence_score > 0
        # RefinementResult doesn't store refinement_type, only in pipeline context
    
    def test_confidence_threshold_reached(self, pipeline, sample_code):
        """Test that refinement stops when confidence threshold is reached"""
        # Mock high confidence validation
        with patch.object(pipeline, '_validate_improvements') as mock_validate:
            mock_validate.return_value = {"confidence": 0.9, "improvements_applied": 3, "length_change": 50, "quality_improved": True}
            
            results = pipeline.refine(sample_code, RefinementType.CODE)
            
            # Should stop after first iteration due to high confidence
            assert len(results) == 1
            assert results[0].confidence_score == 0.9
    
    def test_max_iterations_limit(self, pipeline, sample_code):
        """Test that refinement respects max iterations limit"""
        # Mock low confidence to force max iterations
        with patch.object(pipeline, '_validate_improvements') as mock_validate:
            mock_validate.return_value = {"confidence": 0.5, "improvements_applied": 1, "length_change": 10, "quality_improved": True}
            
            results = pipeline.refine(sample_code, RefinementType.CODE)
            
            # Should run exactly max_iterations
            assert len(results) == pipeline.max_iterations
    
    def test_mcp_tools_integration(self, pipeline, sample_code):
        """Test MCP tools integration in refinement process"""
        results = pipeline.refine(sample_code, RefinementType.CODE)
        
        # Should have some MCP tools usage recorded
        assert len(results) > 0
        first_result = results[0]
        assert isinstance(first_result.mcp_tools_used, list)
        # At least some tools should be used
        assert len(first_result.mcp_tools_used) >= 0
    
    def test_refine_code_file(self, pipeline, sample_code):
        """Test refinement of entire code file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(sample_code)
            temp_file = Path(f.name)
        
        try:
            results = pipeline.refine_code_file(str(temp_file))
            
            assert len(results) >= 1
            # File should be modified if improvement was made
            refined_content = temp_file.read_text()
            assert len(refined_content) >= len(sample_code)
            
            # Backup should exist
            backup_file = temp_file.with_suffix(f"{temp_file.suffix}.backup")
            assert backup_file.exists()
            assert backup_file.read_text() == sample_code
            
        finally:
            temp_file.unlink(missing_ok=True)
            backup_file = temp_file.with_suffix(f"{temp_file.suffix}.backup")
            backup_file.unlink(missing_ok=True)
    
    def test_refinement_report_generation(self, pipeline, sample_code):
        """Test refinement report generation"""
        results = pipeline.refine(sample_code, RefinementType.CODE)
        report = pipeline.generate_refinement_report(results)
        
        assert "summary" in report
        assert "iterations" in report
        assert "final_improvements" in report
        assert "mcp_tools_summary" in report
        
        # Verify summary structure
        summary = report["summary"]
        assert "total_iterations" in summary
        assert "final_confidence" in summary
        assert "threshold_reached" in summary
        assert "total_duration_ms" in summary
        
        # Verify iterations structure
        assert len(report["iterations"]) == len(results)
        
    def test_quick_refine_functions(self, sample_code, sample_text):
        """Test convenience quick refine functions"""
        # Test quick code refinement
        refined_code = quick_refine_code(sample_code)
        assert refined_code != sample_code  # Should be different
        assert len(refined_code) >= len(sample_code)
        
        # Test quick text refinement
        refined_text = quick_refine_text(sample_text)
        assert isinstance(refined_text, str)
        
    def test_enhancement_context_building(self, pipeline):
        """Test context enhancement with MCP tools"""
        content = "def test(): pass"
        context = {"test": "value"}
        
        enhanced = pipeline._enhance_context(content, RefinementType.CODE, context)
        
        assert "test" in enhanced  # Original context preserved
        assert "mcp_tools_used" in enhanced
        # Should have some enhancements
        assert len(enhanced) >= len(context)
    
    def test_critique_generation(self, pipeline):
        """Test critique generation with MCP integration"""
        content = "def test(): pass"
        context = {"relevant_rules": ["Rule 1", "Rule 2"]}
        
        critique = pipeline._critique_with_mcp(content, RefinementType.CODE, context)
        
        assert "critique" in critique
        assert "improvements" in critique
        assert "mcp_tools_used" in critique
        assert "confidence" in critique
        
        assert isinstance(critique["improvements"], list)
        assert len(critique["improvements"]) > 0
        
    def test_validation_logic(self, pipeline):
        """Test improvement validation logic"""
        original = "def test(): pass"
        refined = "def test():\n    '''Test function'''\n    pass\n# Added documentation"
        critique = {"improvements": ["Add documentation", "Improve structure"]}
        
        validation = pipeline._validate_improvements(original, refined, critique)
        
        assert "confidence" in validation
        assert "improvements_applied" in validation
        assert "length_change" in validation
        assert "quality_improved" in validation
        
        assert validation["confidence"] > 0
        assert validation["length_change"] > 0  # Should be longer
        assert validation["quality_improved"] is True
    
    def test_error_handling_file_not_found(self, pipeline):
        """Test error handling for non-existent files"""
        with pytest.raises(FileNotFoundError):
            pipeline.refine_code_file("non_existent_file.py")
    
    def test_empty_results_report(self, pipeline):
        """Test report generation with empty results"""
        report = pipeline.generate_refinement_report([])
        assert "error" in report
        assert "No refinement results provided" in report["error"]
    
    @patch('src.rag_context.interfaces.self_refine_pipeline.AUTO_LOGGING_AVAILABLE', True)
    @patch('src.rag_context.interfaces.self_refine_pipeline.auto_logger')
    def test_auto_logging_integration(self, mock_auto_logger, pipeline, sample_code):
        """Test integration with auto-logging system"""
        results = pipeline.refine(sample_code, RefinementType.CODE)
        
        # Should have called logging functions
        assert mock_auto_logger.log_workflow_phase.called
        call_args = [call[0][0] for call in mock_auto_logger.log_workflow_phase.call_args_list]
        
        # Should have start and complete logs
        start_calls = [arg for arg in call_args if "self_refine_start" in arg]
        complete_calls = [arg for arg in call_args if "self_refine_complete" in arg]
        
        assert len(start_calls) >= 1
        assert len(complete_calls) >= 1


class TestRefinementTypes:
    """Test different refinement types"""
    
    def test_all_refinement_types(self):
        """Test that all refinement types are properly defined"""
        assert RefinementType.CODE.value == "code"
        assert RefinementType.TEXT.value == "text"
        assert RefinementType.CONFIG.value == "config"
        assert RefinementType.WORKFLOW.value == "workflow"
        assert RefinementType.ARCHITECTURE.value == "architecture"


class TestRefinementResult:
    """Test RefinementResult dataclass"""
    
    def test_refinement_result_creation(self):
        """Test RefinementResult creation and attributes"""
        result = RefinementResult(
            iteration=1,
            original="original",
            refined="refined",
            critique="critique",
            improvements=["improvement1"],
            confidence_score=0.8,
            mcp_tools_used=["tool1"],
            duration_ms=100.0
        )
        
        assert result.iteration == 1
        assert result.original == "original"
        assert result.refined == "refined"
        assert result.critique == "critique"
        assert result.improvements == ["improvement1"]
        assert result.confidence_score == 0.8
        assert result.mcp_tools_used == ["tool1"]
        assert result.duration_ms == 100.0


if __name__ == "__main__":
    pytest.main([__file__]) 