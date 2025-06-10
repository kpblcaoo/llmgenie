# LLMGenie Knowledge Base

**Обновлено:** 2025-06-09 (Epic 5 TaskRouter integration)  
**Цель:** Централизованная база знаний для AI-ассистентов и команды разработки

## 🎯 **НОВОЕ: Smart Integration Architecture & Modular Documentation**

### **✅ РАБОТАЮЩИЕ ФУНКЦИИ (протестировано):**
- **Smart AI Routing**: автоматический выбор между Ollama (дешево) и Claude (качественно), основанный на сложности задачи и оптимизации стоимости.
- **TaskClassifier**: классификация 8 типов задач с оценкой достоверности и всесторонней логикой отката.
- **QualityValidator**: валидация Python AST, JavaScript и текста с автоматическим откатом.
- **MCP Server**: localhost:8000/mcp с SSE transport для Cursor IDE integration и вызовов инструментов.
- **Handoff Automation**: автоматизированная валидация пакетов передачи контекста для бесшовной передачи контекста.
- **Модульная документация**: центральный индекс `docs/docs.json` и модульные JSON-файлы в `docs/index/`.

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

### `/capabilities/` - Возможности проекта LLMGenie
- Документация основных функций системы, API-точек, метрик производительности и дорожной карты.

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

### `/projects/` - Знания о внешних проектах
- **internal/**: внутренние проекты разработки, эксперименты, open source.
- **commercial/**: клиентские и коммерческие проекты.

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