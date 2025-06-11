"""Session Context Manager - Phase 4A.2.3 Safe Implementation
Builds on Phase 4A.2.1 (knowledge extraction) and 4A.2.2 (discovery) safely.
"""

import json
import time
from typing import List, Dict, Any, Optional
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime

from .knowledge_extractor import SafeKnowledgeExtractor
from .code_discovery import SmartCodeDiscovery


@dataclass
class SessionSnapshot:
    """Captured session context for restoration"""
    session_id: str
    timestamp: float
    description: str
    key_decisions: List[str]
    reasoning_chains: List[Dict[str, str]]
    problem_type: str
    solutions_used: List[str]
    context_files: List[str]
    restoration_prompt: str


@dataclass
class ContextExtractionResult:
    """Result of context extraction operation"""
    session_snapshots: int
    decisions_extracted: int
    reasoning_chains: int
    extraction_time: float
    success: bool
    errors: List[str]


class SessionContextManager:
    """
    Session Context Preservation for maintaining decision-making context.
    
    Safe design principles:
    - Builds on existing Phase 4A.2.1/4A.2.2 components
    - No breaking changes to existing session logging
    - Graceful fallback if session data unavailable
    - Simple file-based storage (no complex dependencies)
    """
    
    def __init__(self, extractor: Optional[SafeKnowledgeExtractor] = None,
                 discovery: Optional[SmartCodeDiscovery] = None):
        """Initialize with optional existing components"""
        self.extractor = extractor or SafeKnowledgeExtractor()
        self.discovery = discovery or SmartCodeDiscovery()
        
        # Context storage
        self.context_dir = Path("data/sessions/context_snapshots")
        self.context_dir.mkdir(parents=True, exist_ok=True)
        
        # Session logs location (existing)
        self.sessions_dir = Path("data/logs/sessions")
        
        # State
        self._enabled = True
        self._last_extraction = 0
        
    def extract_session_context(self, session_file: Optional[Path] = None) -> ContextExtractionResult:
        """
        Extract key context from session logs safely.
        
        Preserves "why we chose X over Y" decision-making context.
        """
        if not self._enabled:
            return ContextExtractionResult(0, 0, 0, 0, False, ["Context manager disabled"])
        
        start_time = time.time()
        errors = []
        snapshots = []
        
        try:
            # Get session files (safe - uses existing file structure)
            session_files = self._get_session_files_safely(session_file)
            
            for session_file in session_files:
                try:
                    # Extract context from each session
                    session_context = self._extract_context_from_session(session_file)
                    if session_context:
                        snapshots.append(session_context)
                except Exception as e:
                    errors.append(f"Error processing {session_file}: {e}")
                    continue  # Keep going, don't fail on single session
            
            # Save snapshots (simple JSON storage)
            success = self._save_snapshots_safely(snapshots)
            
            elapsed = time.time() - start_time
            self._last_extraction = time.time()
            
            return ContextExtractionResult(
                session_snapshots=len(snapshots),
                decisions_extracted=sum(len(s.key_decisions) for s in snapshots),
                reasoning_chains=sum(len(s.reasoning_chains) for s in snapshots),
                extraction_time=elapsed,
                success=success,
                errors=errors
            )
            
        except Exception as e:
            # Full fallback - never crash
            elapsed = time.time() - start_time
            return ContextExtractionResult(
                session_snapshots=0,
                decisions_extracted=0,
                reasoning_chains=0,
                extraction_time=elapsed,
                success=False,
                errors=[f"Critical error: {e}"]
            )
    
    def _get_session_files_safely(self, specific_file: Optional[Path] = None) -> List[Path]:
        """Get session files safely"""
        try:
            if specific_file:
                return [specific_file] if specific_file.exists() else []
            
            # Get existing session files
            if not self.sessions_dir.exists():
                return []
            
            session_files = []
            for file in self.sessions_dir.iterdir():
                if file.suffix == '.jsonl' and file.is_file():
                    session_files.append(file)
            
            # Limit to recent files (safety)
            return sorted(session_files, key=lambda f: f.stat().st_mtime, reverse=True)[:10]
            
        except Exception:
            return []  # Fail safely
    
    def _extract_context_from_session(self, session_file: Path) -> Optional[SessionSnapshot]:
        """Extract context from a single session file (simple implementation)"""
        try:
            # Read session file (simple JSONL parsing)
            session_data = []
            with open(session_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            session_data.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue  # Skip malformed lines
            
            if not session_data:
                return None
            
            # Extract key information (simple pattern matching)
            session_id = session_file.stem
            description = self._extract_session_description(session_data)
            key_decisions = self._extract_decisions(session_data)
            reasoning_chains = self._extract_reasoning(session_data)
            problem_type = self._extract_problem_type(session_data)
            solutions_used = self._extract_solutions(session_data)
            context_files = self._extract_context_files(session_data)
            
            # Generate restoration prompt
            restoration_prompt = self._generate_restoration_prompt(
                description, key_decisions, reasoning_chains, problem_type
            )
            
            return SessionSnapshot(
                session_id=session_id,
                timestamp=time.time(),
                description=description,
                key_decisions=key_decisions,
                reasoning_chains=reasoning_chains,
                problem_type=problem_type,
                solutions_used=solutions_used,
                context_files=context_files,
                restoration_prompt=restoration_prompt
            )
            
        except Exception:
            return None  # Fail safely
    
    def _extract_session_description(self, session_data: List[Dict]) -> str:
        """Extract session description from data"""
        for entry in session_data:
            if entry.get('event') == 'session_start':
                return entry.get('description', 'Unknown session')
            if 'description' in entry:
                return entry['description'][:100]  # Truncate for safety
        return f"Session with {len(session_data)} events"
    
    def _extract_decisions(self, session_data: List[Dict]) -> List[str]:
        """Extract key decisions from session data"""
        decisions = []
        decision_keywords = ['decided', 'chose', 'selected', 'implemented', 'approach']
        
        for entry in session_data:
            description = entry.get('description', '').lower()
            if any(keyword in description for keyword in decision_keywords):
                decisions.append(entry.get('description', ''))
        
        return decisions[:5]  # Limit for safety
    
    def _extract_reasoning(self, session_data: List[Dict]) -> List[Dict[str, str]]:
        """Extract reasoning chains from session data"""
        reasoning = []
        reasoning_keywords = ['because', 'reason', 'why', 'rationale', 'trade-off']
        
        for entry in session_data:
            description = entry.get('description', '').lower()
            if any(keyword in description for keyword in reasoning_keywords):
                reasoning.append({
                    'step': entry.get('description', ''),
                    'timestamp': str(entry.get('timestamp', '')),
                    'event': entry.get('event', '')
                })
        
        return reasoning[:3]  # Limit for safety
    
    def _extract_problem_type(self, session_data: List[Dict]) -> str:
        """Extract problem type from session data"""
        problem_keywords = {
            'architecture': ['architecture', 'design', 'pattern'],
            'implementation': ['implement', 'code', 'function'],
            'debugging': ['debug', 'error', 'fix', 'bug'],
            'integration': ['integrate', 'connect', 'merge'],
            'refactoring': ['refactor', 'improve', 'optimize']
        }
        
        all_text = ' '.join(entry.get('description', '').lower() for entry in session_data)
        
        for problem_type, keywords in problem_keywords.items():
            if any(keyword in all_text for keyword in keywords):
                return problem_type
        
        return 'general'
    
    def _extract_solutions(self, session_data: List[Dict]) -> List[str]:
        """Extract solutions used from session data"""
        solutions = []
        for entry in session_data:
            if entry.get('event') in ['component_created', 'solution_implemented', 'test_passed']:
                solutions.append(entry.get('description', ''))
        return solutions[:3]  # Limit for safety
    
    def _extract_context_files(self, session_data: List[Dict]) -> List[str]:
        """Extract relevant context files from session data"""
        files = set()
        for entry in session_data:
            # Look for file references
            description = entry.get('description', '')
            if '.py' in description or '.json' in description or '.md' in description:
                # Simple extraction - could be improved
                words = description.split()
                for word in words:
                    if any(ext in word for ext in ['.py', '.json', '.md']):
                        files.add(word.strip('.,;:'))
        return list(files)[:5]  # Limit for safety
    
    def _generate_restoration_prompt(self, description: str, decisions: List[str], 
                                   reasoning: List[Dict], problem_type: str) -> str:
        """Generate restoration prompt for session context"""
        prompt_parts = [
            f"# Session Context Restoration",
            f"",
            f"**Problem Type:** {problem_type}",
            f"**Description:** {description}",
            f""
        ]
        
        if decisions:
            prompt_parts.append("**Key Decisions Made:**")
            for i, decision in enumerate(decisions, 1):
                prompt_parts.append(f"{i}. {decision}")
            prompt_parts.append("")
        
        if reasoning:
            prompt_parts.append("**Reasoning Chain:**")
            for i, reason in enumerate(reasoning, 1):
                prompt_parts.append(f"{i}. {reason['step']}")
            prompt_parts.append("")
        
        prompt_parts.append("**Context restored. You can now continue with similar problem-solving approach.**")
        
        return "\n".join(prompt_parts)
    
    def _save_snapshots_safely(self, snapshots: List[SessionSnapshot]) -> bool:
        """Save session snapshots to JSON safely"""
        try:
            snapshots_file = self.context_dir / "session_contexts.json"
            
            # Convert snapshots to dict format
            snapshots_data = []
            for snapshot in snapshots:
                snapshots_data.append(asdict(snapshot))
            
            # Save with backup (safe)
            if snapshots_file.exists():
                backup_file = self.context_dir / f"session_contexts_backup_{int(time.time())}.json"
                snapshots_file.rename(backup_file)
            
            with open(snapshots_file, 'w', encoding='utf-8') as f:
                json.dump(snapshots_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Warning: Failed to save session contexts: {e}")
            return False
    
    def restore_session_context(self, session_id: str) -> Optional[str]:
        """Restore context for a specific session"""
        try:
            snapshots_file = self.context_dir / "session_contexts.json"
            
            if not snapshots_file.exists():
                return None
            
            with open(snapshots_file, 'r', encoding='utf-8') as f:
                snapshots_data = json.load(f)
            
            # Find matching session
            for snapshot_data in snapshots_data:
                if snapshot_data.get('session_id') == session_id:
                    return snapshot_data.get('restoration_prompt')
            
            return None
            
        except Exception:
            return None
    
    def get_context_stats(self) -> Dict[str, Any]:
        """Get context management statistics"""
        snapshots_file = self.context_dir / "session_contexts.json"
        
        stats = {
            "enabled": self._enabled,
            "last_extraction": self._last_extraction,
            "snapshots_file_exists": snapshots_file.exists(),
            "snapshots_count": 0,
            "problem_types": {}
        }
        
        if snapshots_file.exists():
            try:
                with open(snapshots_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    stats["snapshots_count"] = len(data)
                    
                    # Count problem types
                    for snapshot in data:
                        problem_type = snapshot.get('problem_type', 'unknown')
                        stats["problem_types"][problem_type] = stats["problem_types"].get(problem_type, 0) + 1
                        
            except Exception:
                stats["snapshots_count"] = -1  # Error reading
        
        return stats
    
    def disable(self):
        """Disable context manager safely"""
        self._enabled = False
    
    def enable(self):
        """Enable context manager"""
        self._enabled = True


# Safe factory function
def create_context_manager(extractor: Optional[SafeKnowledgeExtractor] = None,
                          discovery: Optional[SmartCodeDiscovery] = None) -> SessionContextManager:
    """Create context manager safely"""
    try:
        return SessionContextManager(extractor, discovery)
    except Exception as e:
        print(f"Warning: Failed to create context manager: {e}")
        # Return disabled instance rather than None
        manager = SessionContextManager()
        manager.disable()
        return manager

# Alias for expected function name
def create_session_context_manager(extractor: Optional[SafeKnowledgeExtractor] = None,
                                  discovery: Optional[SmartCodeDiscovery] = None) -> SessionContextManager:
    """Create session context manager safely (alias for create_context_manager)"""
    return create_context_manager(extractor, discovery) 