"""
Task Classification Engine for Smart LLM Routing

Based on Epic 5 research findings:
- Code generation patterns → Ollama preference
- Documentation patterns → Ollama preference  
- Complex reasoning patterns → Claude preference
- Mixed complexity handling → Smart routing
"""

from enum import Enum
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import re


class TaskType(Enum):
    """Task classification types based on Epic 5 research"""
    CODE_GENERATION = "code_generation"
    CODE_REVIEW = "code_review" 
    DOCUMENTATION = "documentation"
    DEBUGGING = "debugging"
    ARCHITECTURE_PLANNING = "architecture_planning"
    COMPLEX_REASONING = "complex_reasoning"
    SIMPLE_QUERY = "simple_query"
    REFACTORING = "refactoring"


class ComplexityLevel(Enum):
    """Task complexity levels for routing decisions"""
    SIMPLE = 1      # Routine tasks, patterns, straightforward logic
    MODERATE = 2    # Some analysis required, multiple steps
    COMPLEX = 3     # Deep reasoning, architecture decisions
    CRITICAL = 4    # Mission-critical, requires highest accuracy


@dataclass
class ClassificationResult:
    """Result of task classification analysis"""
    task_type: TaskType
    complexity_level: ComplexityLevel
    confidence_score: float
    reasoning: str
    ollama_preference: bool
    claude_preference: bool


