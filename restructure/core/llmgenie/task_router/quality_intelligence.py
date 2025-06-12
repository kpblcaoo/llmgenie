"""
Quality Intelligence System for Smart LLM Routing

Provides feedback loop mechanism for continuous improvement of routing decisions
Based on Phase 2D architecture design - lightweight implementation for production use
"""

import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
from collections import defaultdict, deque

from .task_classifier import TaskType
from .quality_validator import QualityResult


@dataclass
class ExecutionResult:
    """Record of a single task execution for quality intelligence"""
    task_id: str
    timestamp: datetime
    query: str
    task_type: TaskType
    routing_decision: Any  # RoutingDecision - avoiding circular import
    quality_result: QualityResult
    execution_time: float
    success: bool
    user_feedback: Optional[float] = None  # 0-1 user satisfaction score


@dataclass
class PerformanceReport:
    """Analysis report of model performance trends"""
    model_choice: Any  # ModelChoice - avoiding circular import
    task_type: TaskType
    avg_quality_score: float
    avg_execution_time: float
    success_rate: float
    sample_size: int
    trend_direction: str  # "improving", "declining", "stable"
    confidence: float


@dataclass
class RoutingRecommendation:
    """Recommendation for improving routing decisions"""
    task_type: TaskType
    current_model: Any  # ModelChoice - avoiding circular import
    recommended_model: Any  # ModelChoice - avoiding circular import
    reason: str
    confidence: float
    expected_improvement: float


