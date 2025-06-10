# Стратегический План Работы с Проектом - Июнь 2025

## 📋 Текущее Состояние

**Используемая модель**: Claude 4 Sonnet ⭐ (премиум выбор!)  
**Проект**: llmgenie  
**Цель**: Разобраться с проектом, не накосячить из-за ошибок интерпретации

---

## 🎯 Стратегия Переключения Моделей

### **Когда оставить Claude 4 Sonnet**:
- ✅ Анализ сложного кода
- ✅ Архитектурные решения
- ✅ Отладка багов
- ✅ Планирование и стратегия
- ✅ Работа с документацией
- ✅ Code review

### **Когда переключиться на Gemini 2.5 Flash**:
- 📊 Работа с ОГРОМНЫМИ файлами (>120k токенов)
- 📊 Анализ всей кодовой базы целиком
- 📊 Массовый рефакторинг
- 📊 Когда нужен контекст 1M токенов
- 📊 Экономия requests (бесплатно)

### **Когда использовать o3/o4-mini**:
- 🧠 Сложные алгоритмические задачи
- 🧠 Debugging очень запутанных багов
- 🧠 Математические вычисления
- 🧠 Логические головоломки в коде

---

## 🎯 Критически Важно: llmstruct Integration

### **⚠️ ПЕРЕД ЛЮБЫМ АНАЛИЗОМ:**
1. **Проверить Rule 017_struct_tools_integration**
2. **🚨 ВАЖНО: struct.json (193KB) → Gemini 2.5 Flash**
3. **Изучить `src/.llmstruct_index/` modular index**
4. **Проверить git-зависимость llmstruct в requirements.txt**

### **📊 Данные для анализа:**
- **struct.json:** 193KB, 7131 строк, 42 модуля, 180 функций, 37 классов
- **Сложность:** 44 связи (call_edges, dependencies, imports)
- **Версия:** 2025-06-10T08:28:05.981983Z (актуальная)
- **⚠️ Риск:** Может вызвать глючи у Claude при долгом контексте

### **🔄 Стратегия переключения моделей:**
1. **Claude 4 Sonnet** → **Gemini 2.5 Flash** для анализа struct.json
2. **Обязательные checkpoint'ы** при каждом переходе  
3. **Документирование входа/выхода** между моделями
4. **Сохранение результатов в файлы** для передачи контекста

### **🔗 Архитектурные связи:**
- llmgenie зависит от llmstruct через git-dependency
- TaskRouter может использовать struct.json для анализа кода
- CLI llmgenie интегрирован с llmstruct парсером

---

## 📋 Analysis Artifacts Tracking

### ✅ Completed Analysis
- **Phase 1A**: struct.json analysis (Gemini 2.5 Flash) → `docs/llmstruct_analysis_claude_handoff.md`
- **Phase 1B**: Project architecture mapping (Claude 4 Sonnet) → logged in session
- **Environment**: requirements.txt, venv/, directory structure → validated
- **Integration**: llmstruct git dependency → confirmed working

### 🎯 Phase 1C Target Files (Prioritized)
- **task_router/task_classifier.py** (10KB, 270 lines) - Task classification logic
- **task_router/model_router.py** (9.2KB, 240 lines) - Model selection algorithms  
- **task_router/quality_validator.py** (14KB, 383 lines) - Quality validation rules
- **orchestration/agent_orchestrator.py** (20KB, 516 lines) - Agent coordination
- **api/main.py** (8.8KB, 256 lines) - FastAPI endpoints + MCP
- **api/handoff_validator.py** (11KB, 251 lines) - Handoff validation logic
- **.env** (if exists) - Environment configuration
- **.cursor/mcp.json** - MCP integration config

### 📊 Analysis Coverage Matrix
| Component | Structure | Implementation | Integration | Config | Status |
|-----------|-----------|----------------|-------------|--------|--------|
| llmstruct | ✅ | ✅ | ✅ | ✅ | Complete |
| CLI | ✅ | ✅ | ✅ | ✅ | Complete |
| LLMClient | ✅ | ✅ | ✅ | ❓ | Need config check |
| TaskRouter | ✅ | ❌ | ❓ | ❓ | **Phase 1C target** |
| Orchestration | ✅ | ❌ | ❓ | ❓ | **Phase 1C target** |
| API/MCP | ✅ | ❌ | ❓ | ❓ | **Phase 1C target** |

---

## 🔄 4-Phase Workflow Strategy

