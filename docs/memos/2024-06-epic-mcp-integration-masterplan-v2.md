# Мастер-план v2: Поэтапное внедрение "живого" workflow engine и мультиагентности для llmgenie

Дата: 2024-06-13
Автор: ai_assistant

---

## Фаза 0. Аудит, анализ и подготовка
### Цели:
- Провести автоматизированный аудит состояния проекта, архитектуры, процессов, данных и документации.
- Сверить текущее состояние с целями, best practices, архитектурными gems и требованиями.
- Сформировать pain points, refinement требований, карту данных и зон ответственности.
- Подготовить инфраструктуру для FastAPI/MCP и multi-agent orchestration.

### Чеклист:
- [ ] Запустить аудит по atomic rule @230_project_auditor.mdc (чеклисты, критерии, логи).
- [ ] Проанализировать @PROJECT_VISION.md (цели, критерии успеха, стратегические направления).
- [ ] Извлечь архитектурные gems и best practices из @ARCHIVE_ANALYSIS_REPORT.md.
- [ ] Собрать карту компонентов, ролей, правил, связей из @project_state.json.
- [ ] Сформировать pain points и refinement требований (отдельный doc).
- [ ] Подготовить dev-ветку и окружение для FastAPI/MCP.
- [ ] Зафиксировать результаты аудита и анализа в decision log.

### Технологии:
- Python, FastAPI, MCP, json, git, docs, автоматизация аудита.

---

## Фаза 1. MVP: Workflow engine, multi-agent handoff, enforcement, background-агенты (пилот)
### Цели:
- Реализовать FastAPI-слой для управления workflow, логами, данными, ролями.
- Интегрировать MCP-сервер с мультиплексированными тулзами.
- Прототип multi-agent handoff: coder → librarian → reviewer (логирование, передача метаданных, автоматическое переключение ролей).
- Always-on enforcement для критичных политик (security, branch, logging).
- Внедрить decision log и structured decision making.
- **Провести исследование и пилотирование background-агентов Cursor для автоматизации рутинных задач, CI/CD, тестов, обновлений.**

### Чеклист:
- [ ] Реализовать FastAPI backend с базовыми endpoints:
    - [ ] /actions
    - [ ] /workflow/state
    - [ ] /policy/{name}
    - [ ] /context/{key}
    - [ ] /action
    - [ ] /enforce
- [ ] Реализовать MCP-сервер (gateway к FastAPI):
    - [ ] get_available_actions
    - [ ] run_action
    - [ ] enforce_policy
- [ ] Настроить always-on правила (security, branch, logging).
- [ ] Прототип multi-agent handoff (coder → librarian → reviewer):
    - [ ] Формат метаданных и логов
    - [ ] API для передачи состояния и handoff
    - [ ] Decision log для фиксации решений и передачи
    - [ ] Документация handoff
- [ ] Логирование и восстановление сессий (session_log, meta-log).
- [ ] Чеклисты и decision list для контроля качества.
- [ ] Документировать API, сценарии, роли, процессы.
- [ ] **Провести пилот background-агентов: делегировать аудит, тесты, обновления, CI/CD, зафиксировать сценарии и lessons learned.**

#### Вторичный чеклист: Что можно сделать за один эпик с AI
- [ ] Спроектировать и реализовать FastAPI backend (минимум: /actions, /action, /workflow/state, /enforce).
- [ ] Реализовать MCP-сервер с мультиплексированными тулзами.
- [ ] Настроить always-on enforcement для security/branch/logging.
- [ ] Прототип multi-agent handoff: логирование работы кодера, передача метаданных библиотекарю, ревью.
- [ ] Документировать сценарии и API.
- [ ] **Провести пилот background-агентов на простых задачах.**

### Технологии:
- Python, FastAPI, MCP, json, git, docs, Cursor background agents.

---

## Фаза 2. Knowledge base, memory, расширение ролей и автоматизации, массовое внедрение background-агентов
### Цели:
- Внедрить базы знаний, persistent memory, автоматизацию сбора и обновления данных.
- Расширить handoff: аналитик, devops, интеграция с таск-менеджерами.
- Внедрить agent access control, иерархию ролей, CLI для управления агентами.
- **Массово внедрить background-агентов для автоматизации тестов, CI/CD, миграций, обновлений, параллельных задач.**