class QualityIntelligence:
    """
    Quality Intelligence System for continuous routing improvement
    
    Lightweight implementation focusing on:
    - Execution result tracking
    - Performance trend analysis  
    - Routing improvement recommendations
    - Adaptive threshold management
    """
    
    def __init__(self, data_dir: str = "data/quality_intelligence"):
        """Initialize quality intelligence with data persistence"""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # In-memory storage for recent results (performance optimization)
        self.recent_results = deque(maxlen=1000)  # Last 1000 executions
        
        # Performance tracking by model and task type
        self.performance_metrics = defaultdict(lambda: defaultdict(list))
        
        # Load existing data
        self._load_historical_data()
    
    def record_execution_result(self, task_id: str, routing_decision: Any, 
                              quality_result: QualityResult, execution_time: float,
                              query: str, task_type: TaskType, success: bool = True,
                              user_feedback: Optional[float] = None) -> None:
        """
        Record execution result for quality intelligence analysis
        
        Args:
            task_id: Unique identifier for the task
            routing_decision: The routing decision that was made
            quality_result: Result of quality validation
            execution_time: Time taken for execution in seconds
            query: Original query text
            task_type: Type of task executed
            success: Whether execution was successful
            user_feedback: Optional user satisfaction score (0-1)
        """
        
        result = ExecutionResult(
            task_id=task_id,
            timestamp=datetime.now(),
            query=query,
            task_type=task_type,
            routing_decision=routing_decision,
            quality_result=quality_result,
            execution_time=execution_time,
            success=success,
            user_feedback=user_feedback
        )
        
        # Add to recent results
        self.recent_results.append(result)
        
        # Update performance metrics
        model_key = routing_decision.selected_model
        task_key = task_type
        
        self.performance_metrics[model_key][task_key].append({
            "quality_score": quality_result.score.value,
            "execution_time": execution_time,
            "success": success,
            "timestamp": result.timestamp.isoformat(),
            "user_feedback": user_feedback
        })
        
        # Persist to disk (async in production)
        self._persist_result(result)
    
    def analyze_model_performance_trends(self, 
                                       model_choice: Optional[Any] = None,
                                       task_type: Optional[TaskType] = None,
                                       days_back: int = 30) -> List[PerformanceReport]:
        """
        Analyze performance trends for models and task types
        
        Args:
            model_choice: Specific model to analyze (None for all)
            task_type: Specific task type to analyze (None for all)
            days_back: Number of days to look back for analysis
            
        Returns:
            List of performance reports
        """
        
        cutoff_date = datetime.now() - timedelta(days=days_back)
        reports = []
        
        # Filter models and task types to analyze
        models_to_analyze = [model_choice] if model_choice else list(self.performance_metrics.keys())
        
        for model in models_to_analyze:
            if model not in self.performance_metrics:
                continue
                
            task_types_to_analyze = [task_type] if task_type else list(self.performance_metrics[model].keys())
            
            for task in task_types_to_analyze:
                if task not in self.performance_metrics[model]:
                    continue
                    
                # Filter recent data
                recent_data = [
                    entry for entry in self.performance_metrics[model][task]
                    if datetime.fromisoformat(entry["timestamp"]) >= cutoff_date
                ]
                
                if len(recent_data) < 5:  # Need minimum sample size
                    continue
                
                # Calculate metrics
                quality_scores = [entry["quality_score"] for entry in recent_data]
                execution_times = [entry["execution_time"] for entry in recent_data]
                successes = [entry["success"] for entry in recent_data]
                
                avg_quality = sum(quality_scores) / len(quality_scores)
                avg_time = sum(execution_times) / len(execution_times)
                success_rate = sum(successes) / len(successes)
                
                # Calculate trend (simple linear approximation)
                trend_direction = self._calculate_trend(quality_scores)
                confidence = min(1.0, len(recent_data) / 50.0)  # More data = higher confidence
                
                report = PerformanceReport(
                    model_choice=model,
                    task_type=task,
                    avg_quality_score=avg_quality,
                    avg_execution_time=avg_time,
                    success_rate=success_rate,
                    sample_size=len(recent_data),
                    trend_direction=trend_direction,
                    confidence=confidence
                )
                
                reports.append(report)
        
        return sorted(reports, key=lambda x: x.confidence, reverse=True)
    
    def suggest_routing_improvements(self, min_confidence: float = 0.7) -> List[RoutingRecommendation]:
        """
        Suggest routing improvements based on performance analysis
        
        Args:
            min_confidence: Minimum confidence threshold for recommendations
            
        Returns:
            List of routing recommendations
        """
        
        recommendations = []
        performance_reports = self.analyze_model_performance_trends()
        
        # Group reports by task type for comparison
        task_reports = defaultdict(list)
        for report in performance_reports:
            if report.confidence >= min_confidence:
                task_reports[report.task_type].append(report)
        
        # Find improvement opportunities
        for task_type, reports in task_reports.items():
            if len(reports) < 2:  # Need at least 2 models to compare
                continue
                
            # Sort by quality score
            reports.sort(key=lambda x: x.avg_quality_score, reverse=True)
            best_report = reports[0]
            
            # Check if current routing choices are suboptimal
            for report in reports[1:]:
                if (best_report.avg_quality_score - report.avg_quality_score) > 0.1:  # Significant difference
                    
                    expected_improvement = best_report.avg_quality_score - report.avg_quality_score
                    confidence = min(best_report.confidence, report.confidence)
                    
                    recommendation = RoutingRecommendation(
                        task_type=task_type,
                        current_model=report.model_choice,
                        recommended_model=best_report.model_choice,
                        reason=f"Quality improvement: {report.avg_quality_score:.2f} → {best_report.avg_quality_score:.2f}",
                        confidence=confidence,
                        expected_improvement=expected_improvement
                    )
                    
                    recommendations.append(recommendation)
        
        return sorted(recommendations, key=lambda x: x.expected_improvement, reverse=True)
    
    def update_quality_thresholds(self, task_type: TaskType, 
                                performance_data: Optional[List[ExecutionResult]] = None) -> Dict[str, float]:
        """
        Update quality thresholds based on performance data
        
        Args:
            task_type: Task type to update thresholds for
            performance_data: Optional specific performance data (uses recent if None)
            
        Returns:
            Updated threshold recommendations
        """
        
        if performance_data is None:
            # Use recent results for this task type
            performance_data = [
                result for result in self.recent_results
                if result.task_type == task_type and result.success
            ]
        
        if len(performance_data) < 10:  # Need minimum data
            return {"error": "Insufficient data for threshold adjustment"}
        
        # Calculate statistics
        quality_scores = [result.quality_result.score.value for result in performance_data]
        user_feedback = [result.user_feedback for result in performance_data if result.user_feedback is not None]
        
        # Calculate adaptive thresholds
        avg_quality = sum(quality_scores) / len(quality_scores)
        quality_std = (sum((x - avg_quality) ** 2 for x in quality_scores) / len(quality_scores)) ** 0.5
        
        # Conservative threshold: average minus one standard deviation
        conservative_threshold = max(0.5, avg_quality - quality_std)
        
        # Aggressive threshold: average quality
        aggressive_threshold = min(0.95, avg_quality)
        
        # User-feedback adjusted (if available)
        if user_feedback:
            avg_user_feedback = sum(user_feedback) / len(user_feedback)
            user_adjusted_threshold = min(aggressive_threshold, avg_quality * avg_user_feedback)
        else:
            user_adjusted_threshold = aggressive_threshold
        
        return {
            "conservative_threshold": conservative_threshold,
            "aggressive_threshold": aggressive_threshold,
            "user_adjusted_threshold": user_adjusted_threshold,
            "current_average": avg_quality,
            "sample_size": len(performance_data)
        }
    
    def _load_historical_data(self) -> None:
        """Load historical performance data from disk"""
        try:
            data_file = self.data_dir / "performance_metrics.json"
            if data_file.exists():
                with open(data_file, 'r') as f:
                    data = json.load(f)
                                    # Restore performance metrics
                for model_str, task_data in data.get("performance_metrics", {}).items():
                    # Use string key instead of enum to avoid circular import
                    for task_str, entries in task_data.items():
                        task = TaskType(task_str)
                        self.performance_metrics[model_str][task] = entries
        except Exception as e:
            print(f"Warning: Could not load historical data: {e}")
    
    def _persist_result(self, result: ExecutionResult) -> None:
        """Persist execution result to disk"""
        try:
            result_file = self.data_dir / f"execution_results_{datetime.now().strftime('%Y%m')}.jsonl"
            with open(result_file, 'a') as f:
                # Convert dataclass to dict for JSON serialization
                result_dict = asdict(result)
                result_dict["timestamp"] = result.timestamp.isoformat()
                result_dict["task_type"] = result.task_type.value
                result_dict["routing_decision"]["selected_model"] = result.routing_decision.selected_model.value
                if result.routing_decision.fallback_model:
                    result_dict["routing_decision"]["fallback_model"] = result.routing_decision.fallback_model.value
                result_dict["quality_result"]["score"] = result.quality_result.score.value
                
                f.write(json.dumps(result_dict) + "\n")
        except Exception as e:
            print(f"Warning: Could not persist result: {e}")
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction from list of values"""
        if len(values) < 3:
            return "stable"
            
        # Simple linear trend calculation
        n = len(values)
        x_sum = sum(range(n))
        y_sum = sum(values)
        xy_sum = sum(i * values[i] for i in range(n))
        x2_sum = sum(i * i for i in range(n))
        
        slope = (n * xy_sum - x_sum * y_sum) / (n * x2_sum - x_sum * x_sum)
        
        if slope > 0.05:
            return "improving"
        elif slope < -0.05:
            return "declining"
        else:
            return "stable"
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics for monitoring dashboard"""
        
        total_executions = len(self.recent_results)
        if total_executions == 0:
            return {"total_executions": 0, "status": "no_data"}
        
        recent_successes = sum(1 for r in self.recent_results if r.success)
        success_rate = recent_successes / total_executions
        
        avg_quality = sum(r.quality_result.score.value for r in self.recent_results) / total_executions
        avg_execution_time = sum(r.execution_time for r in self.recent_results) / total_executions
        
        # Model usage distribution
        model_usage = defaultdict(int)
        for result in self.recent_results:
            model_usage[result.routing_decision.selected_model.value] += 1
        
        return {
            "total_executions": total_executions,
            "success_rate": success_rate,
            "avg_quality_score": avg_quality,
            "avg_execution_time": avg_execution_time,
            "model_usage_distribution": dict(model_usage),
            "data_freshness": datetime.now().isoformat()
        } 