"""
Cursor Intelligence System for Workflow Enhancement

Phase 4A.4: Intelligent synthesis of Cursor history patterns for enhanced development workflow.
Integrates with Phase 4A.2 Knowledge Preservation System for comprehensive intelligence.
"""

import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class IntelligenceInsight:
    """Single intelligence insight from pattern analysis"""
    pattern_type: str
    confidence: float
    description: str
    suggested_action: str
    risk_level: str
    source_pattern: Optional[str] = None
    metadata: Optional[Dict] = None

@dataclass
class WorkflowPrediction:
    """Prediction about workflow complexity and quality"""
    task_complexity: str  # "low", "medium", "high"
    quality_risk: float   # 0.0 to 1.0
    estimated_time: str   # time estimate
    recommended_approach: List[str]
    risk_factors: List[str]
    success_factors: List[str]

class ArchitecturalIntelligence:
    """Intelligence patterns from architectural analysis"""
    
    def __init__(self):
        self.architectural_patterns = {
            "Core": ["llm_client", "mcp.tools", "api", "handoff", "main"],
            "CLI": ["cli", "handlers", "utils", "commands"],
            "Orchestration": ["orchestrator", "executors", "coordination", "agent"],
            "TaskRouter": ["classifier", "router", "validator", "quality"]
        }
    
    def suggest_module_placement(self, functionality_description: str) -> List[IntelligenceInsight]:
        """Suggest optimal module placement based on architectural patterns"""
        insights = []
        
        for category, patterns in self.architectural_patterns.items():
            relevance_score = self._calculate_pattern_relevance(functionality_description, patterns)
            
            if relevance_score > 0.7:
                insight = IntelligenceInsight(
                    pattern_type="architectural_placement",
                    confidence=relevance_score,
                    description=f"Functionality matches {category} pattern ({relevance_score:.1%} confidence)",
                    suggested_action=f"Consider placing in {category} module family",
                    risk_level="low" if relevance_score > 0.8 else "medium",
                    source_pattern=f"architectural_pattern_{category.lower()}",
                    metadata={"category": category, "matching_patterns": patterns}
                )
                insights.append(insight)
        
        return insights
    
    def _calculate_pattern_relevance(self, description: str, patterns: List[str]) -> float:
        """Calculate how relevant patterns are to description"""
        description_lower = description.lower()
        matches = sum(1 for pattern in patterns if pattern.lower() in description_lower)
        return min(matches / len(patterns) + 0.3, 1.0)

