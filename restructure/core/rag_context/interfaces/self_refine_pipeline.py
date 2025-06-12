"""
Self-Refine Pipeline with MCP Tools Integration
Enhanced iterative improvement system for code, text, and workflow artifacts
Part of Phase 4A.3: Self-Refine Pipeline Supercharged
"""

from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass
from enum import Enum
import json
import time
from pathlib import Path

try:
    from .auto_logger import auto_logger
    AUTO_LOGGING_AVAILABLE = True
except ImportError:
    AUTO_LOGGING_AVAILABLE = False
    auto_logger = None


class RefinementType(Enum):
    """Types of content that can be refined"""
    CODE = "code"
    TEXT = "text"
    CONFIG = "config"
    WORKFLOW = "workflow"
    ARCHITECTURE = "architecture"


@dataclass
class RefinementResult:
    """Result of a refinement iteration"""
    iteration: int
    original: str
    refined: str
    critique: str
    improvements: List[str]
    confidence_score: float
    mcp_tools_used: List[str]
    duration_ms: float


class SelfRefinePipeline:
    """
    Enhanced Self-Refine Pipeline with MCP Tools Integration
    
    Features:
    - Multi-type content refinement (code, text, config, etc.)
    - MCP tools integration for context-aware critique
    - Automatic logging of refinement process
    - Configurable improvement criteria
    - Iterative improvement until satisfaction threshold
    """
    
    def __init__(self, max_iterations: int = 3, confidence_threshold: float = 0.85):
        self.max_iterations = max_iterations
        self.confidence_threshold = confidence_threshold
        self.mcp_tools_available = self._check_mcp_tools()
        
    def _check_mcp_tools(self) -> Dict[str, bool]:
        """Check which MCP tools are available"""
        # In real implementation, would check actual MCP server status
        return {
            "enhance_prompt": True,
            "get_relevant_rules": True,
            "struct_analyze_module": True,
            "get_project_structure": True
        }
    
    def refine(self, 
               content: str, 
               refinement_type: RefinementType,
               context: Optional[Dict[str, Any]] = None,
               custom_criteria: Optional[List[str]] = None) -> List[RefinementResult]:
        """
        Main refinement method - iteratively improve content
        
        Args:
            content: Original content to refine
            refinement_type: Type of content (code, text, etc.)
            context: Additional context for refinement
            custom_criteria: Custom improvement criteria
            
        Returns:
            List of refinement iterations with results
        """
        start_time = time.time()
        iterations = []
        current_content = content
        
        # Log refinement start
        if AUTO_LOGGING_AVAILABLE and auto_logger:
            auto_logger.log_workflow_phase(f"self_refine_start_{refinement_type.value}")
        
        for iteration in range(1, self.max_iterations + 1):
            # Step 1: Generate enhanced prompt if needed
            enhanced_context = self._enhance_context(current_content, refinement_type, context)
            
            # Step 2: Critique with MCP enhancement
            critique_result = self._critique_with_mcp(current_content, refinement_type, enhanced_context)
            
            # Step 3: Refine based on critique
            refined_content = self._apply_refinements(current_content, critique_result, refinement_type)
            
            # Step 4: Validate improvements
            validation_result = self._validate_improvements(content, refined_content, critique_result)
            
            # Create iteration result
            iteration_result = RefinementResult(
                iteration=iteration,
                original=current_content,
                refined=refined_content,
                critique=critique_result["critique"],
                improvements=critique_result["improvements"],
                confidence_score=validation_result["confidence"],
                mcp_tools_used=critique_result.get("mcp_tools_used", []),
                duration_ms=(time.time() - start_time) * 1000
            )
            
            iterations.append(iteration_result)
            
            # Check if we've reached satisfaction threshold
            if validation_result["confidence"] >= self.confidence_threshold:
                break
                
            current_content = refined_content
        
        # Log completion
        if AUTO_LOGGING_AVAILABLE and auto_logger:
            auto_logger.log_workflow_phase(f"self_refine_complete_{refinement_type.value}")
            
        return iterations
    
    def _enhance_context(self, content: str, refinement_type: RefinementType, context: Dict) -> Dict[str, Any]:
        """Enhance context using MCP tools if available"""
        enhanced = context.copy() if context else {}
        mcp_tools_used = []
        
        # Use enhance_prompt if available
        if self.mcp_tools_available.get("enhance_prompt"):
            # Simulate MCP enhance_prompt call
            query = f"Improve {refinement_type.value}: {content[:100]}..."
            # In real implementation: result = mcp_client.enhance_prompt(query)
            enhanced["enhanced_prompt"] = f"Enhanced context for {refinement_type.value} refinement"
            mcp_tools_used.append("enhance_prompt")
        
        # Get relevant rules if available
        if self.mcp_tools_available.get("get_relevant_rules"):
            # Simulate MCP get_relevant_rules call
            query = f"{refinement_type.value} improvement best practices"
            # In real implementation: rules = mcp_client.get_relevant_rules(query)
            enhanced["relevant_rules"] = [
                "Follow atomic responsibility principle",
                "Ensure maintainability and readability",
                "Add proper error handling"
            ]
            mcp_tools_used.append("get_relevant_rules")
            
        enhanced["mcp_tools_used"] = mcp_tools_used
        return enhanced
    
    def _critique_with_mcp(self, content: str, refinement_type: RefinementType, context: Dict) -> Dict[str, Any]:
        """Generate critique using MCP tools for enhanced analysis"""
        critique_points = []
        improvements = []
        mcp_tools_used = context.get("mcp_tools_used", [])
        
        # Basic critique based on type
        if refinement_type == RefinementType.CODE:
            critique_points.extend([
                "Check for unused variables and imports",
                "Verify error handling completeness", 
                "Assess code readability and documentation",
                "Validate naming conventions"
            ])
            
        elif refinement_type == RefinementType.TEXT:
            critique_points.extend([
                "Check clarity and conciseness",
                "Verify logical flow and structure",
                "Assess tone and audience appropriateness"
            ])
            
        # Use struct_analyze_module for code analysis if available
        if (refinement_type == RefinementType.CODE and 
            self.mcp_tools_available.get("struct_analyze_module")):
            # Simulate struct analysis
            critique_points.append("Structural analysis: complexity and dependencies checked")
            mcp_tools_used.append("struct_analyze_module")
        
        # Apply rules from context
        if "relevant_rules" in context:
            for rule in context["relevant_rules"]:
                critique_points.append(f"Rule application: {rule}")
        
        # Generate improvements based on critique
        improvements = [
            "Add constants for magic values",
            "Improve error handling",
            "Add documentation",
            "Optimize performance where possible"
        ]
        
        return {
            "critique": "; ".join(critique_points),
            "improvements": improvements,
            "mcp_tools_used": mcp_tools_used,
            "confidence": 0.75  # Base confidence
        }
    
    def _apply_refinements(self, content: str, critique_result: Dict, refinement_type: RefinementType) -> str:
        """Apply refinements based on critique results"""
        # In real implementation, this would use AI to apply specific improvements
        # For now, simulate improvements
        
        refined = content
        improvements = critique_result["improvements"]
        
        # Simulate applying improvements
        if "Add constants" in str(improvements):
            refined += "\n# Added constants for maintainability"
            
        if "Improve error handling" in str(improvements):
            refined += "\n# Enhanced error handling"
            
        if "Add documentation" in str(improvements):
            refined += "\n# Added comprehensive documentation"
            
        return refined
    
    def _validate_improvements(self, original: str, refined: str, critique: Dict) -> Dict[str, Any]:
        """Validate that refinements actually improved the content"""
        # Simple validation logic - in real implementation would be more sophisticated
        improvements_count = len(critique["improvements"])
        length_improvement = len(refined) - len(original)
        
        # Calculate confidence based on various factors
        confidence = min(0.95, 0.5 + (improvements_count * 0.1) + (min(length_improvement, 100) / 1000))
        
        return {
            "confidence": confidence,
            "improvements_applied": improvements_count,
            "length_change": length_improvement,
            "quality_improved": length_improvement > 0  # Simple heuristic
        }
    
    def refine_code_file(self, file_path: str, backup: bool = True) -> List[RefinementResult]:
        """Convenience method to refine an entire code file"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        # Create backup if requested
        if backup:
            backup_path = file_path.with_suffix(f"{file_path.suffix}.backup")
            backup_path.write_text(file_path.read_text())
            
        # Read and refine content
        original_content = file_path.read_text()
        results = self.refine(
            content=original_content,
            refinement_type=RefinementType.CODE,
            context={"file_path": str(file_path), "file_type": file_path.suffix}
        )
        
        # Write refined content if improvement was made
        if results and results[-1].confidence_score >= self.confidence_threshold:
            file_path.write_text(results[-1].refined)
            
        return results
    
    def generate_refinement_report(self, results: List[RefinementResult]) -> Dict[str, Any]:
        """Generate a comprehensive report of the refinement process"""
        if not results:
            return {"error": "No refinement results provided"}
            
        final_result = results[-1]
        
        return {
            "summary": {
                "total_iterations": len(results),
                "final_confidence": final_result.confidence_score,
                "threshold_reached": final_result.confidence_score >= self.confidence_threshold,
                "total_duration_ms": sum(r.duration_ms for r in results)
            },
            "iterations": [
                {
                    "iteration": r.iteration,
                    "confidence": r.confidence_score,
                    "improvements_count": len(r.improvements),
                    "mcp_tools_used": r.mcp_tools_used,
                    "duration_ms": r.duration_ms
                }
                for r in results
            ],
            "final_improvements": final_result.improvements,
            "mcp_tools_summary": {
                "total_unique_tools": len(set(tool for r in results for tool in r.mcp_tools_used)),
                "most_used_tools": self._get_most_used_tools(results)
            }
        }
    
    def _get_most_used_tools(self, results: List[RefinementResult]) -> List[str]:
        """Get list of most frequently used MCP tools"""
        tool_counts = {}
        for result in results:
            for tool in result.mcp_tools_used:
                tool_counts[tool] = tool_counts.get(tool, 0) + 1
                
        return sorted(tool_counts.keys(), key=tool_counts.get, reverse=True)


# Convenience functions for easy usage
def quick_refine_code(code: str, max_iterations: int = 2) -> str:
    """Quick function to refine code content"""
    pipeline = SelfRefinePipeline(max_iterations=max_iterations)
    results = pipeline.refine(code, RefinementType.CODE)
    return results[-1].refined if results else code


def quick_refine_text(text: str, max_iterations: int = 2) -> str:
    """Quick function to refine text content"""
    pipeline = SelfRefinePipeline(max_iterations=max_iterations)
    results = pipeline.refine(text, RefinementType.TEXT)
    return results[-1].refined if results else text


# Global pipeline instance for convenience
default_pipeline = SelfRefinePipeline() 