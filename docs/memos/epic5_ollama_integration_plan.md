# Epic 5: MCP-Ollama Integration для Task Offloading

**Дата:** 2025-01-05  
**Автор:** ai_assistant  
**Статус:** Планирование

---

## Цели Epic 5

Реализовать интеграцию MCP с локальной Ollama для автоматического offloading рутинных задач, освобождая дорогие API calls для сложных задач.

### Ключевые результаты:
- 🎯 MCP server с Ollama routing по типу задач
- 🎯 Quality control и validation pipeline для Ollama результатов  
- 🎯 Автоматическое разделение: сложное → Claude, рутинное → Ollama
- 🎯 Экономия API calls и повышение скорости выполнения

---

## Foundation: Lessons Learned из Epic 2

Из **docs/memos/epic2/** уже имеем опыт работы с Ollama:

### ✅ Что работает хорошо:
- Генерация unit-тестов
- Объяснение кода
- Рефакторинг по шаблонам  
- Генерация changelog
- Аудит кода по правилам

### ❌ Что лучше оставить Claude:
- Архитектурные решения
- Сложный debugging
- Code review с контекстом
- Планирование эпиков

### 🏗️ Архитектурные принципы:
- Атомизация задач
- Очередь команд  
- Автоматическая валидация результата
- MCP как glue layer
- Фокус основного LLM на сложных задачах

---

## Техническая архитектура

```
┌─────────────┐    MCP     ┌──────────────────┐    HTTP    ┌──────────────┐
│   Cursor    │ ─────────→ │ llmgenie MCP     │ ──────────→ │    Ollama    │
│  (Claude)   │           │ Server           │            │ (localhost)  │
│             │           │ - Routing        │            │              │
│             │           │ - Quality Check  │            │              │
└─────────────┘           │ - Result Valid.  │            └──────────────┘
                          └──────────────────┘
```

---

## Чеклист реализации

### Phase 1: Ollama Client Integration (Основа)
- [ ] Создать `src/llmgenie/integrations/ollama_client.py`
- [ ] Добавить конфигурацию Ollama в settings
- [ ] Тесты для Ollama client
- [ ] Проверка доступности Ollama сервера

### Phase 2: MCP Routing Logic (Умный роутинг)
- [ ] Функция `should_use_ollama(task: str) -> bool`
- [ ] Patterns для классификации задач
- [ ] Fallback на Claude при недоступности Ollama
- [ ] Логирование routing решений

### Phase 3: Quality Control Pipeline (Контроль качества)
- [ ] Validation functions для разных типов задач
- [ ] Scoring system для Ollama результатов
- [ ] Retry logic при низком качестве
- [ ] Metrics сбор (success rate, latency)

### Phase 4: MCP Tools Implementation (Инструменты)
- [ ] `generate_with_ollama` MCP tool
- [ ] `explain_code_ollama` MCP tool  
- [ ] `refactor_code_ollama` MCP tool
- [ ] `audit_code_ollama` MCP tool

### Phase 5: Integration & Testing (Интеграция)
- [ ] Обновить `.cursor/mcp.json` с Ollama tools
- [ ] E2E тесты MCP-Ollama workflow
- [ ] Performance benchmarks vs Claude-only
- [ ] Cursor integration тестирование

### Phase 6: Documentation & Best Practices (Документация)
- [ ] Обновить `docs/mcp_integration_guide.md`
- [ ] Best practices для task classification
- [ ] Troubleshooting guide
- [ ] Примеры использования

---

## Компоненты для реализации

### 1. OllamaClient
```python
class OllamaClient:
    async def generate(self, prompt: str, model: str = "llama3.2") -> str
    async def is_available(self) -> bool
    async def get_models(self) -> List[str]
```

### 2. TaskRouter
```python
class TaskRouter:
    def should_use_ollama(self, task: str) -> bool
    def get_ollama_model(self, task_type: str) -> str
    def create_optimized_prompt(self, task: str, context: str) -> str
```

### 3. QualityValidator
```python
class QualityValidator:
    async def validate_result(self, task: str, result: str) -> ValidationResult
    def calculate_score(self, result: str, task_type: str) -> float
    def should_retry(self, score: float, attempt: int) -> bool
```

### 4. MCP Tools
```python
@mcp_tool
async def generate_with_ollama(task: str, context: str = "") -> dict:
    """Offload generation task to local Ollama"""
    
@mcp_tool  
async def explain_code_ollama(code: str, language: str = "python") -> dict:
    """Explain code using Ollama"""
```

---

## Критерии успеха

### Technical Success Metrics:
- [ ] Ollama integration работает стабильно
- [ ] Routing accuracy > 90% (правильно классифицирует задачи)
- [ ] Quality score > 0.8 для Ollama результатов
- [ ] API calls reduction > 30% для рутинных задач
- [ ] Response time < 5s для Ollama задач

### User Experience Metrics:
- [ ] Прозрачность для пользователя (не видит переключения)
- [ ] Качество результатов не хуже чем Claude-only
- [ ] Скорость выполнения рутинных задач выше
- [ ] Документация позволяет легко настроить

### Integration Metrics:
- [ ] Все MCP tools работают в Cursor
- [ ] E2E workflow: task → routing → execution → validation
- [ ] Error handling и graceful fallbacks
- [ ] Monitoring и logging всех операций

---

## Risk Mitigation

### Технические риски:
- **Ollama недоступна** → Fallback на Claude
- **Низкое качество результатов** → Retry или fallback
- **Медленная работа** → Таймауты и async execution

### UX риски:
- **Непрозрачность routing** → Логирование и опции debug
- **Качество хуже чем Claude** → Strict validation и fallbacks
- **Сложность настройки** → Подробная документация

---

## Next Steps

1. **Phase 1** начать с простого Ollama client + MCP tool
2. **Тестирование** на простых задачах (generate tests, explain code)  
3. **Итерация** по feedback и quality metrics
4. **Scaling** на более сложные сценарии

**Готовность к запуску:** После завершения Epic 4 MCP foundation

---

## Context Files для Epic 5

- Foundation: `docs/mcp_integration_guide.md` (Epic 4 results)
- Lessons: `docs/memos/epic2/` (Ollama experience)
- Architecture: `src/llmgenie/api/main.py` (MCP server base)
- Tests: `tests/api/test_handoff_validator.py` (MCP testing patterns) 