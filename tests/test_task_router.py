"""
Comprehensive tests for Epic 5 TaskRouter implementation

Tests task classification, model routing, and integration with FastAPI
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from src.llmgenie.task_router import (
    TaskClassifier, TaskType, ComplexityLevel,
    ModelRouter, ModelChoice, RoutingDecision
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


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 