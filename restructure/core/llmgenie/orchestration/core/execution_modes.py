"""
Execution modes for multi-agent orchestration

Epic 5 Phase 3.1: Multi-Agent Orchestration patterns
Single responsibility: Define execution mode types and behavior
"""

from enum import Enum


class ExecutionMode(Enum):
    """
    Multi-Agent execution patterns from Epic 5 checklist
    
    Based on Epic 5 research findings and checklist requirements:
    - Parallel task execution (documentation + code generation)
    - Sequential handoffs (design → implementation → review)  
    - Collaborative problem solving (multiple models, best result)
    """
    
    PARALLEL = "parallel"
    """
    Parallel task execution pattern
    
    Use case: Multiple independent subtasks executed simultaneously
    Example: Generate code + documentation + tests in parallel
    Benefit: Maximum speed, resource utilization
    """
    
    SEQUENTIAL = "sequential" 
    """
    Sequential handoffs pattern
    
    Use case: Tasks that depend on previous step outputs
    Example: Design → Implementation → Review workflow
    Benefit: Context preservation, logical flow
    """
    
    COLLABORATIVE = "collaborative"
    """
    Collaborative problem solving pattern
    
    Use case: Multiple agents solve same problem, best result selected
    Example: Multiple models generate solution, highest quality chosen  
    Benefit: Quality optimization, redundancy
    """
    
    def get_description(self) -> str:
        """Get human-readable description of execution mode"""
        descriptions = {
            self.PARALLEL: "Execute multiple subtasks simultaneously",
            self.SEQUENTIAL: "Execute tasks in order with context handoffs", 
            self.COLLABORATIVE: "Multiple agents solve same problem, best result selected"
        }
        return descriptions.get(self, "Unknown execution mode")
    
    def get_use_cases(self) -> list[str]:
        """Get typical use cases for this execution mode"""
        use_cases = {
            self.PARALLEL: [
                "Code generation + documentation",
                "Multiple independent analysis tasks",
                "Bulk processing operations"
            ],
            self.SEQUENTIAL: [
                "Design → Implementation → Review",
                "Planning → Execution → Validation", 
                "Multi-step reasoning tasks"
            ],
            self.COLLABORATIVE: [
                "Quality-critical code generation",
                "Complex problem solving",
                "Multiple perspective analysis"
            ]
        }
        return use_cases.get(self, [])
    
    @classmethod
    def suggest_mode(cls, task_description: str) -> 'ExecutionMode':
        """
        Suggest optimal execution mode based on task description
        
        Simple heuristic-based suggestion - can be enhanced with ML
        """
        task_lower = task_description.lower()
        
        # Sequential indicators
        if any(word in task_lower for word in ["design", "implement", "review", "step", "workflow"]):
            return cls.SEQUENTIAL
            
        # Collaborative indicators  
        if any(word in task_lower for word in ["complex", "critical", "important", "best", "optimal"]):
            return cls.COLLABORATIVE
            
        # Parallel indicators (default for multiple independent tasks)
        if any(word in task_lower for word in ["and", "plus", "also", "multiple", "bulk"]):
            return cls.PARALLEL
            
        # Default to parallel for simple tasks
        return cls.PARALLEL 