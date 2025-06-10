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

## 🔄 5-Phase Documentation Cleanup Strategy

### Phase 0: Documentation Reconnaissance (NEW)
- **Model**: Claude 4 Sonnet
- **Goal**: Map documentation chaos and identify cleanup priorities
- **Discovered State**:
  - **docs/ directory**: 40+ files mixed together (EPICs, ROADMAPs, analyses, archives)
  - **Root directory**: 9 misc files including temp files, duplicate configs
  - **Subdirectories**: plans/, memos/, notes/, knowledge/, epics/, to_sort/ - unknown state
  - **MCP config**: ✅ .cursor/mcp.json - simple and working (12 lines, localhost:8000/mcp)
- **Actions**:
  1. **Audit docs/ structure**: What's current, what's archive, what's duplicate
  2. **Root cleanup assessment**: Which files belong in docs/, which are temp/outdated
  3. **Content categorization**: EPICs, analyses, roadmaps, guides, archives
  4. **Priority classification**: Keep/archive/merge/delete decisions
- **Output**: `docs/documentation_cleanup_plan.md`
- **Checkpoint Template**:
```markdown
# Checkpoint: Documentation Reconnaissance
- Completed: [file categorization, structure analysis, cleanup priorities]
- Findings: [key discoveries about doc state]
- Issues: [blocking problems, unclear decisions]
- Next Steps: [specific actions for Phase 2]
- Model: Claude 4 Sonnet
```
- **⚠️ MANDATORY STOP**: Review cleanup plan before execution

### Phase 1A: struct.json Analysis (Gemini 2.5 Flash)
- **Status**: ✅ COMPLETED
- **Result**: docs/llmstruct_analysis_claude_handoff.md

### Phase 1B: Project Architecture Mapping (Claude 4 Sonnet)  
- **Status**: ✅ COMPLETED
- **Result**: Basic architecture understanding