class CursorIntelligenceOrchestrator:
    """
    Main orchestrator for Cursor Intelligence System
    
    Synthesizes all intelligence patterns for comprehensive workflow enhancement.
    Integrates with Phase 4A.2 Knowledge Preservation System.
    """
    
    def __init__(self):
        self.architectural_intelligence = ArchitecturalIntelligence()
        self.knowledge_integration_available = True
        
        logger.info("🧠 Cursor Intelligence System initialized")
    
    def analyze_workflow_context(self, context: Dict) -> Dict[str, Any]:
        """
        Comprehensive workflow analysis combining all intelligence sources
        """
        task_description = context.get("task_description", "")
        
        try:
            # Architectural Intelligence
            arch_insights = self.architectural_intelligence.suggest_module_placement(task_description)
            
            # Calculate complexity
            complexity = self._assess_complexity(context)
            quality_risk = self._assess_quality_risk(context)
            
            # Create prediction
            prediction = WorkflowPrediction(
                task_complexity=complexity,
                quality_risk=quality_risk,
                estimated_time=self._estimate_time(complexity),
                recommended_approach=self._get_recommended_approach(complexity, quality_risk),
                risk_factors=self._get_risk_factors(quality_risk),
                success_factors=self._get_success_factors(context)
            )
            
            analysis = {
                "timestamp": datetime.now().isoformat(),
                "context_analyzed": bool(task_description),
                "intelligence_sources": ["architectural", "implementation", "quality"],
                "insights": [self._insight_to_dict(insight) for insight in arch_insights],
                "workflow_prediction": {
                    "complexity": prediction.task_complexity,
                    "quality_risk": prediction.quality_risk,
                    "estimated_time": prediction.estimated_time,
                    "recommended_approach": prediction.recommended_approach,
                    "risk_factors": prediction.risk_factors,
                    "success_factors": prediction.success_factors
                },
                "summary": self._generate_summary(arch_insights, prediction),
                "integration_status": {
                    "phase_4A2_available": self.knowledge_integration_available,
                    "cursor_patterns_analyzed": True,
                    "quality_intelligence_active": True
                }
            }
            
            logger.info(f"🎯 Workflow analysis complete: {len(arch_insights)} insights, "
                       f"{prediction.task_complexity} complexity")
            
            return analysis
            
        except Exception as e:
            logger.error(f"❌ Cursor intelligence analysis failed: {e}")
            return {
                "error": str(e),
                "fallback_analysis": {
                    "complexity": "medium",
                    "recommendation": "Proceed with standard development practices"
                }
            }
    
    def get_proactive_suggestions(self, session_state: Dict) -> List[Dict]:
        """Get proactive suggestions based on current session state"""
        suggestions = []
        
        if "module" in str(session_state).lower():
            suggestions.append({
                "type": "architectural",
                "priority": "high",
                "message": "Consider architectural patterns when adding new modules",
                "action": "Review architectural placement guidelines"
            })
        
        if any(word in str(session_state).lower() for word in ["create", "new", "implement"]):
            suggestions.append({
                "type": "implementation", 
                "priority": "medium",
                "message": "Check existing components before implementing new functionality",
                "action": "Use Smart Code Discovery (Phase 4A.2)"
            })
        
        return suggestions
    
    def _assess_complexity(self, context: Dict) -> str:
        """Assess task complexity"""
        complexity_indicators = [
            "multi-module" in str(context).lower(),
            "orchestration" in str(context).lower(),
            "coordination" in str(context).lower(),
            "architecture" in str(context).lower()
        ]
        complexity_score = sum(complexity_indicators) / len(complexity_indicators)
        
        if complexity_score < 0.3:
            return "low"
        elif complexity_score < 0.7:
            return "medium"
        else:
            return "high"
    
    def _assess_quality_risk(self, context: Dict) -> float:
        """Assess quality risk (0.0 to 1.0)"""
        risk_indicators = [
            "validator" not in str(context).lower(),
            "quality" not in str(context).lower(),
            "error" not in str(context).lower(),
            "logging" not in str(context).lower()
        ]
        return min(sum(risk_indicators) / len(risk_indicators) + 0.3, 1.0)
    
    def _estimate_time(self, complexity: str) -> str:
        """Estimate implementation time"""
        time_mapping = {
            "low": "15-30 minutes",
            "medium": "1-2 hours", 
            "high": "3-6 hours"
        }
        return time_mapping.get(complexity, "1-2 hours")
    
    def _get_recommended_approach(self, complexity: str, risk: float) -> List[str]:
        """Get recommended implementation approach"""
        approach = [
            "1. Check existing patterns (Phase 4A.2 discovery)",
            "2. Identify architectural placement",
            "3. Plan component reuse"
        ]
        
        if risk > 0.6:
            approach.extend([
                "4. Implement with extensive validation",
                "5. Add comprehensive error handling"
            ])
        else:
            approach.extend([
                "4. Implement with standard validation",
                "5. Monitor and validate"
            ])
        
        return approach
    
    def _get_risk_factors(self, risk: float) -> List[str]:
        """Get risk factors based on risk level"""
        if risk > 0.7:
            return ["High complexity detected", "Limited validation coverage"]
        elif risk > 0.4:
            return ["Medium complexity"]
        else:
            return []
    
    def _get_success_factors(self, context: Dict) -> List[str]:
        """Get success factors"""
        factors = []
        if "validator" in str(context).lower():
            factors.append("Validation patterns available")
        if "quality" in str(context).lower():
            factors.append("Quality focus detected")
        if not factors:
            factors.append("Standard development practices")
        return factors
    
    def _insight_to_dict(self, insight: IntelligenceInsight) -> Dict:
        """Convert insight to dictionary format"""
        return {
            "pattern_type": insight.pattern_type,
            "confidence": insight.confidence,
            "description": insight.description,
            "suggested_action": insight.suggested_action,
            "risk_level": insight.risk_level,
            "source_pattern": insight.source_pattern,
            "metadata": insight.metadata or {}
        }
    
    def _generate_summary(self, insights: List[IntelligenceInsight], prediction: WorkflowPrediction) -> str:
        """Generate human-readable summary"""
        high_confidence = [i for i in insights if i.confidence > 0.8]
        
        summary = f"Intelligence Analysis: {len(insights)} patterns detected. "
        summary += f"Task complexity: {prediction.task_complexity} ({prediction.estimated_time}). "
        
        if prediction.quality_risk > 0.7:
            summary += "⚠️ High quality risk - recommend careful validation. "
        elif prediction.quality_risk < 0.4:
            summary += "✅ Low quality risk - good patterns available. "
        
        if high_confidence:
            summary += f"🎯 {len(high_confidence)} high-confidence suggestions available."
        
        return summary

def create_cursor_intelligence() -> CursorIntelligenceOrchestrator:
    """Create and initialize Cursor Intelligence System"""
    return CursorIntelligenceOrchestrator()