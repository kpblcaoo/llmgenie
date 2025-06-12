"""Smart Code Discovery - Phase 4A.2.2 Safe Implementation
Builds on Phase 4A.2.1 knowledge extraction safely.
"""

import json
import time
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass

from .knowledge_extractor import SafeKnowledgeExtractor, CodePattern


@dataclass
class DiscoveryResult:
    """Result of code discovery search"""
    query: str
    patterns_found: List[CodePattern]
    similarity_scores: List[float]
    search_time: float
    suggestions: List[str]


class SmartCodeDiscovery:
    """
    Smart code discovery system for "Have I solved this before?" queries.
    
    Safe design principles:
    - Builds on existing Phase 4A.2.1 infrastructure
    - No breaking changes to existing components
    - Graceful degradation if knowledge base missing
    - Simple text search (no complex NLP that could break)
    """
    
    def __init__(self, extractor: Optional[SafeKnowledgeExtractor] = None):
        """Initialize with optional existing extractor"""
        self.extractor = extractor or SafeKnowledgeExtractor()
        self.knowledge_dir = Path("data/knowledge")
        self._enabled = True
        self._last_search = 0
        
    def search_solutions(self, query: str, max_results: int = 5) -> DiscoveryResult:
        """
        Search for existing solutions to a coding problem.
        
        Answers "Have I solved this before?" type queries.
        """
        if not self._enabled:
            return DiscoveryResult(query, [], [], 0, ["Discovery disabled"])
        
        start_time = time.time()
        
        try:
            # Load existing patterns (safe - uses simple JSON)
            patterns = self._load_patterns_safely()
            
            if not patterns:
                # No patterns available - suggest extraction
                return DiscoveryResult(
                    query=query,
                    patterns_found=[],
                    similarity_scores=[],
                    search_time=time.time() - start_time,
                    suggestions=["No patterns found. Run knowledge extraction first."]
                )
            
            # Simple text-based search (no complex dependencies)
            matching_patterns, scores = self._search_patterns_simple(query, patterns, max_results)
            
            # Generate practical suggestions
            suggestions = self._generate_suggestions(query, matching_patterns)
            
            self._last_search = time.time()
            
            return DiscoveryResult(
                query=query,
                patterns_found=matching_patterns,
                similarity_scores=scores,
                search_time=time.time() - start_time,
                suggestions=suggestions
            )
            
        except Exception as e:
            # Fallback - never crash
            return DiscoveryResult(
                query=query,
                patterns_found=[],
                similarity_scores=[],
                search_time=time.time() - start_time,
                suggestions=[f"Search error: {e}"]
            )
    
    def _load_patterns_safely(self) -> List[CodePattern]:
        """Load patterns from JSON safely"""
        try:
            patterns_file = self.knowledge_dir / "code_patterns.json"
            
            if not patterns_file.exists():
                return []
            
            with open(patterns_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Convert JSON back to CodePattern objects
            patterns = []
            for item in data:
                pattern = CodePattern(
                    pattern_id=item["pattern_id"],
                    name=item["name"],
                    description=item["description"],
                    code_snippet=item["code_snippet"],
                    use_cases=item.get("use_cases", []),
                    source_file=item["source_file"]
                )
                patterns.append(pattern)
            
            return patterns
            
        except Exception:
            return []  # Fail safely
    
    def _search_patterns_simple(self, query: str, patterns: List[CodePattern], 
                               max_results: int) -> Tuple[List[CodePattern], List[float]]:
        """Simple text-based pattern search (no complex NLP dependencies)"""
        
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        # Simple scoring based on text matches
        pattern_scores = []
        
        for pattern in patterns:
            score = 0.0
            
            # Check name match
            if any(word in pattern.name.lower() for word in query_words):
                score += 2.0
            
            # Check description match  
            if any(word in pattern.description.lower() for word in query_words):
                score += 1.0
            
            # Check code snippet match
            if any(word in pattern.code_snippet.lower() for word in query_words):
                score += 1.5
            
            # Check source file relevance
            source_name = Path(pattern.source_file).stem.lower()
            if any(word in source_name for word in query_words):
                score += 0.5
            
            # Boost for certain pattern types
            if pattern.name.lower() in ['class', 'def', 'function']:
                score += 0.2
            
            pattern_scores.append((pattern, score))
        
        # Sort by score and return top results
        pattern_scores.sort(key=lambda x: x[1], reverse=True)
        top_patterns = pattern_scores[:max_results]
        
        # Filter out zero scores
        relevant_patterns = [(p, s) for p, s in top_patterns if s > 0]
        
        if relevant_patterns:
            patterns_found = [p for p, s in relevant_patterns]
            scores = [s for p, s in relevant_patterns]
        else:
            patterns_found = []
            scores = []
        
        return patterns_found, scores
    
    def _generate_suggestions(self, query: str, patterns: List[CodePattern]) -> List[str]:
        """Generate practical suggestions based on found patterns"""
        suggestions = []
        
        if not patterns:
            suggestions.append("No similar patterns found.")
            suggestions.append("Consider extracting more code patterns first.")
            return suggestions
        
        # Pattern-based suggestions
        pattern_types = [p.name for p in patterns]
        
        if any("class" in name.lower() for name in pattern_types):
            suggestions.append("Found class patterns - consider OOP approach")
        
        if any("validator" in name.lower() for name in pattern_types):
            suggestions.append("Found validation patterns - check quality control")
        
        if any("executor" in name.lower() for name in pattern_types):
            suggestions.append("Found execution patterns - consider parallel/sequential")
        
        # Source-based suggestions
        sources = set(Path(p.source_file).stem for p in patterns)
        if sources:
            suggestions.append(f"Check these files: {', '.join(list(sources)[:3])}")
        
        # Generic helpful suggestions
        if len(patterns) > 1:
            suggestions.append(f"Found {len(patterns)} related patterns")
        
        return suggestions[:5]  # Limit suggestions
    
    def quick_search(self, keywords: List[str]) -> Dict[str, Any]:
        """Quick keyword-based search for rapid discovery"""
        if not self._enabled:
            return {"enabled": False}
        
        try:
            patterns = self._load_patterns_safely()
            
            matches = []
            for keyword in keywords:
                for pattern in patterns:
                    if (keyword.lower() in pattern.name.lower() or 
                        keyword.lower() in pattern.code_snippet.lower()):
                        matches.append({
                            "keyword": keyword,
                            "pattern_name": pattern.name,
                            "code_snippet": pattern.code_snippet[:100] + "...",
                            "source": Path(pattern.source_file).name
                        })
            
            return {
                "enabled": True,
                "matches": matches[:10],  # Limit results
                "search_time": time.time()
            }
            
        except Exception as e:
            return {"enabled": True, "error": str(e)}
    
    def get_discovery_stats(self) -> Dict[str, Any]:
        """Get discovery system statistics"""
        patterns_file = self.knowledge_dir / "code_patterns.json"
        
        stats = {
            "enabled": self._enabled,
            "last_search": self._last_search,
            "patterns_available": 0,
            "knowledge_file_exists": patterns_file.exists()
        }
        
        if patterns_file.exists():
            try:
                with open(patterns_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    stats["patterns_available"] = len(data)
            except Exception:
                stats["patterns_available"] = -1
        
        return stats
    
    def disable(self):
        """Disable discovery system safely"""
        self._enabled = False
    
    def enable(self):
        """Enable discovery system"""
        self._enabled = True


# Safe factory function
def create_discovery_system(extractor: Optional[SafeKnowledgeExtractor] = None) -> SmartCodeDiscovery:
    """Create discovery system safely"""
    try:
        return SmartCodeDiscovery(extractor)
    except Exception as e:
        print(f"Warning: Failed to create discovery system: {e}")
        # Return disabled instance rather than None
        discovery = SmartCodeDiscovery()
        discovery.disable()
        return discovery 