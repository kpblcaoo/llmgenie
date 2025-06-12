"""
Agent coordination types for orchestration

Epic 5 Phase 3.1: Agent coordination strategies  
Single responsibility: Define coordination behavior types
"""

from enum import Enum


class AgentCoordination(Enum):
    """
    Agent coordination strategies for multi-agent systems
    
    Defines how agents coordinate and synchronize during task execution
    """
    
    INDEPENDENT = "independent"
    """
    Independent coordination - agents work autonomously
    
    Use case: Parallel tasks with no inter-dependencies
    Benefit: Maximum parallelism, no coordination overhead
    Example: Generate code, docs, and tests independently
    """
    
    SYNCHRONIZED = "synchronized"  
    """
    Synchronized coordination - agents synchronize at checkpoints
    
    Use case: Tasks requiring periodic alignment
    Benefit: Balance between independence and coordination
    Example: Parallel analysis with result aggregation
    """
    
    HIERARCHICAL = "hierarchical"
    """
    Hierarchical coordination - lead agent coordinates others
    
    Use case: Complex workflows requiring central coordination
    Benefit: Clear control flow, centralized decision making
    Example: Lead agent orchestrates specialist agents
    """
    
    def get_description(self) -> str:
        """Get human-readable description of coordination type"""
        descriptions = {
            self.INDEPENDENT: "Agents work autonomously without coordination",
            self.SYNCHRONIZED: "Agents synchronize at defined checkpoints",
            self.HIERARCHICAL: "Lead agent coordinates subordinate agents"
        }
        return descriptions.get(self, "Unknown coordination type")
    
    def get_coordination_overhead(self) -> str:
        """Get expected coordination overhead level"""
        overhead = {
            self.INDEPENDENT: "minimal",
            self.SYNCHRONIZED: "moderate", 
            self.HIERARCHICAL: "high"
        }
        return overhead.get(self, "unknown")
    
    def is_suitable_for_mode(self, execution_mode: 'ExecutionMode') -> bool:
        """Check if coordination type is suitable for execution mode"""
        from .execution_modes import ExecutionMode
        
        # Compatibility matrix
        compatibility = {
            (ExecutionMode.PARALLEL, self.INDEPENDENT): True,
            (ExecutionMode.PARALLEL, self.SYNCHRONIZED): True, 
            (ExecutionMode.PARALLEL, self.HIERARCHICAL): False,
            
            (ExecutionMode.SEQUENTIAL, self.INDEPENDENT): False,
            (ExecutionMode.SEQUENTIAL, self.SYNCHRONIZED): True,
            (ExecutionMode.SEQUENTIAL, self.HIERARCHICAL): True,
            
            (ExecutionMode.COLLABORATIVE, self.INDEPENDENT): True,
            (ExecutionMode.COLLABORATIVE, self.SYNCHRONIZED): True,
            (ExecutionMode.COLLABORATIVE, self.HIERARCHICAL): True,
        }
        
        return compatibility.get((execution_mode, self), False) 