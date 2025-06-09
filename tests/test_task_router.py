"""
Comprehensive tests for Epic 5 TaskRouter implementation

Tests task classification, model routing, and integration with FastAPI
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from src.llmgenie.task_router import (
    TaskClassifier, TaskType, ComplexityLevel,
    ModelRouter, ModelChoice, RoutingDecision,
    QualityValidator, QualityScore, QualityResult
)


class TestTaskClassifier:
    """Test TaskClassifier with Epic 5 research patterns"""
    
    def setup_method(self):
        """Setup classifier for each test"""
        self.classifier = TaskClassifier()
    
    def test_code_generation_classification(self):
        """Test code generation task classification"""
        query = "def create_user_function(name, email): implement user creation logic"
        result = self.classifier.classify_task(query)
        
        assert result.task_type == TaskType.CODE_GENERATION
        assert result.ollama_preference == True
        assert result.confidence_score > 0.7
        
    def test_documentation_classification(self):
        """Test documentation task classification"""
        query = "Write README documentation for the project explaining installation"
        result = self.classifier.classify_task(query)
        
        assert result.task_type == TaskType.DOCUMENTATION
        assert result.ollama_preference == True
        
    def test_complex_reasoning_classification(self):
        """Test complex reasoning task classification"""
        query = "Design microservice architecture for scalable user management system with authentication"
        result = self.classifier.classify_task(query)
        
        assert result.task_type == TaskType.ARCHITECTURE_PLANNING
        assert result.claude_preference == True
        assert result.complexity_level.value >= 3
        
    def test_debugging_classification(self):
        """Test debugging task classification"""
        query = "Fix this error: TypeError: unsupported operand type(s) for +: 'int' and 'str'"
        result = self.classifier.classify_task(query)
        
        assert result.task_type == TaskType.DEBUGGING
        assert result.ollama_preference == True
        
    def test_complexity_scoring(self):
        """Test complexity level calculation"""
        simple_query = "rename variable x to user_count"
        moderate_query = "refactor user authentication module for better performance"
        complex_query = "architect distributed authentication system with microservices"
        critical_query = "migrate production database with zero downtime and security compliance"
        
        simple_result = self.classifier.classify_task(simple_query)
        moderate_result = self.classifier.classify_task(moderate_query)
        complex_result = self.classifier.classify_task(complex_query)
        critical_result = self.classifier.classify_task(critical_query)
        
        assert simple_result.complexity_level == ComplexityLevel.SIMPLE
        assert moderate_result.complexity_level.value >= 2
        assert complex_result.complexity_level.value >= 3
        assert critical_result.complexity_level == ComplexityLevel.CRITICAL
        
    def test_context_based_classification(self):
        """Test classification with context information"""
        query = "optimize this function"
        context = {
            "file_types": [".py", ".js"],
            "file_count": 15,
            "dependencies": ["fastapi", "ollama"]
        }
        
        result = self.classifier.classify_task(query, context)
        assert result.task_type == TaskType.CODE_GENERATION
        assert result.complexity_level.value >= 2  # Context increases complexity


class TestModelRouter:
    """Test ModelRouter with Epic 5 integration patterns"""
    
    def setup_method(self):
        """Setup router for each test"""
        self.classifier = TaskClassifier()
        self.router = ModelRouter(self.classifier)
    
    @pytest.mark.asyncio
    async def test_ollama_routing_preference(self):
        """Test routing to Ollama for code generation"""
        query = "def process_data(data): implement data processing logic with validation"
        
        decision = await self.router.route_task(query)
        
        assert decision.selected_model.name.startswith("OLLAMA_")
        assert "code_generation" in decision.reasoning
        assert decision.confidence_score > 0.5
        
    @pytest.mark.asyncio
    async def test_claude_routing_preference(self):
        """Test routing to Claude for complex reasoning"""
        query = "Design high-availability architecture for user authentication service"
        
        decision = await self.router.route_task(query)
        
        assert decision.selected_model == ModelChoice.CLAUDE_SONNET
        assert "complex" in decision.reasoning.lower()
        
    @pytest.mark.asyncio
    async def test_user_model_preference(self):
        """Test user model preference override"""
        query = "simple task"
        
        decision = await self.router.route_task(
            query, 
            model_preference=ModelChoice.OLLAMA_CODELLAMA
        )
        
        assert decision.selected_model == ModelChoice.OLLAMA_CODELLAMA
        assert "User preference" in decision.reasoning
        assert decision.confidence_score == 1.0
        
    @pytest.mark.asyncio
    async def test_fallback_model_selection(self):
        """Test fallback model logic"""
        query = "test query"
        
        decision = await self.router.route_task(query)
        
        assert decision.fallback_model is not None
        assert decision.fallback_model != decision.selected_model
        
    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.post')
    async def test_ollama_execution(self, mock_post):
        """Test actual Ollama execution"""
        # Mock Ollama response
        mock_response = Mock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Generated code result"}}]
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        result = await self.router.execute_with_model(
            "def test(): pass", 
            ModelChoice.OLLAMA_MISTRAL
        )
        
        assert result["status"] == "success"
        assert result["result"] == "Generated code result"
        assert result["model"] == "mistral:7b-instruct"
        assert "execution_time" in result
        
    @pytest.mark.asyncio
    async def test_claude_execution_placeholder(self):
        """Test Claude execution (placeholder implementation)"""
        result = await self.router.execute_with_model(
            "Design architecture", 
            ModelChoice.CLAUDE_SONNET
        )
        
        assert result["status"] == "success"
        assert "Claude would handle" in result["result"]
        assert result["model"] == "claude-3-5-sonnet-20241022"
        
    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.post')
    async def test_error_handling(self, mock_post):
        """Test error handling in execution"""
        # Mock Ollama error
        mock_post.side_effect = Exception("Ollama connection failed")
        
        result = await self.router.execute_with_model(
            "test query", 
            ModelChoice.OLLAMA_MISTRAL
        )
        
        assert result["status"] == "error"
        assert "error" in result
        assert "Ollama connection failed" in result["error"]


class TestPerformanceOptimization:
    """Test performance optimization based on Epic 5 baselines"""
    
    def setup_method(self):
        """Setup for performance tests"""
        self.router = ModelRouter()
    
    def test_model_performance_baselines(self):
        """Test that performance baselines match Epic 5 findings"""
        # Epic 5 baselines from testing
        expected_baselines = {
            ModelChoice.OLLAMA_MISTRAL: 24.97,
            ModelChoice.CLAUDE_SONNET: 8.94
        }
        
        for model, expected_latency in expected_baselines.items():
            actual_latency = self.router.model_performance[model]["latency"]
            assert actual_latency == expected_latency
            
    @pytest.mark.asyncio
    async def test_routing_decision_optimization(self):
        """Test routing optimization for performance"""
        # Simple task should route to fast Ollama model
        simple_query = "format this code snippet"
        decision = await self.router.route_task(simple_query)
        
        # Should prefer Ollama for simple tasks (faster execution)
        assert decision.selected_model.name.startswith("OLLAMA_")
        assert decision.estimated_latency > 8.0  # Ollama is slower than Claude
        
    def test_quality_threshold_calculation(self):
        """Test quality threshold based on task complexity"""
        classifier = TaskClassifier()
        
        simple_task = classifier.classify_task("fix typo")
        complex_task = classifier.classify_task("architect microservice system")
        
        simple_threshold = self.router._calculate_quality_threshold(simple_task)
        complex_threshold = self.router._calculate_quality_threshold(complex_task)
        
        assert simple_threshold < complex_threshold
        assert complex_threshold >= 0.8  # High quality for complex tasks


class TestIntegrationWithFastAPI:
    """Test integration with existing FastAPI infrastructure"""
    
    def test_agent_request_compatibility(self):
        """Test compatibility with existing AgentRequest model"""
        # This test would verify that TaskRouter integrates cleanly
        # with the existing FastAPI endpoint structure
        
        classifier = TaskClassifier()
        
        # Simulate AgentRequest data
        agent_request_data = {
            "agent_type": "auto",
            "task": "def calculate_total(items): implement calculation logic",
            "context": {"file_types": [".py"], "project": "llmgenie"}
        }
        
        result = classifier.classify_task(
            agent_request_data["task"], 
            agent_request_data["context"]
        )
        
        assert result.task_type == TaskType.CODE_GENERATION
        assert isinstance(result.ollama_preference, bool)
        
    @pytest.mark.asyncio
    async def test_routing_decision_serialization(self):
        """Test that RoutingDecision can be serialized for API responses"""
        router = ModelRouter()
        decision = await router.route_task("test query")
        
        # Test that decision can be converted to dict for JSON serialization
        decision_dict = {
            "selected_model": decision.selected_model.value,
            "reasoning": decision.reasoning,
            "confidence_score": decision.confidence_score,
            "estimated_latency": decision.estimated_latency
        }
        
        assert isinstance(decision_dict["selected_model"], str)
        assert isinstance(decision_dict["reasoning"], str)
        assert isinstance(decision_dict["confidence_score"], float)
        assert isinstance(decision_dict["estimated_latency"], float)


class TestQualityValidator:
    """Test enhanced Quality Validator with real validation logic"""
    
    def setup_method(self):
        """Setup for quality validator tests"""
        self.validator = QualityValidator()
    
    def test_python_code_validation_success(self):
        """Test successful Python code validation"""
        good_code = '''
def fibonacci(n):
    """Calculate fibonacci number"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Example usage
