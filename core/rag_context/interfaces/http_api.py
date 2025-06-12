"""
HTTP API Server для веб-интеграций и внешних сервисов
"""

import asyncio
import json
from typing import Dict, Any, Optional, List
from pathlib import Path

try:
    from fastapi import FastAPI, HTTPException, Query
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    import uvicorn
    FASTAPI_AVAILABLE = True
except ImportError:
    print("Warning: FastAPI not installed. Install with: pip install fastapi uvicorn")
    FASTAPI_AVAILABLE = False

from ..enhancer import PromptEnhancer
from ..config import RAGConfig


# Pydantic модели для API
class EnhanceRequest(BaseModel):
    query: str
    max_context: Optional[int] = 2000
    context: Optional[Dict[str, Any]] = None


class EnhanceResponse(BaseModel):
    enhanced_query: str
    original_query: str
    added_context_length: int
    rules_used: int


class RulesRequest(BaseModel):
    query: str
    max_rules: Optional[int] = 3


class RuleInfo(BaseModel):
    title: str
    content: str
    source: str
    score: float
    type: str


class RulesResponse(BaseModel):
    rules: List[RuleInfo]
    total_found: int


class HTTPAPIServer:
    """HTTP API Server для универсального доступа к RAG системе"""
    
    def __init__(self, config: Optional[RAGConfig] = None, port: int = 8001):
        if not FASTAPI_AVAILABLE:
            raise ImportError("FastAPI required: pip install fastapi uvicorn")
        
        self.config = config or RAGConfig()
        self.port = port
        self.enhancer = PromptEnhancer(self.config)
        
        # FastAPI app
        self.app = FastAPI(
            title="LLMGenie RAG API",
            description="API для доступа к RAG Context Enhancement системе",
            version="1.0.0"
        )
        
        # CORS middleware для веб-интеграций
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # В production ограничить домены
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        self._setup_routes()
    
    def _setup_routes(self):
        """Настройка API endpoints"""
        
        @self.app.on_event("startup")
        async def startup_event():
            """Инициализация при запуске сервера"""
            print("Initializing RAG system...")
            await self.enhancer.initialize()
            print("RAG API server ready!")
        
        @self.app.get("/")
        async def root():
            """Корневой endpoint"""
            return {
                "name": "LLMGenie RAG API",
                "version": "1.0.0",
                "status": "running",
                "initialized": self.enhancer._initialized
            }
        
        @self.app.get("/health")
        async def health_check():
            """Health check для мониторинга"""
            stats = self.enhancer.get_stats()
            return {
                "status": "healthy" if stats["initialized"] else "initializing",
                "stats": stats
            }
        
        @self.app.post("/enhance", response_model=EnhanceResponse)
        async def enhance_prompt(request: EnhanceRequest):
            """
            Улучшает промпт добавлением релевантного контекста
            """
            try:
                # Обновляем конфигурацию если нужно
                if request.max_context != self.config.max_context_length:
                    self.config.max_context_length = request.max_context
                
                original_query = request.query
                enhanced_query = await self.enhancer.enhance(request.query, request.context)
                
                # Подсчитываем статистику
                added_context_length = len(enhanced_query) - len(original_query)
                
                # Считаем использованные правила (простая эвристика)
                rules_used = enhanced_query.count("RULE (") if "RULE (" in enhanced_query else 0
                
                return EnhanceResponse(
                    enhanced_query=enhanced_query,
                    original_query=original_query,
                    added_context_length=max(0, added_context_length),
                    rules_used=rules_used
                )
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Enhancement failed: {str(e)}")
        
        @self.app.post("/rules/search", response_model=RulesResponse)
        async def search_rules(request: RulesRequest):
            """
            Ищет релевантные правила для запроса
            """
            try:
                # Инициализируем если нужно
                if not self.enhancer._initialized:
                    await self.enhancer.initialize()
                
                # Получаем результаты поиска
                results = self.enhancer.retriever.retrieve(request.query, request.max_rules)
                
                rules = []
                for result in results:
                    rule = RuleInfo(
                        title=result.document.metadata.get("title", "Untitled"),
                        content=result.document.content[:500] + "..." if len(result.document.content) > 500 else result.document.content,
                        source=result.document.source,
                        score=round(result.score, 3),
                        type=result.document.doc_type
                    )
                    rules.append(rule)
                
                return RulesResponse(
                    rules=rules,
                    total_found=len(rules)
                )
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Rules search failed: {str(e)}")
        
        @self.app.get("/project/structure")
        async def get_project_structure():
            """
            Возвращает структуру проекта из struct.json
            """
            try:
                if self.config.struct_json.exists():
                    with open(self.config.struct_json, 'r', encoding='utf-8') as f:
                        return json.load(f)
                else:
                    raise HTTPException(status_code=404, detail="struct.json not found")
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to read struct.json: {str(e)}")
        
        @self.app.get("/stats")
        async def get_system_stats():
            """
            Возвращает статистику RAG системы
            """
            try:
                return self.enhancer.get_stats()
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")
        
        @self.app.post("/admin/refresh")
        async def refresh_index():
            """
            Обновляет индекс документов RAG системы
            """
            try:
                success = await self.enhancer.refresh_index()
                if success:
                    return {"status": "success", "message": "Index refreshed successfully"}
                else:
                    raise HTTPException(status_code=500, detail="Failed to refresh index")
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error refreshing index: {str(e)}")
        
        # Простые GET endpoints для быстрого доступа
        @self.app.get("/enhance")
        async def enhance_prompt_get(
            query: str = Query(..., description="Query to enhance"),
            max_context: int = Query(2000, description="Maximum context length")
        ):
            """
            GET версия enhance для простых интеграций
            """
            request = EnhanceRequest(query=query, max_context=max_context)
            return await enhance_prompt(request)
        
        @self.app.get("/rules/search")
        async def search_rules_get(
            query: str = Query(..., description="Query to search rules"),
            max_rules: int = Query(3, description="Maximum number of rules")
        ):
            """
            GET версия rules search для простых интеграций  
            """
            request = RulesRequest(query=query, max_rules=max_rules)
            return await search_rules(request)
    
    async def run(self, host: str = "0.0.0.0"):
        """Запуск HTTP API сервера"""
        print(f"Starting HTTP API Server on {host}:{self.port}...")
        
        config = uvicorn.Config(
            app=self.app,
            host=host,
            port=self.port,
            log_level="info"
        )
        server = uvicorn.Server(config)
        await server.serve()
    
    def run_sync(self, host: str = "0.0.0.0"):
        """Синхронный запуск сервера"""
        uvicorn.run(
            self.app,
            host=host,
            port=self.port,
            log_level="info"
        )


async def main():
    """Главная функция для запуска HTTP API сервера"""
    import sys
    
    # Парсим аргументы командной строки
    host = "0.0.0.0"
    port = 8001
    
    if "--host" in sys.argv:
        host_idx = sys.argv.index("--host") + 1
        if host_idx < len(sys.argv):
            host = sys.argv[host_idx]
    
    if "--port" in sys.argv:
        port_idx = sys.argv.index("--port") + 1
        if port_idx < len(sys.argv):
            port = int(sys.argv[port_idx])
    
    # Создаем и запускаем сервер
    server = HTTPAPIServer(port=port)
    await server.run(host=host)


if __name__ == "__main__":
    asyncio.run(main()) 