### Чеклист:
- [ ] Реализовать knowledge base (json/db, API для LLM, автоматизация сбора знаний).
- [ ] Внедрить persistent memory (memories, базы данных, хранение связей и решений).
- [ ] Автоматизация сбора и обновления данных (логов, связей, статусов, решений).
- [ ] Расширить handoff: аналитик, devops, таск-менеджеры.
- [ ] Внедрить agent access control и иерархию ролей (lead/worker, escalation protocols).
- [ ] Реализовать CLI для управления агентами и orchestration.
- [ ] Документировать интерфейсы, сценарии, процессы.
- [ ] **Интегрировать background-агентов в multi-agent workflows, автоматизацию CI/CD, тестов, миграций.**

### Технологии:
- FastAPI, json/db, MCP, CLI, docs, Cursor background agents, интеграция с таск-менеджерами.

---

## Фаза 3. Оркестрация, слои контекста, параллельные ветки, мультиагентность, advanced background-агенты
### Цели:
- Внедрить оркестратор для управления ролями, потоками, сессиями, параллельными ветками.
- Реализовать слои контекста, message bus, автоматическую маршрутизацию handoff.
- Поддержка параллельных веток обсуждения/разработки, возврата к ним.
- Внедрить smart wrapper pattern, context-driven execution, fallback mechanisms.
- **Использовать background-агентов для сложных сценариев orchestration, распределённой работы, автоматического handoff между ролями, интеграции с внешними сервисами.**

### Чеклист:
- [ ] Реализовать оркестратор (FastAPI/microservices/message bus).
- [ ] Слои контекста: session, project, global.
- [ ] Автоматическая маршрутизация handoff между ролями и потоками.
- [ ] Поддержка параллельных веток и возврата к ним.
- [ ] Внедрить smart wrapper pattern для агентов.
- [ ] Документировать архитектуру, сценарии, процессы.
- [ ] **Интегрировать background-агентов в advanced multi-agent workflows, orchestration, распределённую работу.**

### Технологии:
- FastAPI, message bus, microservices, MCP, CLI, docs, Cursor background agents.

---

## Фаза 4. Мультидоменность, масштабирование, интеграция с внешними системами
### Цели:
- Расширить архитектуру на новые домены: наука, бизнес, ассистенты, корпоративные решения.
- Поддержка новых типов данных, ролей, сценариев, multi-tenant agent systems.
- Масштабирование и интеграция с внешними системами, API, плагинами.
- Внедрить enterprise agent management, BI для агентских операций, стратегическое планирование.

### Чеклист:
- [ ] Абстрагировать доменные сценарии и роли.
- [ ] Поддержка новых типов данных и API.
- [ ] Интеграция с внешними системами (API, плагины, сервисы).
- [ ] Внедрить multi-tenant agent systems, BI, стратегическое планирование.
- [ ] Документировать best practices, lessons learned, стратегию развития.

### Технологии:
- FastAPI, MCP, плагины, внешние API, BI-инструменты, docs, Cursor background agents.

---

## Рекомендации по обучению и best practices
- Проводить пилоты background-агентов на простых задачах, фиксировать сценарии и lessons learned.
- Постепенно усложнять сценарии: параллельные задачи, автоматический handoff, интеграция с orchestration.
- Документировать все сценарии, шаблоны environment.json, примеры автоматизации.
- Обучать команду phased rollout, multi-agent workflows, orchestration, CI/CD с background-агентами.
- Использовать возможности Cursor (rules, MCP, background agents, memories, BugBot, custom tools) максимально эффективно для автоматизации и контроля.

---

## Итог
- Мастер-план v2 теперь учитывает background-агентов Cursor, их пилотирование, массовое внедрение и интеграцию в multi-agent workflows и orchestration.
- Все фазы предполагают поэтапное внедрение, фиксацию lessons learned, расширение архитектуры и интеграцию новых идей.
- Структура готова к доработке и детализации под новые требования и домены. 