result = fibonacci(10)
print(f"Result: {result}")
        '''
        
        result = self.validator.validate_code_output(good_code, "python")
        
        assert result.score.value >= 3  # At least ACCEPTABLE
        assert result.confidence > 0.7
        assert not result.needs_fallback
        assert "syntax valid" in result.reasoning
        assert result.metrics["has_docstrings"] == True
        assert result.metrics["has_comments"] == True
        assert result.metrics["function_count"] == 1
        
    def test_python_code_validation_syntax_error(self):
        """Test Python code with syntax errors"""
        bad_code = '''
def broken_function(
    # Missing closing parenthesis
    return "this will fail"
        '''
        
        result = self.validator.validate_code_output(bad_code, "python")
        
        assert result.score == QualityScore.FAILED
        assert result.needs_fallback == True
        assert result.confidence > 0.9  # High confidence in syntax error detection
        assert any("syntax error" in issue.lower() for issue in result.issues)
        
    def test_javascript_code_validation(self):
        """Test JavaScript code validation"""
        js_code = '''
function calculateTotal(items) {
    // Calculate total price
    let total = 0;
    for (let item of items) {
        total += item.price;
    }
    return total;
}

const items = [{price: 10}, {price: 20}];
console.log(calculateTotal(items));
        '''
        
        result = self.validator.validate_code_output(js_code, "javascript")
        
        assert result.score.value >= 3
        assert result.metrics["has_functions"] == True
        assert result.metrics["has_comments"] == True
        assert result.confidence == 0.7  # Expected confidence for JS
        
    def test_text_validation_high_quality(self):
        """Test high-quality text validation"""
        good_text = '''
This is a comprehensive explanation of the task router system. 

First, the system analyzes the incoming query to determine its complexity and type. 
Therefore, it can make intelligent routing decisions between different AI models.

For example, simple code generation tasks are routed to Ollama because it provides 
faster execution and lower costs. However, complex architectural decisions require 
Claude's superior reasoning capabilities.

In conclusion, this approach optimizes both performance and cost while maintaining 
high quality standards across all task types.
        '''
        
        result = self.validator.validate_text_output(good_text, "explanation")
        
        assert result.score.value >= 4  # GOOD or EXCELLENT
        assert result.confidence > 0.8
        assert not result.needs_fallback
        assert result.metrics["word_count"] > 50
        assert result.metrics["coherence_score"] > 0.5
        assert result.metrics["completeness_score"] > 0.5
        
    def test_text_validation_poor_quality(self):
        """Test poor quality text validation"""
        poor_text = "yes"
        
        result = self.validator.validate_text_output(poor_text)
        
        assert result.score.value <= 2  # POOR or FAILED
        assert result.needs_fallback == True
        assert "very short" in result.issues[0].lower()
        assert result.metrics["word_count"] < 10
        
    def test_documentation_specific_validation(self):
        """Test documentation-specific validation"""
        doc_text = '''
API Usage Guide

This function accepts the following parameters:
- query: string (required) - The input query to process
- context: dict (optional) - Additional context information

Returns:
- result: dict - The processed result with status and data

Example:
```python
result = process_query("hello world", {"user": "test"})
```
        '''
        
        result = self.validator.validate_text_output(doc_text, "documentation")
        
        assert result.score.value >= 4
        assert result.metrics["has_structure"] == True
        # Should not have missing documentation elements issue
        doc_issues = [issue for issue in result.issues if "documentation elements" in issue]
        assert len(doc_issues) == 0
        
    def test_fallback_decision_making(self):
        """Test fallback decision based on task type and quality"""
        from src.llmgenie.task_router.task_classifier import TaskType
        
        # Low quality result for critical task
        poor_result = QualityResult(
            score=QualityScore.POOR,
            confidence=0.3,
            issues=["Multiple issues"],
            reasoning="Poor quality",
            metrics={},
            needs_fallback=False  # Test threshold-based fallback
        )
        
        # Should fallback for architecture planning (high threshold)
        assert self.validator.should_fallback(poor_result, TaskType.ARCHITECTURE_PLANNING) == True
        
        # Might not fallback for code review (lower threshold)
        assert self.validator.should_fallback(poor_result, TaskType.CODE_REVIEW) == True  # Still poor quality
        
        # Excellent quality result should not fallback for high threshold tasks
        excellent_result = QualityResult(
            score=QualityScore.EXCELLENT,
            confidence=0.95,
            issues=[],
            reasoning="Excellent quality",
            metrics={},
            needs_fallback=False
        )
        
        assert self.validator.should_fallback(excellent_result, TaskType.ARCHITECTURE_PLANNING) == False
        
        # Good quality should not fallback for medium threshold tasks
        good_result = QualityResult(
            score=QualityScore.GOOD,
            confidence=0.8,
            issues=[],
            reasoning="Good quality",
            metrics={},
            needs_fallback=False
        )
        
        assert self.validator.should_fallback(good_result, TaskType.CODE_REVIEW) == False
        
    def test_quality_thresholds_by_task_type(self):
        """Test different quality thresholds for different task types"""
        # Architecture planning should have high threshold (0.9)
        assert self.validator.quality_thresholds[TaskType.ARCHITECTURE_PLANNING] == 0.9
        
        # Code generation should have high threshold (0.8)
        assert self.validator.quality_thresholds[TaskType.CODE_GENERATION] == 0.8
        
        # Code review should have medium threshold (0.7)
        assert self.validator.quality_thresholds[TaskType.CODE_REVIEW] == 0.7
        
    def test_coherence_score_calculation(self):
        """Test text coherence scoring"""
        coherent_text = "first we analyze the problem. therefore, we can find a solution. however, there are challenges."
        
        score = self.validator._calculate_coherence_score(coherent_text)
        
        # Should have high coherence due to transition words
        assert score > 0.5
        
        incoherent_text = "word word word word word word word word"
        score_low = self.validator._calculate_coherence_score(incoherent_text)
        
        # Should have lower coherence due to repetition
        assert score_low < score
        
    def test_completeness_score_calculation(self):
        """Test text completeness scoring"""
        complete_text = '''
        Here is the implementation approach:
        
        1. First step
        2. Second step
        
        For example, we can use this method.
        
        In conclusion, this solution is effective.
        '''
        
        score = self.validator._calculate_completeness_score(complete_text.lower())
        
        # Should have high completeness due to structure and keywords
        assert score > 0.6
        
    def test_empty_input_handling(self):
        """Test handling of empty inputs"""
        # Empty code
        code_result = self.validator.validate_code_output("")
        assert code_result.score == QualityScore.FAILED
        assert code_result.needs_fallback == True
        assert "empty code" in code_result.issues[0].lower()
        
        # Empty text
        text_result = self.validator.validate_text_output("")
        assert text_result.score == QualityScore.FAILED
        assert text_result.needs_fallback == True
        assert "empty text" in text_result.issues[0].lower()
        
    def test_quality_metrics_extraction(self):
        """Test quality metrics extraction for monitoring"""
        result = QualityResult(
            score=QualityScore.GOOD,
            confidence=0.85,
            issues=["minor issue"],
            reasoning="test reasoning",
            metrics={"word_count": 100},
            needs_fallback=False
        )
        
        metrics = self.validator.get_quality_metrics(result)
        
        assert metrics["quality_score"] == 4  # GOOD = 4
        assert metrics["confidence"] == 0.85
        assert metrics["issue_count"] == 1
        assert metrics["needs_fallback"] == False
        assert metrics["metrics"]["word_count"] == 100
        
    def test_generic_code_validation(self):
        """Test generic code validation for unknown languages"""
        generic_code = '''
        function main() {
            var result = calculate(10, 20);
            return result;
        }
        '''
        
        result = self.validator.validate_code_output(generic_code, "unknown")
        
        assert result.score.value >= 2  # At least POOR due to structure
        assert result.confidence == 0.5  # Low confidence for generic
        assert result.metrics["has_structure"] == True


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 