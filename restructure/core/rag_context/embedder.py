"""Embedding система для RAG контекста"""

import os
import json
import hashlib
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Tuple

from sentence_transformers import SentenceTransformer


class SimpleEmbedder:
    """Простая система embeddings с кэшированием"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", cache_dir: Optional[Path] = None):
        self.model_name = model_name
        self.cache_dir = cache_dir or Path(".cache/rag_embeddings")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self._model = None  # Lazy loading
        self._cache: Dict[str, np.ndarray] = {}
    
    @property
    def model(self) -> SentenceTransformer:
        """Lazy loading модели"""
        if self._model is None:
            print(f"Loading embedding model: {self.model_name}")
            self._model = SentenceTransformer(self.model_name)
        return self._model
    
    def embed_text(self, text: str) -> np.ndarray:
        """Получает embedding для текста с кэшированием"""
        # Создаем hash для кэширования
        text_hash = self._hash_text(text)
        
        # Проверяем кэш в памяти
        if text_hash in self._cache:
            return self._cache[text_hash]
        
        # Проверяем кэш на диске
        cached_embedding = self._load_from_cache(text_hash)
        if cached_embedding is not None:
            self._cache[text_hash] = cached_embedding
            return cached_embedding
        
        # Генерируем новый embedding
        embedding = self.model.encode(text, convert_to_numpy=True)
        
        # Сохраняем в кэш
        self._cache[text_hash] = embedding
        self._save_to_cache(text_hash, embedding, text[:100])  # сохраняем первые 100 символов для debug
        
        return embedding
    
    def embed_batch(self, texts: List[str]) -> List[np.ndarray]:
        """Batch обработка текстов для эффективности"""
        # Разделяем на закэшированные и новые
        cached_embeddings = {}
        new_texts = []
        new_indices = []
        
        for i, text in enumerate(texts):
            text_hash = self._hash_text(text)
            
            # Проверяем кэш
            if text_hash in self._cache:
                cached_embeddings[i] = self._cache[text_hash]
            else:
                cached_embedding = self._load_from_cache(text_hash)
                if cached_embedding is not None:
                    self._cache[text_hash] = cached_embedding
                    cached_embeddings[i] = cached_embedding
                else:
                    new_texts.append(text)
                    new_indices.append(i)
        
        # Обрабатываем новые тексты batch-ом
        if new_texts:
            print(f"Generating embeddings for {len(new_texts)} new texts")
            new_embeddings = self.model.encode(new_texts, convert_to_numpy=True)
            
            # Сохраняем в кэш
            for idx, text, embedding in zip(new_indices, new_texts, new_embeddings):
                text_hash = self._hash_text(text)
                self._cache[text_hash] = embedding
                self._save_to_cache(text_hash, embedding, text[:100])
                cached_embeddings[idx] = embedding
        
        # Собираем результат в правильном порядке
        return [cached_embeddings[i] for i in range(len(texts))]
    
    def _hash_text(self, text: str) -> str:
        """Создает hash для текста"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    def _load_from_cache(self, text_hash: str) -> Optional[np.ndarray]:
        """Загружает embedding из кэша на диске"""
        cache_file = self.cache_dir / f"{text_hash}.npy"
        if cache_file.exists():
            try:
                return np.load(cache_file)
            except Exception as e:
                print(f"Warning: Failed to load cached embedding {cache_file}: {e}")
        return None
    
    def _save_to_cache(self, text_hash: str, embedding: np.ndarray, text_preview: str):
        """Сохраняет embedding в кэш на диске"""
        try:
            # Сохраняем embedding
            cache_file = self.cache_dir / f"{text_hash}.npy"
            np.save(cache_file, embedding)
            
            # Сохраняем метаданные для debug
            meta_file = self.cache_dir / f"{text_hash}.json"
            metadata = {
                "text_preview": text_preview,
                "embedding_shape": embedding.shape,
                "model": self.model_name
            }
            with open(meta_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Warning: Failed to cache embedding {text_hash}: {e}")
    
    def similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Вычисляет cosine similarity между embeddings"""
        return float(np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2)))
    
    def find_most_similar(self, query_embedding: np.ndarray, 
                         candidate_embeddings: List[np.ndarray],
                         threshold: float = 0.7) -> List[Tuple[int, float]]:
        """Находит наиболее похожие embeddings"""
        similarities = []
        
        for i, candidate in enumerate(candidate_embeddings):
            sim = self.similarity(query_embedding, candidate)
            if sim >= threshold:
                similarities.append((i, sim))
        
        # Сортируем по убыванию схожести
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities
    
    def get_cache_stats(self) -> Dict[str, int]:
        """Статистика кэша"""
        cache_files = list(self.cache_dir.glob("*.npy"))
        return {
            "memory_cache_size": len(self._cache),
            "disk_cache_size": len(cache_files),
            "total_cache_size_mb": sum(f.stat().st_size for f in cache_files) / (1024 * 1024)
        } 