class TaskClassifier:
    """
    Smart Task Classifier for LLM routing decisions
    
    Integrates with existing AgentRequest pattern from main.py:98-112
    """
    
    def __init__(self):
        """Initialize classifier with Epic 5 research patterns"""
        self.code_patterns = [
            r'def\s+\w+', r'class\s+\w+', r'import\s+\w+',
            r'function\s*\(', r'const\s+\w+', r'var\s+\w+',
            r'git\s+\w+', r'npm\s+\w+', r'pip\s+install'
        ]
        
        self.documentation_patterns = [
            r'readme', r'documentation', r'docs?/', r'\.md$',
            r'explain', r'describe', r'document', r'comment'
        ]
        
        self.architecture_patterns = [
            r'architecture', r'design', r'system', r'structure',
            r'microservice', r'database', r'api', r'integration'
        ]
        
        self.complexity_indicators = {
            'simple': ['fix', 'format', 'rename', 'delete', 'add'],
            'moderate': ['refactor', 'optimize', 'implement', 'create'], 
            'complex': ['design', 'architect', 'analyze', 'solve'],
            'critical': ['migrate', 'security', 'performance', 'scale']
        }

    def classify_task(self, query: str, context: Optional[Dict] = None) -> ClassificationResult:
        """
        Classify task based on Epic 5 research patterns
        
        Args:
            query: User request/task description
            context: Optional context (file types, project info, etc.)
            
        Returns:
            ClassificationResult with routing recommendation
        """
        query_lower = query.lower()
        
        # Determine task type
        task_type = self._determine_task_type(query_lower, context)
        
        # Calculate complexity
        complexity_level = self._calculate_complexity(query_lower, context)
        
        # Get routing preferences based on Epic 5 findings
        ollama_pref, claude_pref = self._get_routing_preferences(task_type, complexity_level)
        
        # Calculate confidence
        confidence = self._calculate_confidence(query, task_type, complexity_level)
        
        # Generate reasoning
        reasoning = self._generate_reasoning(task_type, complexity_level, ollama_pref, claude_pref)
        
        return ClassificationResult(
            task_type=task_type,
            complexity_level=complexity_level,
            confidence_score=confidence,
            reasoning=reasoning,
            ollama_preference=ollama_pref,
            claude_preference=claude_pref
        )

    def _determine_task_type(self, query: str, context: Optional[Dict]) -> TaskType:
        """Determine primary task type from query content"""
        
        # Code generation indicators
        if any(re.search(pattern, query) for pattern in self.code_patterns):
            return TaskType.CODE_GENERATION
            
        # Documentation indicators  
        if any(re.search(pattern, query) for pattern in self.documentation_patterns):
            return TaskType.DOCUMENTATION
            
        # Architecture indicators
        if any(re.search(pattern, query) for pattern in self.architecture_patterns):
            return TaskType.ARCHITECTURE_PLANNING
            
        # Context-based detection
        if context:
            file_types = context.get('file_types', [])
            if any(ft in ['.py', '.js', '.ts', '.java', '.cpp'] for ft in file_types):
                return TaskType.CODE_GENERATION
                
        # Default classification based on keywords
        if any(word in query for word in ['debug', 'error', 'fix', 'bug']):
            return TaskType.DEBUGGING
        elif any(word in query for word in ['review', 'check', 'validate']):
            return TaskType.CODE_REVIEW
        elif any(word in query for word in ['refactor', 'improve', 'optimize']):
            return TaskType.REFACTORING
        else:
            return TaskType.SIMPLE_QUERY

    def _calculate_complexity(self, query: str, context: Optional[Dict]) -> ComplexityLevel:
        """Calculate task complexity based on content analysis"""
        
        complexity_score = 0
        
        # Keyword-based scoring - count matches for better accuracy
        for level, keywords in self.complexity_indicators.items():
            matches = sum(1 for keyword in keywords if keyword in query)
            if matches > 0:
                if level == 'simple':
                    complexity_score += matches * 1
                elif level == 'moderate': 
                    complexity_score += matches * 2
                elif level == 'complex':
                    complexity_score += matches * 3
                elif level == 'critical':
                    complexity_score += matches * 4
                    
        # Architecture-specific boost (these are inherently complex)
        if any(pattern in query for pattern in ['architecture', 'microservice', 'system', 'distributed']):
            complexity_score += 2
                    
        # Length-based scoring (longer queries often more complex)
        if len(query.split()) > 50:
            complexity_score += 1
        if len(query.split()) > 100:
            complexity_score += 1
            
        # Context-based scoring
        if context:
            if context.get('file_count', 0) > 10:
                complexity_score += 1
            if context.get('dependencies', []):
                complexity_score += 1
                
        # Map score to complexity level with adjusted thresholds
        if complexity_score <= 2:
            return ComplexityLevel.SIMPLE
        elif complexity_score <= 4:
            return ComplexityLevel.MODERATE
        elif complexity_score <= 7:  # Increased threshold
            return ComplexityLevel.COMPLEX
        else:
            return ComplexityLevel.CRITICAL

    def _get_routing_preferences(self, task_type: TaskType, complexity: ComplexityLevel) -> Tuple[bool, bool]:
        """
        Get routing preferences based on Epic 5 research findings:
        - Code generation patterns → Ollama preference
        - Documentation patterns → Ollama preference  
        - Complex reasoning patterns → Claude preference
        """
        
        # Ollama preferences (from Epic 5 research)
        ollama_preferred_types = {
            TaskType.CODE_GENERATION,
            TaskType.DOCUMENTATION, 
            TaskType.SIMPLE_QUERY,
            TaskType.DEBUGGING  # For routine debugging
        }
        
        # Claude preferences (complex reasoning)
        claude_preferred_types = {
            TaskType.ARCHITECTURE_PLANNING,
            TaskType.COMPLEX_REASONING,
            TaskType.CODE_REVIEW  # Requires deep analysis
        }
        
        ollama_pref = task_type in ollama_preferred_types and complexity in [ComplexityLevel.SIMPLE, ComplexityLevel.MODERATE]
        claude_pref = task_type in claude_preferred_types or complexity in [ComplexityLevel.COMPLEX, ComplexityLevel.CRITICAL]
        
        return ollama_pref, claude_pref

    def _calculate_confidence(self, query: str, task_type: TaskType, complexity: ComplexityLevel) -> float:
        """Calculate confidence score for classification"""
        
        confidence = 0.5  # Base confidence
        
        # Pattern matching confidence boost
        query_lower = query.lower()
        if any(re.search(pattern, query_lower) for pattern in self.code_patterns):
            confidence += 0.3
        if any(re.search(pattern, query_lower) for pattern in self.documentation_patterns):
            confidence += 0.3
        if any(re.search(pattern, query_lower) for pattern in self.architecture_patterns):
            confidence += 0.3
            
        # Length-based confidence (more content = higher confidence)
        if len(query.split()) > 20:
            confidence += 0.1
        if len(query.split()) > 50:
            confidence += 0.1
            
        return min(confidence, 1.0)

    def _generate_reasoning(self, task_type: TaskType, complexity: ComplexityLevel, 
                          ollama_pref: bool, claude_pref: bool) -> str:
        """Generate human-readable reasoning for classification"""
        
        reasoning_parts = [
            f"Task classified as {task_type.value} with {complexity.name.lower()} complexity."
        ]
        
        if ollama_pref:
            reasoning_parts.append("Ollama preferred: routine task matching established patterns.")
        elif claude_pref:
            reasoning_parts.append("Claude preferred: complex reasoning or critical decision required.")
        else:
            reasoning_parts.append("Mixed complexity: consider hybrid approach or quality validation.")
            
        return " ".join(reasoning_parts)

    def get_complexity_score(self, task_dict: Dict) -> float:
        """
        Get numerical complexity score for external systems
        
        Integrates with existing workflow for performance monitoring
        """
        query = task_dict.get('description', '')
        context = task_dict.get('context', {})
        
        result = self.classify_task(query, context)
        return result.complexity_level.value / 4.0  # Normalize to 0-1 scale 