### Phase 1A: struct.json Analysis (Gemini 2.5 Flash)
- **Model**: Gemini 2.5 Flash (1M контекст, бесплатно)
- **Goal**: Deep llmstruct integration analysis
- **Status**: ✅ COMPLETED
- **Промпт**:
```
[code][analysis] ФАЗА 1A: Анализ llmstruct архитектуры

ПЕРЕКЛЮЧИСЬ НА GEMINI 2.5 FLASH (1M контекст, бесплатно)

Проанализируй файл src/struct.json (193KB, 7131 строк):
- 🏗️ Архитектурные паттерны и модульная структура
- 🔗 Call edges и зависимости между компонентами  
- 📊 Метрики: 42 модуля, 180 функций, 37 классов
- ⚠️ Потенциальные проблемы интеграции llmstruct ↔ llmgenie

РЕЗУЛЬТАТ: Сохрани детальный анализ в файл docs/llmstruct_analysis_claude_handoff.md
для передачи Claude 4 Sonnet на следующем этапе.
```

### Phase 1B: Project Architecture Mapping (Claude 4 Sonnet)
- **Model**: Claude 4 Sonnet
- **Goal**: High-level project structure understanding
- **Status**: ✅ COMPLETED
- **Промпт**:
```
[audit][meta] ФАЗА 1B: Разведка проекта llmgenie

ИСПОЛЬЗУЙ РЕЗУЛЬТАТЫ: docs/llmstruct_analysis_claude_handoff.md

Проанализируй структуру проекта /home/kpblc/projects/llmgenie:
- 📁 Общую архитектуру с учетом llmstruct интеграции
- 🔧 Состояние окружения (venv, зависимости)
- ⚙️ Конфигурационные файлы
- ⚠️ Потенциальные проблемы setup'а

НЕ делай выводов о работоспособности кода без проверки окружения.
CHECKPOINT: Зафиксируй результаты для Фазы 1C.
```

### Phase 1C: Deep Code Analysis
- **Model Selection Strategy**: 
  - **Claude 4 Sonnet**: Complex logic analysis, error patterns, integration flows (<15KB files)
  - **Gemini 2.5 Flash**: Large files (>15KB), comprehensive analysis (>100KB context)
- **Goal**: Detailed implementation understanding
- **Status**: 🔄 CURRENT PHASE
- **Target Files with Model Assignment**: 
  - 🎯 **task_router/task_classifier.py** (10KB) → Claude 4 Sonnet
  - 🎯 **task_router/model_router.py** (9.2KB) → Claude 4 Sonnet  
  - 🔄 **task_router/quality_validator.py** (14KB) → Claude 4 Sonnet → **SWITCH to Gemini 2.5 Flash if needed**
  - 🔄 **orchestration/agent_orchestrator.py** (20KB) → **SWITCH to Gemini 2.5 Flash**
  - 🎯 **api/main.py** (8.8KB) → Claude 4 Sonnet
  - 🎯 **api/handoff_validator.py** (11KB) → Claude 4 Sonnet
  - 🎯 **Configuration files** (.env, .cursor/mcp.json) → Claude 4 Sonnet
- **⚠️ Model Switch Checkpoints**: After each file >15KB, validate analysis completeness before model switch
- **Промпт**:
```
[code][analysis] ФАЗА 1C: Глубокий анализ кода

Проанализируй детально implementation файлов:
- task_router/task_classifier.py (10KB) - логика классификации задач
- task_router/model_router.py (9.2KB) - алгоритмы выбора модели
- task_router/quality_validator.py (14KB) - правила валидации качества
- api/main.py (8.8KB) - FastAPI endpoints + MCP
- api/handoff_validator.py (11KB) - логика валидации handoff

ФОКУС: Implementation logic, error handling, performance bottlenecks, integration patterns

⚠️ МОДЕЛЬНЫЕ ПЕРЕКЛЮЧЕНИЯ:
- Для файлов >15KB (quality_validator.py, agent_orchestrator.py) → переключись на Gemini 2.5 Flash
- Для complex logic analysis → остайся на Claude 4 Sonnet
- CHECKPOINT после каждого переключения модели

РЕЗУЛЬТАТ: Сохрани детальный анализ в файл docs/code_analysis_phase_1c.md
для передачи в Phase 2 Diagnosis.

Включи:
- Implementation patterns и архитектурные решения
- Error handling strategies и potential bottlenecks  
- Integration points между компонентами
- Рекомендации для Phase 2 Diagnosis
```
- **⚠️ MANDATORY STOP**: Review implementation findings before Phase 2

