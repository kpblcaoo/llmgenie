"""
Quality Validator for LLM Output Assessment

Enhanced implementation for Epic 5 Phase 2: Quality Validation Pipeline
Provides comprehensive validation for code and text outputs with automatic fallback
"""

import ast
import re
import json
from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any, Optional, List, Tuple
from ..task_router.task_classifier import TaskType


class QualityScore(Enum):
    """Quality assessment levels"""
    EXCELLENT = 5
    GOOD = 4
    ACCEPTABLE = 3
    POOR = 2
    FAILED = 1


@dataclass
class QualityResult:
    """Result of quality validation"""
    score: QualityScore
    confidence: float
    issues: List[str]
    reasoning: str
    metrics: Dict[str, Any]
    needs_fallback: bool = False


class QualityValidator:
    """
    Quality Validator for LLM outputs
    
    Enhanced implementation with real validation logic:
    - Code syntax and structure validation
    - Text coherence and completeness analysis
    - Automatic fallback decision making
    - Quality thresholds based on task type
    """
    
    def __init__(self):
        """Initialize validator with quality rules and thresholds"""
        
        # Quality thresholds by task type (based on Epic 5 research)
        self.quality_thresholds = {
            TaskType.CODE_GENERATION: 0.8,     # High bar for code
            TaskType.CODE_REVIEW: 0.7,         # Medium bar for reviews
            TaskType.DOCUMENTATION: 0.75,      # Good bar for docs
            TaskType.ARCHITECTURE_PLANNING: 0.9,  # Very high bar for architecture
            TaskType.DEBUGGING: 0.8,           # High bar for debugging
            TaskType.REFACTORING: 0.8,         # High bar for refactoring
            TaskType.COMPLEX_REASONING: 0.9    # Very high bar for reasoning
        }
        
        # Text quality patterns
        self.coherence_indicators = [
            r'\b(therefore|thus|hence|consequently)\b',
            r'\b(however|but|although|despite)\b',
            r'\b(first|second|next|finally)\b',
            r'\b(because|since|due to)\b'
        ]
        
        self.completeness_indicators = [
            r'\b(summary|conclusion|result)\b',
            r'\b(example|instance|for instance)\b',
            r'\b(implementation|solution|approach)\b'
        ]
    
    def validate_code_output(self, code: str, language: str = "python") -> QualityResult:
        """
        Validate code output quality with syntax checking and structure analysis
        
        Args:
            code: Code string to validate
            language: Programming language (default: python)
            
        Returns:
            QualityResult with detailed analysis
        """
        issues = []
        metrics = {}
        
        # Basic checks
        if not code.strip():
            return QualityResult(
                score=QualityScore.FAILED,
                confidence=1.0,
                issues=["Empty code output"],
                reasoning="No code provided",
                metrics={},
                needs_fallback=True
            )
        
        # Language-specific validation
        if language.lower() == "python":
            return self._validate_python_code(code)
        elif language.lower() in ["javascript", "typescript"]:
            return self._validate_javascript_code(code)
        else:
            return self._validate_generic_code(code)
    
    def _validate_python_code(self, code: str) -> QualityResult:
        """Validate Python code specifically"""
        issues = []
        metrics = {
            "lines_of_code": len([line for line in code.split('\n') if line.strip()]),
            "has_docstrings": bool(re.search(r'""".*?"""', code, re.DOTALL)),
            "has_comments": '#' in code,
            "function_count": len(re.findall(r'def\s+\w+\(', code)),
            "class_count": len(re.findall(r'class\s+\w+\(', code))
        }
        
        # Syntax validation using AST
        try:
            ast.parse(code)
            syntax_valid = True
        except SyntaxError as e:
            syntax_valid = False
            issues.append(f"Syntax error: {str(e)}")
        except Exception as e:
            syntax_valid = False
            issues.append(f"Parse error: {str(e)}")
        
        # Code quality checks
        if not syntax_valid:
            score = QualityScore.FAILED
            confidence = 0.95
            needs_fallback = True
        else:
            score_value = 3  # Start with ACCEPTABLE
            
            # Bonus points for good practices
            if metrics["has_docstrings"]:
                score_value += 0.5
            if metrics["has_comments"]:
                score_value += 0.3
            if metrics["lines_of_code"] > 0:
                score_value += 0.2
                
            # Penalty for issues
            if metrics["lines_of_code"] < 3:
                issues.append("Very short code output")
                score_value -= 0.5
                
            score = QualityScore(min(5, max(1, round(score_value))))
            confidence = 0.8 if syntax_valid else 0.3
            needs_fallback = score.value < 3
        
        reasoning = f"Python code validation: syntax {'valid' if syntax_valid else 'invalid'}, {metrics['lines_of_code']} LOC"
        if issues:
            reasoning += f", Issues: {', '.join(issues[:2])}"
        
        return QualityResult(
            score=score,
            confidence=confidence,
            issues=issues,
            reasoning=reasoning,
            metrics=metrics,
            needs_fallback=needs_fallback
        )
    
    def _validate_javascript_code(self, code: str) -> QualityResult:
        """Basic JavaScript validation"""
        issues = []
        metrics = {
            "lines_of_code": len([line for line in code.split('\n') if line.strip()]),
            "has_functions": bool(re.search(r'function\s+\w+|=>\s*{|\w+\s*=\s*function', code)),
            "has_comments": '//' in code or '/*' in code,
            "has_semicolons": ';' in code
        }
        
        # Basic syntax checks
        brace_balance = code.count('{') - code.count('}')
        paren_balance = code.count('(') - code.count(')')
        
        if brace_balance != 0:
            issues.append("Unbalanced braces")
        if paren_balance != 0:
            issues.append("Unbalanced parentheses")
            
        score_value = 3
        if not issues:
            score_value += 1
        if metrics["has_functions"]:
            score_value += 0.5
        if metrics["has_comments"]:
            score_value += 0.3
            
        score = QualityScore(min(5, max(1, round(score_value))))
        confidence = 0.7  # Lower confidence without full parser
        needs_fallback = score.value < 3 or bool(issues)
        
        return QualityResult(
            score=score,
            confidence=confidence,
            issues=issues,
            reasoning=f"JavaScript validation: {metrics['lines_of_code']} LOC, {'issues found' if issues else 'basic checks passed'}",
            metrics=metrics,
            needs_fallback=needs_fallback
        )
    
    def _validate_generic_code(self, code: str) -> QualityResult:
        """Generic code validation for unknown languages"""
        issues = []
        metrics = {
            "lines_of_code": len([line for line in code.split('\n') if line.strip()]),
            "has_structure": bool(re.search(r'[{}()\[\]]', code)),
            "char_count": len(code.strip())
        }
        
        score_value = 3  # Default ACCEPTABLE
        
        if metrics["lines_of_code"] < 2:
            issues.append("Very short code output")
            score_value -= 1
        
        if not metrics["has_structure"]:
            issues.append("No apparent code structure")
            score_value -= 0.5
            
        score = QualityScore(min(5, max(1, round(score_value))))
        confidence = 0.5  # Low confidence for generic validation
        needs_fallback = score.value < 3
        
        return QualityResult(
            score=score,
            confidence=confidence,
            issues=issues,
            reasoning=f"Generic code validation: {metrics['lines_of_code']} LOC",
            metrics=metrics,
            needs_fallback=needs_fallback
        )
    
    def validate_text_output(self, text: str, expected_type: str = "general") -> QualityResult:
        """
        Validate text output quality with coherence and completeness analysis
        
        Args:
            text: Text string to validate
            expected_type: Type of text (documentation, explanation, etc.)
            
        Returns:
            QualityResult with detailed analysis
        """
        if not text.strip():
            return QualityResult(
                score=QualityScore.FAILED,
                confidence=1.0,
                issues=["Empty text output"],
                reasoning="No text provided",
                metrics={},
                needs_fallback=True
            )
        
        issues = []
        text_lower = text.lower()
        
        # Calculate metrics
        metrics = {
            "word_count": len(text.split()),
            "sentence_count": len([s for s in text.split('.') if s.strip()]),
            "paragraph_count": len([p for p in text.split('\n\n') if p.strip()]),
            "has_structure": bool(re.search(r'[\n\-\*\d\.]', text)),
            "coherence_score": self._calculate_coherence_score(text_lower),
            "completeness_score": self._calculate_completeness_score(text_lower)
        }
        
        # Quality assessment
        score_value = 3  # Start with ACCEPTABLE
        
        # Length checks
        if metrics["word_count"] < 10:
            issues.append("Very short text output")
            score_value -= 1
        elif metrics["word_count"] > 50:
            score_value += 0.5
            
        # Structure checks
        if metrics["has_structure"]:
            score_value += 0.3
        if metrics["paragraph_count"] > 1:
            score_value += 0.2
            
        # Coherence and completeness
        score_value += metrics["coherence_score"] * 0.8
        score_value += metrics["completeness_score"] * 0.8
        
        # Type-specific validation
        if expected_type == "documentation":
            if not re.search(r'\b(usage|example|api|parameter|return)\b', text_lower):
                issues.append("Missing documentation elements")
                score_value -= 0.5
        elif expected_type == "explanation":
            if not re.search(r'\b(because|reason|why|how|what)\b', text_lower):
                issues.append("Missing explanatory elements")
                score_value -= 0.3
        
        score = QualityScore(min(5, max(1, round(score_value))))
        confidence = min(0.9, 0.6 + (metrics["coherence_score"] + metrics["completeness_score"]) / 2)
        needs_fallback = score.value < 3
        
        reasoning = f"Text validation: {metrics['word_count']} words, coherence={metrics['coherence_score']:.2f}, completeness={metrics['completeness_score']:.2f}"
        if issues:
            reasoning += f", Issues: {', '.join(issues[:2])}"
        
        return QualityResult(
            score=score,
            confidence=confidence,
            issues=issues,
            reasoning=reasoning,
            metrics=metrics,
            needs_fallback=needs_fallback
        )
    
    def _calculate_coherence_score(self, text: str) -> float:
        """Calculate text coherence based on transition words and structure"""
        score = 0.0
        
        # Check for coherence indicators
        for pattern in self.coherence_indicators:
            if re.search(pattern, text):
                score += 0.25
                
        # Penalty for too many repetitive words
        words = text.split()
        if len(words) > 0:
            unique_ratio = len(set(words)) / len(words)
            score += min(0.5, unique_ratio)
        
        return min(1.0, score)
    
    def _calculate_completeness_score(self, text: str) -> float:
        """Calculate text completeness based on structure and content indicators"""
        score = 0.0
        
        # Check for completeness indicators
        for pattern in self.completeness_indicators:
            if re.search(pattern, text):
                score += 0.3
        
        # Check for proper ending
        if text.strip().endswith(('.', '!', '?', ':', '```')):
            score += 0.2
            
        # Check for structured content
        if re.search(r'[\n\-\*\d\.\:]', text):
            score += 0.2
            
        return min(1.0, score)
    
    def should_fallback(self, result: QualityResult, task_type: TaskType) -> bool:
        """
        Determine if we should fallback to a different model based on quality
        
        Args:
            result: Quality validation result
            task_type: Type of task being validated
            
        Returns:
            True if fallback is recommended
        """
        threshold = self.quality_thresholds.get(task_type, 0.7)
        quality_ratio = result.score.value / 5.0  # Normalize to 0-1
        
        # Fallback if below threshold or explicit flag
        return result.needs_fallback or quality_ratio < threshold
    
    def get_quality_metrics(self, result: QualityResult) -> Dict[str, Any]:
        """Extract standardized quality metrics for monitoring"""
        return {
            "quality_score": result.score.value,
            "confidence": result.confidence,
            "issue_count": len(result.issues),
            "needs_fallback": result.needs_fallback,
            "metrics": result.metrics
        } 