"""
Model Router for Smart LLM Selection

Integrates with existing FastAPI infrastructure (main.py:98-112)
Extends AgentRequest/AgentResponse pattern with Ollama backend
"""

from enum import Enum
from typing import Dict, Optional, Any, Union
from dataclasses import dataclass
import asyncio
import httpx
from datetime import datetime

from .task_classifier import TaskClassifier, ClassificationResult


class ModelChoice(Enum):
    """Available LLM backends for task execution"""
    CLAUDE_SONNET = "claude-3-5-sonnet-20241022"
    OLLAMA_MISTRAL = "mistral:7b-instruct"
    OLLAMA_CODELLAMA = "codellama:7b"
    OLLAMA_LLAMA31 = "llama3.1:70b-instruct"
    AUTO = "auto"  # Let router decide


@dataclass
class RoutingDecision:
    """Result of routing decision process"""
    selected_model: ModelChoice
    reasoning: str
    confidence_score: float
    fallback_model: Optional[ModelChoice]
    estimated_latency: float
    quality_threshold: float


class ModelRouter:
    """
    Smart Model Router for LLM task execution
    
    Extends existing FastAPI agent pattern from main.py:98-112
    Integrates with AgentRequest/AgentResponse models
    """
    
    def __init__(self, classifier: Optional[TaskClassifier] = None):
        """Initialize router with task classifier"""
        self.classifier = classifier or TaskClassifier()
        self.ollama_base_url = "http://localhost:11434"
        self.claude_api_key = None  # Will be set from environment
        
        # Performance baselines from Epic 5 testing
        self.model_performance = {
            ModelChoice.OLLAMA_MISTRAL: {"latency": 24.97, "quality": 0.75},
            ModelChoice.OLLAMA_CODELLAMA: {"latency": 30.0, "quality": 0.80},
            ModelChoice.OLLAMA_LLAMA31: {"latency": 45.0, "quality": 0.85},
            ModelChoice.CLAUDE_SONNET: {"latency": 8.94, "quality": 0.95}
        }

    async def route_task(self, query: str, context: Optional[Dict] = None, 
                        model_preference: ModelChoice = ModelChoice.AUTO) -> RoutingDecision:
        """
        Route task to optimal LLM based on classification and performance
        
        Args:
            query: Task description/request
            context: Additional context (file types, project info, etc.)
            model_preference: User's model preference (overrides auto-routing)
            
        Returns:
            RoutingDecision with selected model and reasoning
        """
        
        # If user specified model preference, respect it
        if model_preference != ModelChoice.AUTO:
            return await self._create_preference_decision(model_preference, query)
        
        # Classify task using Epic 5 research patterns
        classification = self.classifier.classify_task(query, context)
        
        # Select optimal model based on classification
        selected_model = await self._select_optimal_model(classification)
        
        # Determine fallback model
        fallback_model = self._get_fallback_model(selected_model)
        
        # Estimate performance
        estimated_latency = self.model_performance[selected_model]["latency"]
        quality_threshold = self._calculate_quality_threshold(classification)
        
        # Generate routing reasoning
        reasoning = self._generate_routing_reasoning(classification, selected_model)
        
        return RoutingDecision(
            selected_model=selected_model,
            reasoning=reasoning,
            confidence_score=classification.confidence_score,
            fallback_model=fallback_model,
            estimated_latency=estimated_latency,
            quality_threshold=quality_threshold
        )

    async def _select_optimal_model(self, classification: ClassificationResult) -> ModelChoice:
        """Select optimal model based on task classification"""
        
        # Epic 5 research-based routing decisions
        if classification.ollama_preference:
            # Route to best available Ollama model
            if classification.task_type.value in ["code_generation", "refactoring"]:
                return ModelChoice.OLLAMA_CODELLAMA
            elif classification.task_type.value == "documentation":
                return ModelChoice.OLLAMA_MISTRAL
            else:
                return ModelChoice.OLLAMA_MISTRAL  # Default Ollama choice
                
        elif classification.claude_preference:
            return ModelChoice.CLAUDE_SONNET
            
        else:
            # Mixed complexity - choose based on quality requirements
            if classification.complexity_level.value >= 3:
                return ModelChoice.CLAUDE_SONNET
            else:
                return ModelChoice.OLLAMA_MISTRAL

    async def execute_with_model(self, query: str, model_choice: ModelChoice, 
                               context: Optional[Dict] = None) -> Dict[str, Any]:
        """Execute task with specified model"""
        start_time = datetime.now()
        
        try:
            if model_choice.name.startswith("OLLAMA_"):
                result = await self._execute_ollama_task(query, model_choice, context)
            elif model_choice == ModelChoice.CLAUDE_SONNET:
                result = await self._execute_claude_task(query, context)
            else:
                raise ValueError(f"Unsupported model choice: {model_choice}")
                
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "result": result,
                "model": model_choice.value,
                "execution_time": execution_time,
                "timestamp": datetime.now().isoformat(),
                "status": "success"
            }
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return {
                "result": None,
                "model": model_choice.value,
                "execution_time": execution_time,
                "timestamp": datetime.now().isoformat(),
                "status": "error",
                "error": str(e)
            }

    async def _execute_ollama_task(self, query: str, model_choice: ModelChoice, 
                                 context: Optional[Dict]) -> str:
        """Execute task using Ollama API"""
        
        model_name = model_choice.value
        
        # Prepare Ollama request (OpenAI-compatible format)
        payload = {
            "model": model_name,
            "messages": [
                {"role": "user", "content": query}
            ],
            "stream": False
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.ollama_base_url}/v1/chat/completions",
                json=payload,
                timeout=120.0
            )
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]

    async def _execute_claude_task(self, query: str, context: Optional[Dict]) -> str:
        """Execute task using Claude API - placeholder for integration"""
        return f"Claude would handle: {query[:100]}..."

    def _get_fallback_model(self, primary_model: ModelChoice) -> ModelChoice:
        """Determine fallback model for reliability"""
        
        fallback_map = {
            ModelChoice.OLLAMA_MISTRAL: ModelChoice.CLAUDE_SONNET,
            ModelChoice.OLLAMA_CODELLAMA: ModelChoice.OLLAMA_MISTRAL,
            ModelChoice.OLLAMA_LLAMA31: ModelChoice.OLLAMA_MISTRAL,
            ModelChoice.CLAUDE_SONNET: ModelChoice.OLLAMA_MISTRAL
        }
        
        return fallback_map.get(primary_model, ModelChoice.CLAUDE_SONNET)

    def _calculate_quality_threshold(self, classification: ClassificationResult) -> float:
        """Calculate minimum quality threshold based on task complexity"""
        
        base_thresholds = {
            1: 0.6,  # Simple tasks
            2: 0.7,  # Moderate complexity
            3: 0.8,  # Complex tasks
            4: 0.9   # Critical tasks
        }
        
        return base_thresholds.get(classification.complexity_level.value, 0.7)

    async def _create_preference_decision(self, model_preference: ModelChoice, 
                                        query: str) -> RoutingDecision:
        """Create routing decision for user-specified model preference"""
        
        estimated_latency = self.model_performance[model_preference]["latency"]
        
        return RoutingDecision(
            selected_model=model_preference,
            reasoning=f"User preference: {model_preference.value}",
            confidence_score=1.0,
            fallback_model=self._get_fallback_model(model_preference),
            estimated_latency=estimated_latency,
            quality_threshold=0.7
        )

    def _generate_routing_reasoning(self, classification: ClassificationResult, 
                                  selected_model: ModelChoice) -> str:
        """Generate human-readable reasoning for routing decision"""
        
        reasoning_parts = [
            f"Task: {classification.task_type.value}",
            f"Complexity: {classification.complexity_level.name.lower()}",
            f"Selected: {selected_model.value}",
            classification.reasoning
        ]
        
        return " | ".join(reasoning_parts) 