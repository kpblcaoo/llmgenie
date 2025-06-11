"""Configuration для RAG Context системы"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class RAGConfig:
    """Конфигурация для RAG Context Enhancement"""
    
    # Пути к источникам данных
    rules_dir: Path = Path(".cursor/rules")
    struct_json: Path = Path("struct.json")
    
    # Embedding конфигурация
    embedding_model: str = "all-MiniLM-L6-v2"
    embedding_dim: int = 384
    
    # Retrieval параметры
    max_context_length: int = 2000  # максимальная длина контекста
    similarity_threshold: float = 0.3  # порог релевантности (понижен для лучшего срабатывания)
    max_chunks: int = 3  # максимум чанков в результате
    
    # Кэширование
    cache_embeddings: bool = True
    cache_dir: Path = Path(".cache/rag_embeddings")
    
    # Файловые фильтры
    rules_extensions: List[str] = None  # по умолчанию [".md", ".mdc"]
    exclude_patterns: List[str] = None  # паттерны исключения
    
    def __post_init__(self):
        """Установка значений по умолчанию"""
        if self.rules_extensions is None:
            self.rules_extensions = [".md", ".mdc"]
        
        if self.exclude_patterns is None:
            self.exclude_patterns = ["*.bak", "temp_*", ".*~"]
        
        # Убеждаемся что директории существуют
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    @property
    def is_valid(self) -> bool:
        """Проверка корректности конфигурации"""
        return (
            self.rules_dir.exists() and 
            self.struct_json.exists() and
            self.max_context_length > 0 and
            0 <= self.similarity_threshold <= 1
        ) 