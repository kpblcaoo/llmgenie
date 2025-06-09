"""
Collaborative execution strategy

Epic 5 Phase 3.1: Collaborative problem solving
Single responsibility: Multiple agents solve same problem, best result selected
"""

from typing import Dict, List, Any, Optional
from datetime import datetime

from ..core import OrchestrationTask, OrchestrationResult
from ...task_router import ModelRouter, ModelChoice, QualityValidator, QualityResult


class CollaborativeExecutor:
    """
    Collaborative problem solving execution strategy
    
    Epic 5 example: Multiple models generate solution, highest quality chosen
    Benefit: Quality optimization, redundancy, multiple perspectives
    """
    
    def __init__(self, agent_routers: Dict[str, ModelRouter]):
        """Initialize with available ModelRouter instances"""
        self.agent_routers = agent_routers
        self.quality_validator = QualityValidator()
        
    async def execute(self, task: OrchestrationTask) -> OrchestrationResult:
        """
        Execute task using collaborative strategy
        
        All agents attempt same task, best quality result is selected
        """
        start_time = datetime.now()
        
        collaborative_results = {}
        agents_used = []
        quality_scores = {}
        
        # Execute same task with multiple agents/models
        for router_name, router in self.agent_routers.items():
            try:
                # Each agent attempts the full task
                agent_result = await self._execute_with_agent(router_name, router, task)
                collaborative_results[router_name] = agent_result
                agents_used.append(router_name)
                
                # Calculate quality score for this result
                quality_score = await self._assess_result_quality(agent_result, task)
                quality_scores[router_name] = quality_score
                
                # Add quality score to result
                agent_result["quality_score"] = quality_score
                
            except Exception as e:
                collaborative_results[router_name] = {
                    "status": "failed",
                    "error": str(e),
                    "quality_score": 0.0
                }
                quality_scores[router_name] = 0.0
        
        # Select best result based on quality scores
        if quality_scores:
            best_agent = max(quality_scores.items(), key=lambda x: x[1])
            best_agent_name, best_quality = best_agent
            best_result = collaborative_results[best_agent_name]
        else:
            # Fallback if no quality scores available
            best_agent_name = list(collaborative_results.keys())[0] if collaborative_results else "none"
            best_quality = 0.0
            best_result = collaborative_results.get(best_agent_name, {"status": "failed"})
        
        # Calculate execution metrics
        execution_time = (datetime.now() - start_time).total_seconds()
        
        # Calculate coordination efficiency (how many agents succeeded)
        successful_agents = [
            name for name, result in collaborative_results.items() 
            if result.get("status") == "completed"
        ]
        coordination_efficiency = len(successful_agents) / len(collaborative_results) if collaborative_results else 0.0
        
        # Aggregate results with best result highlighted
        final_results = {
            "best_result": {
                "agent": best_agent_name,
                "quality_score": best_quality,
                "result": best_result
            },
            "all_results": collaborative_results,
            "quality_comparison": quality_scores,
            "consensus_analysis": self._analyze_consensus(collaborative_results)
        }
        
        # Determine overall status
        if best_result.get("status") == "completed":
            status = "completed"
        elif any(r.get("status") == "completed" for r in collaborative_results.values()):
            status = "partial"  # At least one agent succeeded
        else:
            status = "failed"
        
        return OrchestrationResult(
            task_id=task.task_id,
            status=status,
            results=final_results,
            execution_time=execution_time,
            quality_score=best_quality,
            coordination_efficiency=coordination_efficiency,
            agents_used=agents_used,
            metadata={
                "collaboration_type": "competitive",
                "agents_count": len(collaborative_results),
                "successful_agents": len(successful_agents),
                "quality_variance": self._calculate_quality_variance(quality_scores),
                "best_agent": best_agent_name
            }
        )
    
    async def _execute_with_agent(self, router_name: str, router: ModelRouter, task: OrchestrationTask) -> Dict[str, Any]:
        """Execute task with single agent"""
        try:
            # Route task using existing TaskRouter logic
            routing_decision = await router.route_task(
                query=task.query,
                context=task.context,
                model_preference=ModelChoice.AUTO
            )
            
            # Execute with selected model
            execution_result = await router.execute_with_model(
                query=task.query,
                model_choice=routing_decision.selected_model,
                context=task.context
            )
            
            return {
                "status": "completed",
                "router": router_name,
                "result": execution_result,
                "routing_decision": {
                    "selected_model": routing_decision.selected_model.value,
                    "reasoning": routing_decision.reasoning,
                    "confidence_score": routing_decision.confidence_score
                }
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "router": router_name,
                "error": str(e)
            }
    
    async def _assess_result_quality(self, agent_result: Dict[str, Any], task: OrchestrationTask) -> float:
        """Assess quality of agent result using QualityValidator"""
        try:
            if agent_result.get("status") != "completed":
                return 0.0
            
            result_data = agent_result.get("result", {})
            result_content = result_data.get("result", "") if isinstance(result_data, dict) else str(result_data)
            
            # Use existing QualityValidator from Epic 5
            quality_result = self.quality_validator.validate_output(result_content, "text")
            
            if quality_result and hasattr(quality_result, 'overall_score'):
                return float(quality_result.overall_score)
            else:
                # Fallback quality assessment
                return self._basic_quality_assessment(result_content, task)
            
        except Exception:
            return 0.0
    
    def _basic_quality_assessment(self, content: str, task: OrchestrationTask) -> float:
        """Basic quality assessment fallback"""
        if not content or not isinstance(content, str):
            return 0.0
        
        score = 0.0
        content_lower = content.lower()
        task_lower = task.query.lower()
        
        # Length check (reasonable response length)
        if 50 <= len(content) <= 5000:
            score += 0.3
        elif len(content) > 20:
            score += 0.1
        
        # Relevance check (task keywords in response)
        task_words = set(word for word in task_lower.split() if len(word) > 3)
        content_words = set(word for word in content_lower.split() if len(word) > 3)
        relevance = len(task_words & content_words) / len(task_words) if task_words else 0.0
        score += relevance * 0.4
        
        # Structure check (has proper formatting)
        if any(marker in content for marker in ['\n', '.', ':', '-', '*']):
            score += 0.2
        
        # Completeness check (doesn't end abruptly)
        if content.strip().endswith(('.', '!', '?', '```', ')')):
            score += 0.1
        
        return min(score, 1.0)
    
    def _analyze_consensus(self, collaborative_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze consensus between agent results"""
        successful_results = [
            result for result in collaborative_results.values()
            if result.get("status") == "completed"
        ]
        
        if len(successful_results) < 2:
            return {"consensus": "insufficient_data", "agreement_level": 0.0}
        
        # Extract result contents for comparison
        contents = []
        for result in successful_results:
            result_data = result.get("result", {})
            content = result_data.get("result", "") if isinstance(result_data, dict) else str(result_data)
            contents.append(content.lower())
        
        # Simple consensus analysis based on common words
        if len(contents) >= 2:
            # Calculate word overlap between results
            all_words = [set(content.split()) for content in contents]
            if all_words:
                common_words = set.intersection(*all_words)
                total_unique_words = len(set.union(*all_words))
                agreement_level = len(common_words) / total_unique_words if total_unique_words > 0 else 0.0
            else:
                agreement_level = 0.0
        else:
            agreement_level = 0.0
        
        consensus_level = "high" if agreement_level > 0.7 else "medium" if agreement_level > 0.4 else "low"
        
        return {
            "consensus": consensus_level,
            "agreement_level": agreement_level,
            "agents_agreeing": len(successful_results),
            "common_themes": len(common_words) if 'common_words' in locals() else 0
        }
    
    def _calculate_quality_variance(self, quality_scores: Dict[str, float]) -> float:
        """Calculate variance in quality scores across agents"""
        if not quality_scores:
            return 0.0
        
        scores = list(quality_scores.values())
        if len(scores) < 2:
            return 0.0
        
        mean_score = sum(scores) / len(scores)
        variance = sum((score - mean_score) ** 2 for score in scores) / len(scores)
        return variance 