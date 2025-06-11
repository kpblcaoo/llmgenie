"""Context Retriever с FAISS для поиска релевантных правил"""

import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

import faiss

from .loader import Document
from .embedder import SimpleEmbedder


@dataclass 
class RetrievalResult:
    """Результат поиска контекста"""
    document: Document
    score: float
    chunk_index: int = 0  # для будущего chunking


class ContextRetriever:
    """FAISS-based retriever для поиска релевантного контекста"""
    
    def __init__(self, embedder: SimpleEmbedder, max_chunks: int = 3, 
                 similarity_threshold: float = 0.7):
        self.embedder = embedder
        self.max_chunks = max_chunks
        self.similarity_threshold = similarity_threshold
        
        # FAISS index и метаданные
        self._index: Optional[faiss.Index] = None
        self._documents: List[Document] = []
        self._embeddings: List[np.ndarray] = []
        
    def index_documents(self, documents: List[Document]) -> None:
        """Индексирует документы для поиска"""
        if not documents:
            print("Warning: No documents to index")
            return
        
        print(f"Indexing {len(documents)} documents...")
        
        # Готовим тексты для embedding
        texts = []
        for doc in documents:
            # Для больших документов можем сделать chunking в будущем
            chunked_texts = self._chunk_document(doc)
            texts.extend(chunked_texts)
        
        # Генерируем embeddings
        embeddings = self.embedder.embed_batch(texts)
        
        # Создаем FAISS index
        embedding_dim = embeddings[0].shape[0]
        self._index = faiss.IndexFlatIP(embedding_dim)  # Inner Product (cosine similarity)
        
        # Нормализуем embeddings для cosine similarity
        normalized_embeddings = []
        for emb in embeddings:
            norm = np.linalg.norm(emb)
            if norm > 0:
                normalized_embeddings.append(emb / norm)
            else:
                normalized_embeddings.append(emb)
        
        # Добавляем в index
        embeddings_matrix = np.vstack(normalized_embeddings).astype('float32')
        self._index.add(embeddings_matrix)
        
        # Сохраняем метаданные
        self._documents = documents
        self._embeddings = normalized_embeddings
        
        print(f"Successfully indexed {len(embeddings)} text chunks from {len(documents)} documents")
    
    def retrieve(self, query: str, max_results: Optional[int] = None) -> List[RetrievalResult]:
        """Ищет релевантные документы для запроса"""
        if self._index is None or not self._documents:
            print("Warning: No documents indexed")
            return []
        
        max_results = max_results or self.max_chunks
        
        # Генерируем embedding для запроса
        query_embedding = self.embedder.embed_text(query)
        query_embedding = query_embedding / np.linalg.norm(query_embedding)  # нормализуем
        
        # Ищем в FAISS index
        scores, indices = self._index.search(
            query_embedding.reshape(1, -1).astype('float32'), 
            max_results * 2  # берем больше, чтобы потом отфильтровать
        )
        
        # Обрабатываем результаты
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx >= 0 and score >= self.similarity_threshold:
                # Определяем к какому документу относится chunk
                doc_idx = min(idx, len(self._documents) - 1)  # пока простая логика
                
                result = RetrievalResult(
                    document=self._documents[doc_idx],
                    score=float(score),
                    chunk_index=0  # пока без chunking
                )
                results.append(result)
        
        # Убираем дубли по документам и сортируем по релевантности
        unique_results = self._deduplicate_results(results)
        return unique_results[:max_results]
    
    def _chunk_document(self, document: Document, chunk_size: int = 1000) -> List[str]:
        """Разбивает документ на чанки (пока простая реализация)"""
        content = document.content
        
        # Пока возвращаем весь документ как один чанк
        # В будущем можем добавить умное chunking по параграфам/секциям
        if len(content) <= chunk_size:
            return [content]
        
        # Простое chunking по предложениям
        sentences = content.split('. ')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk + sentence) > chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += sentence + ". "
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks or [content]
    
    def _deduplicate_results(self, results: List[RetrievalResult]) -> List[RetrievalResult]:
        """Убирает дубли и сортирует по релевантности"""
        # Группируем по source (путь к файлу)
        source_to_best = {}
        
        for result in results:
            source = result.document.source
            if source not in source_to_best or result.score > source_to_best[source].score:
                source_to_best[source] = result
        
        # Сортируем по score
        unique_results = list(source_to_best.values())
        unique_results.sort(key=lambda x: x.score, reverse=True)
        
        return unique_results
    
    def get_stats(self) -> Dict[str, Any]:
        """Статистика retriever"""
        return {
            "indexed_documents": len(self._documents),
            "total_embeddings": len(self._embeddings),
            "index_size": self._index.ntotal if self._index else 0,
            "similarity_threshold": self.similarity_threshold,
            "max_chunks": self.max_chunks
        } 