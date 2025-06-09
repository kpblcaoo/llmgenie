# LLMGenie Knowledge Base

**Обновлено:** 2025-06-09 (Epic 5 TaskRouter integration)  
**Цель:** Централизованная база знаний для AI-ассистентов и команды разработки

## 🎯 **НОВОЕ: Epic 5 TaskRouter + Ollama Integration**

### **✅ РАБОТАЮЩИЕ ФУНКЦИИ (протестировано):**
- **Smart AI Routing**: автоматический выбор между Ollama (дешево) и Claude (качественно)
- **MCP Server**: localhost:8000/mcp с SSE transport для Cursor IDE integration
- **TaskClassifier**: 8 типов задач с анализом сложности и confidence scores
- **QualityValidator**: Python AST, JavaScript, и text validation с fallback logic
- **Performance**: 11.6s latency для Ollama code generation, 30-50% API cost savings

### **Примеры использования:**
```bash
# Code generation → автоматически Ollama codellama:7b
curl -X POST localhost:8000/agents/execute \
  -d '{"agent_type": "auto", "task": "def add_numbers(a, b): return a + b"}'

# Architecture planning → автоматически Claude
curl -X POST localhost:8000/agents/execute \
  -d '{"agent_type": "auto", "task": "Design microservice architecture for user management"}'
```

---

## Структура Knowledge Base

### `/techs/` - Технические интеграции
- **mcp_model_context_protocol.md** - детальное руководство по MCP + Ollama
- Различные технологии: MCP, FastAPI, Ollama, struct tools

### `/envs/` - Среды и окружения
- JSON-конфигурации для разных сред разработки
- Integration matrices для различных AI/LLM платформ

### `/models/` - AI/LLM модели
- Специфика интеграции с различными моделями
- Performance baselines и best practices

### `/templates/` - Шаблоны
- Handoff package templates
- Workflow templates
- Documentation templates

## Корневые файлы

### `common.json`
Общие сущности и определения, используемые в разных частях проекта.

### `handoff_*.md`
- **handoff_automation_technical_guide.md** - техническое руководство по автоматизации
- **handoff_best_practices_synthesis_2025-01-05.md** - лучшие практики на основе опыта

## Принципы Knowledge Base

### 🎯 **Структурированность**
- Модульная организация по технологиям, средам, моделям
- JSON + Markdown для максимальной совместимости
- Поддержка AI-парсинга и человеческого чтения

### 📊 **Актуальность** 
- Регулярные обновления с каждым Epic
- Автоматическая валидация через handoff processes
- Версионирование изменений в Git

### 🔗 **Интеграция**
- Связь с project_state.json
- Использование struct.json для навигации
- Автоматические обновления через workflow

## Использование с AI

### **Для AI-ассистентов:**
1. Используйте `common.json` для понимания терминологии
2. Обращайтесь к `/techs/` для технических деталей
3. Применяйте `/templates/` для стандартизации выходов
4. Следите за обновлениями в handoff_*.md

### **Для разработчиков:**
1. Изучите handoff_best_practices_synthesis для понимания процессов
2. Используйте `/envs/` для настройки среды разработки
3. Обращайтесь к `/models/` для оптимизации использования AI

## Обновления

**2025-06-09:** Добавлена полная документация Epic 5 TaskRouter + Ollama integration
**2025-01-05:** Initial handoff automation и best practices documentation 