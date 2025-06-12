"""
RAG Context Enhancement System

Простая система для улучшения контекста AI-исполнителей через 
релевантное содержимое из .cursor/rules и struct.json
"""

from .enhancer import PromptEnhancer
from .config import RAGConfig

__all__ = ["PromptEnhancer", "RAGConfig"]
__version__ = "0.1.0" 