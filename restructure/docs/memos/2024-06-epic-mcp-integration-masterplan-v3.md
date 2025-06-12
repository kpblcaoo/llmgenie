# Мастер-план v3: Реалистичное внедрение workflow engine и мультиагентности для llmgenie

**Дата:** 2024-06-XX  
**Автор:** ai_assistant (обновлено по итогам аудита, ретроспектив и lessons learned)

---

## Фаза 0. Аудит, анализ и подготовка (Epic 1)

### Цели:
- Провести автоматизированный аудит состояния проекта, архитектуры, процессов, данных и документации.
- Сверить текущее состояние с целями, best practices, архитектурными gems и требованиями.
- Сформировать pain points, refinement требований, карту данных и зон ответственности.
- Подготовить инфраструктуру для FastAPI/MCP и multi-agent orchestration.

### Статус: **ВЫПОЛНЕНО (100%)**

#### Чеклист (все файлы и отчёты перенесены в docs/memos/epic1/):
- [x] Аудит по atomic rule @230_project_auditor.mdc (чеклисты, критерии, логи)
- [x] Анализ @PROJECT_VISION.md, выявление gap (60%)
- [x] Извлечение best practices и gems из @ARCHIVE_ANALYSIS_REPORT.md
- [x] Карта компонентов, ролей, правил, связей из @project_state.json
- [x] Pain points и refinement требований (отдельный doc)
- [x] Dev-ветка и окружение для FastAPI/MCP
- [x] Все результаты аудита и анализа зафиксированы в decision log
- [x] Формализован стандарт передачи контекста (context_transfer_guide.md)
- [x] Lessons learned зафиксированы (lessons_learned_detailed)
- [x] Чеклист передачи контекста выполнен (startup prompt, файлы, тех.инфа, lessons, scope, вопросы)

---

## Фаза 1. Пилот background-агентов и handoff (Epic 2)

### Цели:
- Исследовать и опробовать background-агентов Cursor и Ollama для автоматизации рутинных задач, CI/CD, тестов, обновлений.
- Зафиксировать сценарии, ограничения, lessons learned для дальнейшей интеграции в multi-agent workflows.
- Подготовить шаблоны, инструкции и best practices для команды.

### Статус: **ВЫПОЛНЕНО (100%)**

#### Чеклист (все файлы и отчёты перенесены в docs/memos/epic2/):
- [x] Пилот Cursor background-агентов отменён из-за отсутствия privacy mode
- [x] Пилот Ollama: очередь, интеграция, фиксация результатов, сценарии, best practices
- [x] Lessons learned и ограничения зафиксированы
- [x] Подготовлены рекомендации для MCP, knowledge base и автоматизации пайплайна

---

## Фаза 2. Стандартизация и автоматизация правил, handoff и передачи контекста (Epic 3)

### Цели:
- Внедрить стандартизированную, автоматизированную систему управления atomic rules, handoff между сессиями/чатами и передачей контекста, используя @rules_manifest.json как центральный реестр.

### Статус: **ВЫПОЛНЕНО (100%)**

#### Чеклист (все файлы и отчёты перенесены в docs/memos/epic3/):
- [x] Актуализация и аудит правил, @rules_manifest.json
- [x] Интеграция lessons learned и best practices в .cursor/rules/ и knowledge base
- [x] Автоматизация handoff и передачи контекста (MCP/CLI endpoint — реализован прототип, требуется production)
- [x] Документирование и прозрачность (decision log, session log, docs)
- [x] Контроль качества и ретроспектива (code review, .mdc_ work protocol, финальная валидация manifest)

---

## Фаза 3. MCP enforcement, always-on policy, knowledge base, orchestration (НОВЫЕ ЭПИКИ)

### Epic 4: MCP/CLI enforcement & handoff validation

**Цели:**
- Production-реализация MCP endpoint для автоматической проверки completeness handoff-пакета (минимум 5 файлов, prompt, контрольные вопросы)
- Интеграция с CI/CD и FastAPI
- Автоматический отчёт о качестве передачи (score, gaps)

**Статус:** [x] ВЫПОЛНЕНО (2025-01-05)

#### Чеклист (вести все файлы и отчёты в docs/memos/epic4/):
- [x] Проектирование и реализация production MCP endpoint для валидации handoff
- [x] Интеграция с CI/CD и FastAPI
- [x] Автоматический отчёт о качестве передачи (score, gaps)
- [x] Документирование всех решений, проблем, lessons learned
- [x] Чеклисты, шаблоны, инструкции для команды