### Phase 2: Diagnosis
- **Model**: Claude 4 Sonnet
- **Goal**: Identify concrete issues, environment problems, configuration gaps
- **Actions**: Environment validation, dependency analysis, error identification
- **⚠️ MANDATORY STOP**: Review diagnosis, prioritize fixes before Phase 3

### Phase 3: Planning
- **Model**: Claude 4 Sonnet + o3-mini for complex decisions
- **Goal**: Create detailed action plan with priorities and risk assessment
- **Actions**: Solution design, implementation roadmap, resource planning
- **⚠️ MANDATORY STOP**: Approve plan and resource allocation before Phase 4

### Phase 4: Implementation
- **Model**: Task-specific selection
- **Goal**: Execute planned improvements and verify results
- **Actions**: Code changes, configuration updates, testing, documentation
- **⚠️ MANDATORY STOP**: After each major change for validation

---

## 🎭 Роли и Промпты

### **🔍 Роль: Системный Аналитик (Claude 4 Sonnet)**
```
[audit][analysis] Проанализируй текущее состояние проекта llmgenie. 
Сфокусируйся на:
1. Структуре проекта и архитектуре
2. Состоянии зависимостей и окружения
3. Потенциальных проблемах конфигурации
4. НЕ делай поспешных выводов о "неработающем коде"

Дай объективную оценку состояния без попыток угодить.
```

### **🐛 Роль: Дебаггер (Claude 4 Sonnet)**
```
[debug][code] Проанализируй найденные ошибки.
Различай:
- Реальные баги в коде vs проблемы окружения
- Отсутствующие зависимости vs логические ошибки  
- Конфигурационные проблемы vs архитектурные недочеты

Предложи конкретные шаги исправления с приоритизацией.
```

### **📊 Роль: Архитектор (Gemini 2.5 Flash для больших файлов)**
```
[code][analysis] Проанализируй всю кодовую базу проекта целиком.
Используй весь доступный контекст (1M токенов).
Выяви:
- Паттерны архитектуры
- Связи между компонентами
- Возможности для улучшения
- Консистентность стиля кода
```

### **🧠 Роль: Problem Solver (o3-mini для сложных задач)**
```
[debug][reasoning] Реши сложную техническую проблему пошагово.
Используй глубокие рассуждения для:
- Анализа причинно-следственных связей
- Поиска неочевидных решений
- Оптимизации алгоритмов
- Решения архитектурных головоломок
```

---

## ⚠️ Протокол "Безопасной Диагностики"

### **Принципы:**
1. **Не объявляй код нерабочим** до проверки окружения
2. **Сначала проверь venv и зависимости**
3. **Различай ошибки среды vs ошибки кода**
4. **Делай маленькие шаги с проверкой**
5. **Сохраняй контекст на каждом шаге**

### **Чек-лист проверок:**
- [ ] Virtual environment активирован?
- [ ] Все зависимости установлены?
- [ ] Переменные окружения настроены?
- [ ] Пути к файлам корректны?
- [ ] Права доступа настроены?
- [ ] Конфигурационные файлы на месте?

---

## 🔄 Workflow с Сохранением Контекста

### **Шаблон перехода между задачами:**

**Промпт завершения этапа:**
```
[checkpoint] Зафиксируй текущий контекст:
- Что сделано на этом этапе
- Ключевые находки
- Проблемы, требующие внимания
- Следующие шаги
- Рекомендации по выбору модели для следующего этапа
```

**Промпт начала нового этапа:**
```
[context][role_switch] Восстанови контекст по предыдущему этапу.
Прими роль [указать роль].
Начни работу с учетом найденной информации.
```

---

## 🌐 Про Оптимизацию Промптов

### **Стоит ли пропускать через ChatGPT?**

**ДА, если:**
- Промпт сложный и многоуровневый
- Нужна техническая точность терминов
- Хочешь максимальную эффективность

**НЕТ, если:**
- Простой запрос
- Работаешь в режиме реального времени
- Уже на русском и понятно

### **Шаблон для оптимизации:**
```
"Оптимизируй этот промпт для AI модели. Сделай его более точным, 
конкретным и эффективным. Переведи на английский если нужно:

[твой промпт]"
```

---

## 🚀 Готов продолжать Phase 1C?

**Следующий шаг**: Глубокий анализ implementation файлов task_router и API компонентов.

**Готов начинать Phase 1C с промптом выше или нужны корректировки?** 