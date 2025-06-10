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
- **Status**: ✅ **COMPLETED** (2025-06-11) - Environment + MCP analysis added
- **Completed**: 
  - **Code Structure**: Basic architecture analysis (docs/code_analysis_phase_1c.md) 
  - **Test Coverage**: Full analysis of test_task_router.py (21KB), test_ollama_function_calling.py (8.8KB)
  - **Environment Setup**: Complete .env validation with all API keys
  - **MCP Integration**: Deep FastApiMCP analysis with SSE transport details
- **Artifacts Created**:
  - Enhanced docs/code_analysis_phase_1c.md (95% completeness assessment)
  - **NEW**: docs/mcp_overview.md (comprehensive MCP integration details)
  - **NEW**: tests/struct_and_test_coverage_insights.md (test coverage matrix)
- **Key Findings**:
  - TaskRouter + QualityValidator + HandoffValidator = Production ready
  - All API keys configured (Anthropic, Grok, GitHub, Telegram, Ollama)  
  - MCP server configured but not currently running
  - Test coverage: Unit tests complete, integration tests present, E2E tests needed
- **Checkpoint PASSED**: Ready for Phase 2 strategic implementation analysis

---

## PHASE 2: Strategic Implementation Analysis 🚀

### ✅ Phase 2A: Integration Testing & Validation (COMPLETED)
- **Prerequisites**: Phase 1C completed ✅
- **Model**: Claude 4 Sonnet  
- **Duration**: 90 minutes (actual)
- **Goal**: Test actual component integration and identify real vs perceived issues
- **Status**: ✅ **COMPLETED** (2025-06-11)
- **Results**: All core components working, environment setup validated, API endpoints operational

**Detailed Prompt:**
```
[code][test][analysis] ФАЗА 2A: Интеграционное тестирование

КОНТЕКСТ: Phase 1C показал 95% готовность архитектуры. 
Компоненты проанализированы: TaskRouter, QualityValidator, HandoffValidator, MCP, API.

ЗАДАЧА: Проверить реальную работоспособность интеграций

ПЛАН ТЕСТИРОВАНИЯ:
1. **Environment Validation**:
   - Проверь virtual environment активацию
   - Убедись что все dependencies установлены из requirements.txt
   - Валидируй .env переменные (не показывай ключи!)

2. **Component Integration Tests**:
   - Запусти test_task_router.py - что работает/падает
   - Проверь test_ollama_function_calling.py - реальные API вызовы
   - Тест TaskClassifier + ModelRouter + QualityValidator цепочки

3. **API Endpoint Testing**:
   - Запусти FastAPI сервер (python -m src.llmgenie.api.main)
   - Тест /health, /agents/execute, /handoff/validate endpoints
   - Проверь MCP mount point /mcp

4. **Real-world Routing Test**:
   - Подай несколько задач через /agents/execute
   - Проанализируй routing decisions
   - Проверь quality validation работу

ФОКУС НА:
- Что РЕАЛЬНО работает vs что только в коде
- Какие ошибки environment vs code issues
- Производительность и latency реальных вызовов

РЕЗУЛЬТАТ: 
- docs/integration_test_results_phase_2a.md
- Четкое разделение: Working ✅ / Broken ❌ / Needs Setup ⚙️

CHECKPOINT: Готов к Phase 2B только после подтверждения базовой работоспособности
```

**✅ Чеклист Phase 2A (COMPLETED):**
- [x] Virtual environment проверен ✅
- [x] Dependencies установлены и работают ✅
- [x] API ключи настроены корректно ✅ (Anthropic, Grok, GitHub, Telegram, Ollama)
- [x] Unit tests запущены и проанализированы ✅ (31/31 passed)
- [x] FastAPI сервер запускается без ошибок ✅
- [x] Basic endpoints отвечают ✅ (/health, /agents/execute, /mcp)
- [x] TaskRouter routing decisions работают ✅
- [x] Документированы реальные vs воображаемые проблемы ✅

**✅ CHECKPOINT PASSED**: Phase 2A confirmed basic system operability

### ✅ Phase 2B: Performance & Quality Analysis (COMPLETED)
- **Prerequisites**: Phase 2A integration tests passed ✅
- **Model**: Claude 4 Sonnet
- **Duration**: 60 minutes (actual)
- **Goal**: Analyze performance characteristics and quality validation effectiveness
- **Status**: ✅ **COMPLETED** (2025-06-11)
- **Critical Findings**: QualityValidator accuracy issues (42.9%), TaskRouter routing bias, struct.json integration success

**Detailed Prompt:**
```
[analysis][performance] ФАЗА 2B: Анализ производительности и качества

КОНТЕКСТ: Phase 2A подтвердил работоспособность основных компонентов.
Теперь анализируем качество решений и производительность.

ЗАДАЧИ:
1. **Model Routing Performance**:
   - Измерь latency Ollama vs Claude calls
   - Проанализируй routing decision accuracy
   - Тест quality threshold срабатывания
   - Fallback mechanism validation

2. **Quality Validator Analysis**:
   - Тест различных типов задач через QualityValidator
   - Анализ false positives/negatives в качестве оценки
   - Настройка threshold per TaskType

3. **Concurrent Load Testing**:
   - Несколько одновременных requests к /agents/execute
   - Memory usage и response time под нагрузкой
   - Error handling при перегрузке

4. **Real Use Cases**:
   - Code generation tasks (Ollama preferred)
   - Complex reasoning tasks (Claude preferred)  
   - Documentation tasks (Ollama preferred)
   - Debugging tasks (mixed routing)

МЕТРИКИ:
- Response time по моделям
- Quality score accuracy
- Cost optimization effectiveness
- Error rates и типы ошибок

РЕЗУЛЬТАТ: docs/performance_analysis_phase_2b.md

CHECKPOINT: Оптимизация рекомендации готовы
```