### Phase 1C: Deep Code Analysis
- **Status**: ❌ **INCOMPLETE** - Missing tests analysis and deeper integration details  
- **Completed**: Basic code structure analysis (docs/code_analysis_phase_1c.md)
- **Missing**: 
  - **Tests analysis**: tests/test_task_router.py (21KB), test_ollama_function_calling.py (8.8KB)
  - **Integration testing**: tests/integration/, tests/orchestration/  
  - **Configuration details**: .env file, environment setup validation
  - **MCP integration depth**: How api/*.py actually works with MCP protocol
- **Need to complete**:
  1. **Test Coverage Audit** (Claude): Analyze all test files, understand what's tested/missing
  2. **Integration Analysis** (Gemini for large test files): Deep dive into test_task_router.py
  3. **Environment Validation** (Claude): Check .env, configuration completeness  
  4. **MCP Integration Details** (Claude): How api/main.py + handoff_validator.py work with MCP
- **Updated Outputs**: 
  - Enhanced docs/code_analysis_phase_1c.md with test coverage matrix
  - **NEW**: docs/test_plan.md (test coverage assessment)
  - **NEW**: docs/mcp_overview.md (MCP integration details)
- **Checkpoint Template**:
```markdown
# Checkpoint: Phase 1C Completion
- Completed: [test analysis, MCP integration, environment check]
- Findings: [test coverage gaps, integration issues]
- Issues: [blocking problems, missing components]
- Next Steps: [specific Phase 2 preparation actions]
- Model: [Claude/Gemini/o3-mini as appropriate]
```
- **⚠️ MUST COMPLETE before Phase 2**

### Phase 2: Implementation & Integration Analysis
- **Model**: Claude 4 Sonnet (primary) + o3-mini (complex algorithms)
- **Goal**: Understand how components work together, identify gaps and issues
- **Prerequisites**: Phase 1C must be completed with test analysis
- **Actions**:
  1. **Integration Testing**: Run actual tests, check what works/fails
  2. **Component Interaction**: How TaskRouter + API + MCP work together  
  3. **Performance Validation**: Real-world TaskRouter routing decisions
  4. **Gap Identification**: What's missing for full functionality
- **Documentation Updates**:
  - **data/knowledge/README.md**: Project overview and capabilities
  - **docs/orchestration/README.md**: Multi-agent orchestration guide
  - **docs/taskrouter/README.md**: Smart routing usage guide
- **Output**: docs/integration_analysis_phase_2.md
- **Checkpoint Template**:
```markdown
# Checkpoint: Integration Analysis
- Completed: [component testing, integration validation]
- Findings: [working components, broken integrations]
- Issues: [performance problems, missing features]
- Next Steps: [prioritized fix list for Phase 3]
- Model: Claude 4 Sonnet
```
- **⚠️ MANDATORY STOP**: Review integration state before Phase 3

### Phase 3: Planning & Gap Resolution
- **Model**: Claude 4 Sonnet + o3-mini for complex planning decisions
- **Goal**: Create action plan to resolve identified gaps and optimize system
- **Actions**:
  1. **Gap Prioritization**: Critical vs nice-to-have improvements
  2. **Implementation Roadmap**: Step-by-step resolution plan
  3. **Resource Assessment**: What needs to be built/fixed/optimized
  4. **Documentation Cleanup Plan**: Based on integration findings
- **Documentation Tasks**:
  - **docs/documentation_cleanup_plan.md**: Files to archive/merge/update
  - Update project_state.json with realistic status vs aspirational
- **Output**: docs/improvement_roadmap_phase_3.md
- **⚠️ MANDATORY STOP**: Approve plan and resource allocation before Phase 4

### Phase 4: Content Audit & Gap Analysis
- **Model**: Gemini 2.5 Flash (for comprehensive content review)
- **Goal**: Identify missing documentation and content gaps
- **Actions**:
  1. **Current state documentation**: What actually works vs what's documented
  2. **Missing guides**: Practical usage, setup, troubleshooting
  3. **Outdated content**: Update status, remove deprecated information
  4. **Knowledge gaps**: What's implemented but not documented
- **⚠️ MANDATORY STOP**: Prioritize content creation before Phase 4

### Phase 4: Content Creation & Updates
- **Model**: Task-specific selection
- **Goal**: Create missing practical documentation
- **Actions**:
  1. **Essential guides**: Setup, usage, troubleshooting based on real testing
  2. **Update status files**: Reflect actual working state vs aspirational
  3. **Consolidate learnings**: From this cleanup session into reusable guides
  4. **Remove theoretical**: Keep only proven-working documentation

---

## 🎭 Updated Role Prompts

### **🗂️ Роль: Documentation Auditor (Claude 4 Sonnet)**
```
[audit][docs] ФАЗА 0: Документационная разведка

Проанализируй состояние документации в проекте llmgenie:

docs/ (40+ файлов смешаны):
- EPICs, ROADMAPs, анализы, архивы в одной папке
- Дублирующиеся файлы (ROADMAP_STRATEGIC*, EPIC5_*)
- Подпапки: plans/, memos/, notes/, knowledge/, epics/, to_sort/

Корень проекта (барахло):
- docs.json (53KB) - что это?
- temp_checklist_archive_analysis.md - временный файл
- meta_files.txt, meta_links.txt - служебные файлы
- PR_KNOWLEDGE_BASE.md - должен быть в docs/

ЗАДАЧИ:
1. Категоризируй файлы: актуальные/архивные/дубли/временные
2. Определи структуру reorganization
3. Выяви пропущенную документацию
4. Создай план cleanup с приоритетами

РЕЗУЛЬТАТ: docs/documentation_cleanup_plan.md
```

### **🧹 Роль: Documentation Organizer (Claude 4 Sonnet)**
```
[meta][cleanup] ФАЗА 2: Исполнение cleanup плана

Выполни reorganization документации по плану:
1. Создай структуру папок docs/{epics,analyses,guides,archive}/
2. Переместить файлы в правильные места
3. Объединить дублирующиеся файлы
4. Архивировать устаревшие документы
5. Очистить корень проекта от барахла
6. Обновить ссылки после перемещения

Принцип: Лучше меньше, да лучше. Убрать хаос, оставить рабочее.
```

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