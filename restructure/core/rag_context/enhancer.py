"""Prompt Enhancer - главный интерфейс RAG системы"""

import time
from typing import List, Dict, Any, Optional
from pathlib import Path

from .config import RAGConfig
from .loader import RulesLoader, StructLoader, Document
from .embedder import SimpleEmbedder
from .retriever import ContextRetriever, RetrievalResult


class PromptEnhancer:
    """Главный интерфейс для улучшения промптов через RAG"""
    
    def __init__(self, config: Optional[RAGConfig] = None):
        self.config = config or RAGConfig()
        
        # Компоненты системы
        self.embedder = SimpleEmbedder(
            model_name=self.config.embedding_model,
            cache_dir=self.config.cache_dir
        )
        
        self.retriever = ContextRetriever(
            embedder=self.embedder,
            max_chunks=self.config.max_chunks,
            similarity_threshold=self.config.similarity_threshold
        )
        
        # Состояние
        self._initialized = False
        self._last_index_time = 0
        
    async def initialize(self) -> bool:
        """Инициализация системы - загрузка и индексация документов"""
        try:
            if not self.config.is_valid:
                print("Warning: RAG config is invalid, some features may not work")
            
            print("Initializing RAG Context System...")
            start_time = time.time()
            
            # Загружаем документы
            documents = self._load_all_documents()
            
            if not documents:
                print("Warning: No documents loaded for RAG system")
                return False
            
            # Индексируем документы
            self.retriever.index_documents(documents)
            
            self._initialized = True
            self._last_index_time = time.time()
            
            elapsed = time.time() - start_time
            print(f"RAG system initialized in {elapsed:.2f}s with {len(documents)} documents")
            
            return True
            
        except Exception as e:
            print(f"Failed to initialize RAG system: {e}")
            return False
    
    async def enhance(self, task_text: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Улучшает промпт добавлением релевантного контекста"""
        
        # Инициализируем если нужно
        if not self._initialized:
            await self.initialize()
        
        if not self._initialized:
            # Fallback: возвращаем оригинальный текст
            return task_text
        
        try:
            # Ищем релевантный контекст
            relevant_results = self.retriever.retrieve(task_text)
            
            if not relevant_results:
                # Нет релевантного контекста
                return task_text
            
            # Формируем улучшенный промпт
            enhanced_prompt = self._build_enhanced_prompt(task_text, relevant_results, context)
            
            return enhanced_prompt
            
        except Exception as e:
            print(f"Error enhancing prompt: {e}")
            # Fallback: возвращаем оригинальный текст
            return task_text
    
    def _load_all_documents(self) -> List[Document]:
        """Загружает все доступные документы"""
        documents = []
        
        # Загружаем правила из .cursor/rules
        rules_loader = RulesLoader(
            rules_dir=self.config.rules_dir,
            extensions=self.config.rules_extensions,
            exclude_patterns=self.config.exclude_patterns
        )
        rules_docs = rules_loader.load_documents()
        documents.extend(rules_docs)
        print(f"Loaded {len(rules_docs)} rule documents")
        
        # Загружаем struct.json
        struct_loader = StructLoader(self.config.struct_json)
        struct_doc = struct_loader.load_document()
        if struct_doc:
            documents.append(struct_doc)
            print("Loaded struct.json document")
        
        return documents
    
    def _build_enhanced_prompt(self, original_task: str, 
                             relevant_results: List[RetrievalResult],
                             context: Optional[Dict[str, Any]] = None) -> str:
        """Строит улучшенный промпт с контекстом"""
        
        # Собираем релевантные правила
        rules_context = []
        struct_context = []
        
        for result in relevant_results:
            doc = result.document
            score = result.score
            
            if doc.doc_type == "rule":
                # Добавляем информацию о правиле
                rule_info = f"RULE ({score:.2f}): {doc.metadata.get('title', 'Untitled')}"
                rule_content = doc.content[:self.config.max_context_length // len(relevant_results)]
                rules_context.append(f"{rule_info}\n{rule_content}")
                
            elif doc.doc_type == "struct":
                # Добавляем информацию о структуре проекта
                struct_info = f"PROJECT STRUCTURE ({score:.2f}):"
                struct_content = doc.content[:self.config.max_context_length // 2]
                struct_context.append(f"{struct_info}\n{struct_content}")
        
        # Строим итоговый промпт
        prompt_parts = []
        
        # Добавляем контекст структуры проекта
        if struct_context:
            prompt_parts.append("=== PROJECT CONTEXT ===")
            prompt_parts.extend(struct_context)
            prompt_parts.append("")
        
        # Добавляем релевантные правила
        if rules_context:
            prompt_parts.append("=== RELEVANT RULES ===")
            prompt_parts.extend(rules_context)
            prompt_parts.append("")
        
        # Добавляем дополнительный контекст если есть
        if context:
            prompt_parts.append("=== ADDITIONAL CONTEXT ===")
            for key, value in context.items():
                prompt_parts.append(f"{key}: {value}")
            prompt_parts.append("")
        
        # Добавляем оригинальную задачу
        prompt_parts.append("=== TASK ===")
        prompt_parts.append(original_task)
        
        return "\n".join(prompt_parts)
    
    def get_stats(self) -> Dict[str, Any]:
        """Статистика RAG системы"""
        stats = {
            "initialized": self._initialized,
            "last_index_time": self._last_index_time,
            "config": {
                "max_context_length": self.config.max_context_length,
                "similarity_threshold": self.config.similarity_threshold,
                "max_chunks": self.config.max_chunks
            }
        }
        
        if self._initialized:
            stats.update({
                "embedder": self.embedder.get_cache_stats(),
                "retriever": self.retriever.get_stats()
            })
        
        return stats
    
    async def refresh_index(self) -> bool:
        """Обновляет индекс документов"""
        print("Refreshing RAG index...")
        self._initialized = False
        return await self.initialize() 