### Epic 5: MCP-Ollama Integration для Task Offloading (ОБНОВЛЕН)

**Цели:**
- Production-ready интеграция MCP с локальной Ollama для intelligent task routing
- Smart classification: complex reasoning → Claude, routine tasks → Ollama  
- Context preservation system с quality validation pipeline
- Performance analytics, cost optimization, multi-agent orchestration

**Статус:** [ ] ПЛАНИРОВАНИЕ ЗАВЕРШЕНО (план v2.0 готов в docs/memos/epic5/)

#### Planning completed (ready for implementation):
- [x] Deep research MCP + Ollama integration (production examples found)
- [x] Architecture v2.0: Smart Task Router + Context Preservation + Performance Analytics  
- [x] Technical implementation plan: 3-tier approach (Foundation → Smart Routing → Production)
- [x] Success metrics, risk mitigation, timeline корректировка
- [x] Integration с Epic 4 infrastructure, documentation v2.0

#### Implementation tasks (Epic 5 scope):
- [ ] Ollama function calling setup + models download
- [ ] Smart Task Classification Engine implementation
- [ ] Quality Validation Pipeline с fallback mechanisms  
- [ ] Task Router с intelligent routing logic
- [ ] Context Preservation System для model switching
- [ ] Performance Monitoring & Analytics dashboard
- [ ] Multi-Agent Orchestration layer
- [ ] Production deployment + documentation

---

### Epic 6: Always-on policy enforcement

**Цели:**
- Автоматизация enforcement для branch policy, logging, security (atomic rules 009, 001, 400)
- Интеграция с MCP и workflow engine

**Статус:** [ ] Не начато

#### Чеклист (вести все файлы и отчёты в docs/memos/epic6/):
- [ ] Проектирование и реализация enforcement для branch policy, logging, security
- [ ] Интеграция с MCP и workflow engine
- [ ] Документирование всех решений, проблем, lessons learned
- [ ] Чеклисты, шаблоны, инструкции для команды

---

### Epic 7: Knowledge base & lessons learned automation

**Цели:**
- Автоматизация сбора, хранения и поиска best practices, lessons learned, решений (core/006, 011)
- API для доступа к lessons и best practices

**Статус:** [ ] Не начато

#### Чеклист (вести все файлы и отчёты в docs/memos/epic7/):
- [ ] Проектирование и реализация автоматизации knowledge base
- [ ] API для lessons и best practices
- [ ] Документирование всех решений, проблем, lessons learned
- [ ] Чеклисты, шаблоны, инструкции для команды

---

### Epic 8: Multi-agent handoff & orchestration

**Цели:**
- Production-реализация multi-agent handoff (coder → librarian → reviewer), автоматизация передачи метаданных, логов, decision log
- Прототип message bus/оркестратора для параллельных веток

**Статус:** [ ] Не начато

#### Чеклист (вести все файлы и отчёты в docs/memos/epic8/):
- [ ] Production-реализация multi-agent handoff
- [ ] Прототип message bus/оркестратора
- [ ] Документирование всех решений, проблем, lessons learned
- [ ] Чеклисты, шаблоны, инструкции для команды

---

## Lessons learned (ключевые):

- **Foundation first:** Без тестов, dev dependencies и CI/CD невозможна качественная разработка multi-agent систем.
- **Checkpoints & context transfer:** Регулярные чекпоинты, структурированные логи, стандарт передачи контекста — критичны для handoff и командной работы.
- **Realistic scope:** 60% gap между vision и реальностью — норма, нужен phased rollout и регулярные reality checks.
- **Automation & enforcement:** Прототипы автоматизации handoff и policy enforcement есть, но требуется production-реализация.
- **Документирование:** Все best practices, lessons learned и решения должны фиксироваться централизованно (knowledge base, session log).

---

## Критерии успеха для новых эпиков:

- Production-реализация MCP/CLI enforcement и handoff validation
- Always-on policy enforcement (branch, logging, security)
- Knowledge base с API для lessons learned и best practices
- Multi-agent handoff с автоматизацией передачи и orchestration

---

## Рекомендации:

1. **Не закрывать эпики без production-артефактов (endpoint, CLI, docs, тесты, интеграция в workflow).**
2. **Ввести регулярный аудит соответствия atomic rules (epic 5).**
3. **Фиксировать lessons learned и best practices централизованно (epic 6).**
4. **Для каждого этапа — production-критерии, не закрывать чеклист без реального результата.**
5. **Планировать phased rollout с регулярными reality checks и checkpoint culture.** 