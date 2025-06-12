"""Active Knowledge Integration - Phase 4A.2.4 Safe Implementation
Integrates Phase 4A.2.1 (extraction), 4A.2.2 (discovery), 4A.2.3 (context) into active workflow.
"""

import json
import time
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass

from .knowledge_extractor import SafeKnowledgeExtractor
from .code_discovery import SmartCodeDiscovery, DiscoveryResult
from .session_context_manager import SessionContextManager


@dataclass
class KnowledgeSuggestion:
    """Proactive knowledge suggestion for active workflow"""
    suggestion_type: str  # 'similar_solution', 'previous_context', 'pattern_match'
    title: str
    description: str
    relevance_score: float
    action_suggestion: str
    source_info: Dict[str, Any]


@dataclass
class ActiveSessionState:
    """Current active session state for context-aware suggestions"""
    session_id: str
    current_task: str
    problem_type: str
    files_involved: List[str]
    recent_actions: List[str]
    timestamp: float


class ActiveKnowledgeIntegrator:
    """
    Active Knowledge Integration system - the intelligence layer.
    
    Brings together all knowledge preservation components into active workflow:
    - Proactive suggestions during coding
    - "You solved this before" notifications  
    - Auto-tagging of new solutions
    - Smart context switching
    
    Safe design principles:
    - Builds on all previous Phase 4A.2.1-3 components
    - Non-intrusive suggestions (can be ignored)
    - Performance-conscious (fast suggestions)
    - Easy disable without workflow disruption
    """
    
    def __init__(self, 
                 extractor: Optional[SafeKnowledgeExtractor] = None,
                 discovery: Optional[SmartCodeDiscovery] = None,
                 context_manager: Optional[SessionContextManager] = None):
        """Initialize with optional existing components"""
        self.extractor = extractor or SafeKnowledgeExtractor()
        self.discovery = discovery or SmartCodeDiscovery()
        self.context_manager = context_manager or SessionContextManager()
        
        # Integration state
        self.integration_dir = Path("data/knowledge/integration")
        self.integration_dir.mkdir(parents=True, exist_ok=True)
        
        # Active session tracking
        self.current_session: Optional[ActiveSessionState] = None
        self._enabled = True
        self._suggestion_threshold = 0.5  # Minimum relevance for suggestions
        
    def start_active_session(self, task_description: str, 
                           files_involved: List[str] = None) -> Dict[str, Any]:
        """
        Start active knowledge-aware session.
        
        Immediately provides proactive suggestions based on task.
        """
        if not self._enabled:
            return {"enabled": False, "suggestions": []}
        
        try:
            # Create session state
            session_id = f"active_{int(time.time())}"
            self.current_session = ActiveSessionState(
                session_id=session_id,
                current_task=task_description,
                problem_type=self._classify_problem_type(task_description),
                files_involved=files_involved or [],
                recent_actions=[],
                timestamp=time.time()
            )
            
            # Get immediate proactive suggestions
            suggestions = self._generate_proactive_suggestions(task_description)
            
            # Log session start
            self._log_session_event("session_started", {
                "task": task_description,
                "suggestions_count": len(suggestions)
            })
            
            return {
                "enabled": True,
                "session_id": session_id,
                "suggestions": [self._suggestion_to_dict(s) for s in suggestions],
                "status": "active_session_started"
            }
            
        except Exception as e:
            return {"enabled": True, "error": str(e), "suggestions": []}
    
    def get_contextual_suggestions(self, current_code: str, 
                                 current_file: str = None) -> List[KnowledgeSuggestion]:
        """
        Get contextual suggestions based on current coding context.
        
        "You solved this before" type suggestions.
        """
        if not self._enabled or not self.current_session:
            return []
        
        try:
            suggestions = []
            
            # 1. Search for similar code patterns
            if current_code:
                discovery_result = self.discovery.search_solutions(current_code, max_results=3)
                suggestions.extend(self._convert_discovery_to_suggestions(discovery_result))
            
            # 2. Look for similar session contexts
            if self.current_session.problem_type != 'general':
                context_suggestions = self._get_context_based_suggestions(
                    self.current_session.problem_type
                )
                suggestions.extend(context_suggestions)
            
            # 3. File-based suggestions
            if current_file:
                file_suggestions = self._get_file_based_suggestions(current_file)
                suggestions.extend(file_suggestions)
            
            # Filter by relevance and limit
            relevant_suggestions = [s for s in suggestions if s.relevance_score >= self._suggestion_threshold]
            return sorted(relevant_suggestions, key=lambda x: x.relevance_score, reverse=True)[:5]
            
        except Exception:
            return []  # Fail safely
    
    def notify_solution_implemented(self, solution_description: str, 
                                  code_snippet: str = None) -> Dict[str, Any]:
        """
        Notify that a solution was implemented - auto-tag for future discovery.
        """
        if not self._enabled:
            return {"enabled": False}
        
        try:
            # Auto-extract and save this solution for future use
            new_pattern = {
                "pattern_id": f"solution_{int(time.time())}",
                "name": solution_description[:50],
                "description": solution_description,
                "code_snippet": code_snippet or "",
                "use_cases": [self.current_session.problem_type if self.current_session else "general"],
                "source_file": "active_session",
                "session_id": self.current_session.session_id if self.current_session else "unknown",
                "auto_tagged": True,
                "timestamp": time.time()
            }
            
            # Save to knowledge base
            success = self._save_solution_pattern(new_pattern)
            
            # Log the solution
            if self.current_session:
                self.current_session.recent_actions.append(f"Implemented: {solution_description}")
            
            self._log_session_event("solution_implemented", {
                "description": solution_description,
                "auto_tagged": success
            })
            
            return {
                "enabled": True,
                "auto_tagged": success,
                "pattern_id": new_pattern["pattern_id"]
            }
            
        except Exception as e:
            return {"enabled": True, "error": str(e)}
    
    def suggest_related_sessions(self, current_problem: str) -> List[Dict[str, Any]]:
        """
        Suggest related sessions that might have relevant context.
        """
        if not self._enabled:
            return []
        
        try:
            # Get context stats to find related sessions
            context_stats = self.context_manager.get_context_stats()
            
            if not context_stats.get("snapshots_file_exists"):
                return []
            
            # Load session contexts
            snapshots_file = Path("data/sessions/context_snapshots/session_contexts.json")
            with open(snapshots_file, 'r', encoding='utf-8') as f:
                snapshots = json.load(f)
            
            # Find related sessions (simple text matching)
            related_sessions = []
            problem_words = set(current_problem.lower().split())
            
            for snapshot in snapshots:
                description = snapshot.get('description', '').lower()
                problem_type = snapshot.get('problem_type', '')
                
                # Calculate relevance
                description_words = set(description.split())
                overlap = len(problem_words & description_words)
                
                if overlap > 0 or problem_type == self.current_session.problem_type:
                    related_sessions.append({
                        "session_id": snapshot['session_id'],
                        "description": snapshot['description'][:100],
                        "problem_type": problem_type,
                        "relevance": overlap,
                        "restoration_available": bool(snapshot.get('restoration_prompt'))
                    })
            
            # Sort by relevance and return top 3
            related_sessions.sort(key=lambda x: x['relevance'], reverse=True)
            return related_sessions[:3]
            
        except Exception:
            return []
    
    def _generate_proactive_suggestions(self, task_description: str) -> List[KnowledgeSuggestion]:
        """Generate proactive suggestions for a new task"""
        suggestions = []
        
        try:
            # Search existing patterns
            discovery_result = self.discovery.search_solutions(task_description, max_results=3)
            suggestions.extend(self._convert_discovery_to_suggestions(discovery_result))
            
            # Add workflow suggestions based on problem type
            problem_type = self._classify_problem_type(task_description)
            workflow_suggestions = self._get_workflow_suggestions(problem_type)
            suggestions.extend(workflow_suggestions)
            
        except Exception:
            pass  # Fail safely
        
        return suggestions
    
    def _convert_discovery_to_suggestions(self, discovery_result: DiscoveryResult) -> List[KnowledgeSuggestion]:
        """Convert discovery results to knowledge suggestions"""
        suggestions = []
        
        for i, pattern in enumerate(discovery_result.patterns_found):
            score = discovery_result.similarity_scores[i] if i < len(discovery_result.similarity_scores) else 0.5
            
            suggestion = KnowledgeSuggestion(
                suggestion_type="similar_solution",
                title=f"Similar pattern: {pattern.name}",
                description=f"Found similar implementation in {Path(pattern.source_file).name}",
                relevance_score=score / 4.0,  # Normalize to 0-1
                action_suggestion=f"Check {pattern.source_file} for implementation details",
                source_info={
                    "pattern_id": pattern.pattern_id,
                    "source_file": pattern.source_file,
                    "code_snippet": pattern.code_snippet[:100]
                }
            )
            suggestions.append(suggestion)
        
        return suggestions
    
    def _get_context_based_suggestions(self, problem_type: str) -> List[KnowledgeSuggestion]:
        """Get suggestions based on previous session contexts"""
        suggestions = []
        
        try:
            related_sessions = self.suggest_related_sessions(problem_type)
            
            for session in related_sessions[:2]:  # Limit to top 2
                suggestion = KnowledgeSuggestion(
                    suggestion_type="previous_context",
                    title=f"Previous {session['problem_type']} session",
                    description=session['description'],
                    relevance_score=min(session['relevance'] / 3.0, 1.0),
                    action_suggestion="Consider restoring session context for similar approach",
                    source_info={
                        "session_id": session['session_id'],
                        "restoration_available": session['restoration_available']
                    }
                )
                suggestions.append(suggestion)
                
        except Exception:
            pass
        
        return suggestions
    
    def _get_file_based_suggestions(self, current_file: str) -> List[KnowledgeSuggestion]:
        """Get suggestions based on current file context"""
        suggestions = []
        
        # Simple file-based suggestions
        file_path = Path(current_file)
        
        if "test" in file_path.name.lower():
            suggestion = KnowledgeSuggestion(
                suggestion_type="pattern_match",
                title="Testing pattern detected",
                description="Consider checking existing test patterns",
                relevance_score=0.6,
                action_suggestion="Look for similar test implementations",
                source_info={"file_type": "test", "suggestion": "testing_patterns"}
            )
            suggestions.append(suggestion)
        
        return suggestions
    
    def _get_workflow_suggestions(self, problem_type: str) -> List[KnowledgeSuggestion]:
        """Get workflow suggestions based on problem type"""
        workflow_suggestions = {
            "implementation": "Consider checking existing implementation patterns",
            "architecture": "Look for architectural decision records and patterns",
            "debugging": "Check for similar debugging approaches in past sessions",
            "integration": "Review integration patterns and connection approaches"
        }
        
        suggestions = []
        if problem_type in workflow_suggestions:
            suggestion = KnowledgeSuggestion(
                suggestion_type="pattern_match",
                title=f"{problem_type.title()} workflow suggestion",
                description=workflow_suggestions[problem_type],
                relevance_score=0.7,
                action_suggestion=f"Search knowledge base for {problem_type} patterns",
                source_info={"workflow_type": problem_type}
            )
            suggestions.append(suggestion)
        
        return suggestions
    
    def _classify_problem_type(self, task_description: str) -> str:
        """Classify problem type from task description"""
        task_lower = task_description.lower()
        
        if any(word in task_lower for word in ["implement", "create", "build", "develop"]):
            return "implementation"
        elif any(word in task_lower for word in ["debug", "fix", "error", "bug"]):
            return "debugging"  
        elif any(word in task_lower for word in ["integrate", "connect", "merge", "combine"]):
            return "integration"
        elif any(word in task_lower for word in ["design", "architecture", "pattern", "structure"]):
            return "architecture"
        else:
            return "general"
    
    def _save_solution_pattern(self, pattern: Dict[str, Any]) -> bool:
        """Save new solution pattern to knowledge base"""
        try:
            # Load existing patterns
            patterns_file = Path("data/knowledge/code_patterns.json")
            
            if patterns_file.exists():
                with open(patterns_file, 'r', encoding='utf-8') as f:
                    patterns = json.load(f)
            else:
                patterns = []
            
            # Add new pattern
            patterns.append(pattern)
            
            # Save back
            with open(patterns_file, 'w', encoding='utf-8') as f:
                json.dump(patterns, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception:
            return False
    
    def _log_session_event(self, event_type: str, details: Dict[str, Any]):
        """Log session events for integration tracking"""
        try:
            log_file = self.integration_dir / "integration_log.jsonl"
            
            log_entry = {
                "timestamp": time.time(),
                "event": event_type,
                "session_id": self.current_session.session_id if self.current_session else "none",
                "details": details
            }
            
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry) + '\n')
                
        except Exception:
            pass  # Fail safely on logging
    
    def _suggestion_to_dict(self, suggestion: KnowledgeSuggestion) -> Dict[str, Any]:
        """Convert suggestion to dict for JSON serialization"""
        return {
            "type": suggestion.suggestion_type,
            "title": suggestion.title,
            "description": suggestion.description,
            "relevance": suggestion.relevance_score,
            "action": suggestion.action_suggestion,
            "source": suggestion.source_info
        }
    
    def get_integration_stats(self) -> Dict[str, Any]:
        """Get integration system statistics"""
        stats = {
            "enabled": self._enabled,
            "active_session": self.current_session.session_id if self.current_session else None,
            "suggestion_threshold": self._suggestion_threshold,
            "components_status": {
                "extractor": "operational",
                "discovery": "operational", 
                "context_manager": "operational"
            }
        }
        
        # Add log stats if available
        log_file = self.integration_dir / "integration_log.jsonl"
        if log_file.exists():
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    stats["log_entries"] = sum(1 for _ in f)
            except Exception:
                stats["log_entries"] = -1
        
        return stats
    
    def disable(self):
        """Disable integration system safely"""
        self._enabled = False
        if self.current_session:
            self._log_session_event("session_disabled", {"reason": "system_disabled"})
    
    def enable(self):
        """Enable integration system"""
        self._enabled = True


# Safe factory function
def create_active_integrator(extractor: Optional[SafeKnowledgeExtractor] = None,
                           discovery: Optional[SmartCodeDiscovery] = None,
                           context_manager: Optional[SessionContextManager] = None) -> ActiveKnowledgeIntegrator:
    """Create active integrator safely"""
    try:
        return ActiveKnowledgeIntegrator(extractor, discovery, context_manager)
    except Exception as e:
        print(f"Warning: Failed to create active integrator: {e}")
        # Return disabled instance
        integrator = ActiveKnowledgeIntegrator()
        integrator.disable()
        return integrator 