**✅ Чеклист Phase 2B (COMPLETED):**
- [x] Latency benchmarks сняты ✅ (TaskRouter: 0.39ms avg)
- [x] Quality validation accuracy измерена ✅ (42.9% - КРИТИЧЕСКАЯ ПРОБЛЕМА)
- [x] Real use cases протестированы ✅ (struct.json integration)
- [x] Cost/quality trade-offs проанализированы ✅
- [x] Performance bottlenecks выявлены ✅ (QualityValidator, routing bias)
- [x] Optimization recommendations подготовлены ✅
- [x] **BONUS**: struct.json реалистичные сценарии ✅ (лучший routing баланс)

**🚨 CRITICAL ISSUES FOUND**: QualityValidator 42.9% accuracy, Ollama routing bias

### ✅ Phase 2C: Gap Analysis & Roadmap (COMPLETED)
- **Prerequisites**: Phase 2A + 2B completed ✅
- **Model**: Claude 4 Sonnet (primary) + web research
- **Duration**: 120 minutes (actual)
- **Goal**: Create prioritized improvement roadmap based on real testing + research validation
- **Status**: ✅ **COMPLETED** (2025-06-11)
- **Critical Discovery**: Integration layer opportunity, not metric reinvention

**Research Validation Completed:**
- **Existing LLM Evaluation Ecosystem**: Comprehensive analysis of 17+ frameworks
- **Major Frameworks**: DeepEval, TruLens, HELM, RAGAS, Arthur.ai, PromptLayer
- **Established Metrics**: BLEU, ROUGE, BERTScore, G-Eval, QAG, DAG evaluation approaches
- **Key Finding**: ❌ **WE ARE NOT DUPLICATING** - building smart integration layer

**Gap Analysis Results:**
```
{
  "gaps_identified": [
    "No unified quality validation for production RAG systems",
    "Limited integration between evaluation and routing decisions", 
    "Gap between evaluation metrics and actual routing quality",
    "Missing adaptive threshold management"
  ],
  "our_opportunity": "Integration layer, not reinventing metrics"
}
```

**✅ Чеклист Phase 2C (COMPLETED):**
- [x] **Step 0**: struct.json обновлен свежими данными (`llmstruct parse`) ✅
- [x] **Step 1**: Critical gaps vs nice-to-have разделены ✅
- [x] **Step 2**: Existing solutions research completed ✅ (17+ frameworks analyzed)
- [x] **Step 3**: Integration opportunities identified ✅ (QualityValidator design)
- [x] **Step 4**: Development roadmap created ✅ (Phase 2D → 3A → 3B → 3C)
- [x] **Step 5**: Smart integration architecture planned ✅
- [x] **Step 6**: User learning TODO added ✅ (RAG fundamentals)
- [x] **Step 7**: Anti-duplication validation ✅ (we build bridges, not wheels)

**📄 Output Documents:**
- ✅ `docs/gap_analysis_phase_2c.md` - Complete gap analysis with roadmap
- ✅ Session logs with research findings and conclusions
- ✅ User TODO: Learn RAG fundamentals and use cases

**🔧 struct.json Update Protocol:**
```bash
llmstruct parse --modular-index --include-ranges --include-hashes src/ -o src/struct.json
```
**📖 struct.json Reading Checkpoints:**
- После каждого крупного изменения кода
- Перед gap analysis
- При планировании архитектурных изменений

---

## 🚀 PHASE 3: Implementation Strategy (NEXT)

### 🔄 Phase 2D: Smart Integration Architecture Design (IN PROGRESS)
- **Prerequisites**: Phase 2C completed ✅ 
- **Model**: Claude 4 Sonnet (primary) + architectural analysis
- **Duration**: 90 minutes (estimated)
- **Goal**: Design detailed architecture for smart evaluation integration
- **Status**: 🔄 **IN PROGRESS** (2025-06-11)

#### ✅ Phase 2D.1: QualityValidator Enhancement (COMPLETED)
- **Model**: Gemini 2.5 Flash → Claude 4 Sonnet  
- **Duration**: 30 minutes (actual)
- **Deliverables**:
  - `predict_quality_requirements()` method ✅
  - `assess_model_capability()` method ✅  
  - DeepEval integration wrapper ✅
  - TruLens monitoring hooks ✅
- **Status**: ✅ **COMPLETED** (2025-06-11)

#### 🔄 Phase 2D.2: ModelRouter Integration (CURRENT)
- **Model**: Claude 4 Sonnet  
- **Duration**: 45 minutes (estimated)
- **Goal**: Integrate quality-aware routing logic
- **Status**: 🔄 **IN PROGRESS** (2025-06-11)

#### 🎯 Phase 2D.3: Quality Intelligence System (PENDING)
- **Model**: Claude 4 Sonnet (or o3-mini if complex)
- **Duration**: 15 minutes (estimated)
- **Goal**: Implement feedback loop system
- **Status**: 🎯 **PENDING**

**Key Design Tasks:**
1. **QualityValidator Interface Design**:
   - Integration with DeepEval/TruLens frameworks
   - Adaptive threshold management system
   - Quality-aware routing interface
   
2. **Evaluation-Routing Bridge**:
   - Router decisions based on quality predictions
   - Feedback loop: evaluation results → routing improvements
   - Real-time quality monitoring pipeline

3. **Architecture Integration**:
   - Extend existing TaskRouter with quality awareness
   - Integrate with current HandoffValidator workflow  
   - Maintain backward compatibility

**📄 Output Document**: `docs/smart_integration_architecture_phase_2d.md`

**⚠️ MANDATORY STOP**: Architecture review and approval before Phase 3A implementation

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