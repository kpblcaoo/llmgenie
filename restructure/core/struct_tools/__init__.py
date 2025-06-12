"""
struct_tools - Специализированные инструменты для работы со структурным анализом проекта

Этот пакет предоставляет мощные инструменты для:
- Генерации и анализа struct.json
- Работы с modular index (.llmstruct_index/)
- Архитектурного анализа проекта  
- Оценки влияния рефакторинга
- Анализа зависимостей и call graphs
"""

from .structure_analyzer import StructureAnalyzer, StructureConfig
from .cli_interface import StructureCLI

__version__ = "1.0.0"
__all__ = ["StructureAnalyzer", "StructureConfig", "StructureCLI"] 