"""Knowledge Extractor - Phase 4A.2.1 Safe Implementation
Builds on existing RAG infrastructure without breaking existing tools.
Lessons learned from struct tools issues applied.
"""

import json
import time
from typing import List, Dict, Any, Optional
from pathlib import Path
from dataclasses import dataclass

from .loader import Document
from .enhancer import PromptEnhancer


@dataclass
class CodePattern:
    """Extracted code pattern for knowledge base"""
    pattern_id: str
    name: str
    description: str
    code_snippet: str
    use_cases: List[str]
    source_file: str
    last_used: Optional[str] = None
    frequency: int = 1


@dataclass 
class KnowledgeExtractionResult:
    """Result of knowledge extraction operation"""
    patterns_found: int
    solutions_cataloged: int
    extraction_time: float
    errors: List[str]
    success: bool


class SafeKnowledgeExtractor:
    """
    Safe knowledge extractor that builds on existing RAG infrastructure.
    
    Design principles:
    - NO breaking changes to existing components
    - Graceful fallbacks if anything fails  
    - Self-contained with minimal dependencies
    - Can be disabled without trace
    """
    
    def __init__(self, enhancer: Optional[PromptEnhancer] = None):
        """Initialize with optional existing enhancer"""
        # Use existing enhancer or create new one (fallback)
        self.enhancer = enhancer or PromptEnhancer()
        
        # Knowledge storage
        self.knowledge_dir = Path("data/knowledge")
        self.knowledge_dir.mkdir(exist_ok=True)
        
        # State tracking
        self._enabled = True
        self._last_extraction = 0
        
    def extract_code_knowledge(self) -> Dict[str, Any]:
        """Extract code knowledge safely"""
        if not self._enabled:
            return {"success": False, "reason": "Extractor disabled"}
        
        try:
            documents = self.enhancer._load_all_documents()
            patterns = []
            
            for doc in documents:
                doc_patterns = self._extract_patterns_from_document(doc)
                patterns.extend(doc_patterns)
            
            self._save_patterns(patterns)
            
            return {
                "success": True,
                "patterns_found": len(patterns),
                "timestamp": time.time()
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _extract_patterns_from_document(self, doc: Document) -> List[CodePattern]:
        """Extract patterns from document"""
        patterns = []
        content = doc.content
        source = doc.source
        
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.strip().startswith(('def ', 'class ')):
                pattern_name = line.strip().split('(')[0].replace('def ', '').replace('class ', '')
                
                pattern = CodePattern(
                    pattern_id=f"{source}_{i}",
                    name=pattern_name,
                    description="Code pattern",
                    code_snippet=line.strip(),
                    use_cases=[],
                    source_file=source
                )
                patterns.append(pattern)
        
        return patterns
    
    def _save_patterns(self, patterns: List[CodePattern]) -> bool:
        """Save patterns to JSON"""
        try:
            patterns_file = self.knowledge_dir / "code_patterns.json"
            patterns_data = []
            
            for pattern in patterns:
                patterns_data.append({
                    "pattern_id": pattern.pattern_id,
                    "name": pattern.name,
                    "description": pattern.description,
                    "code_snippet": pattern.code_snippet,
                    "source_file": pattern.source_file,
                    "extracted_at": time.time()
                })
            
            with open(patterns_file, 'w', encoding='utf-8') as f:
                json.dump(patterns_data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception:
            return False
    
    def get_extraction_stats(self) -> Dict[str, Any]:
        """Get extraction statistics"""
        patterns_file = self.knowledge_dir / "code_patterns.json"
        
        stats = {
            "enabled": self._enabled,
            "last_extraction": self._last_extraction,
            "patterns_file_exists": patterns_file.exists(),
            "extraction_count": 0
        }
        
        if patterns_file.exists():
            try:
                with open(patterns_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    stats["extraction_count"] = len(data)
            except Exception:
                stats["extraction_count"] = -1  # Error reading
        
        return stats
    
    def disable(self):
        """Disable safely"""
        self._enabled = False
    
    def enable(self):
        """Enable knowledge extraction"""
        self._enabled = True


# Safe factory function
def create_knowledge_extractor(enhancer: Optional[PromptEnhancer] = None) -> SafeKnowledgeExtractor:
    """Create knowledge extractor safely"""
    try:
        return SafeKnowledgeExtractor(enhancer)
    except Exception as e:
        print(f"Warning: Failed to create knowledge extractor: {e}")
        # Return a disabled instance rather than None
        extractor = SafeKnowledgeExtractor()
        extractor.disable()
        return extractor 