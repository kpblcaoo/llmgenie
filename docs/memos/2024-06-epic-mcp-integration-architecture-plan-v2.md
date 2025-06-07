# Архитектурный план v2: MCP, FastAPI и "живой" workflow engine для llmgenie

Дата: 2024-06-13
Автор: ai_assistant

---

## 1. Цели и задачи
- Построить гибкую, масштабируемую и "осознанную" систему workflow-контроля для LLM.
- Обеспечить не только enforcement (запреты), но и автоматизацию, динамику, прозрачность, ситуативное поведение.
- Централизовать управление действиями, политиками, логами, статусами через FastAPI/MCP.
- Дать LLM API для получения информации о возможностях, сценариях, политике, данных, а также для инициирования действий.
- Поддерживать расширяемость через плагины, CLI, внешние LLM/API.

---

## 2. Архитектурные компоненты
### 2.1. FastAPI-слой (workflow engine backend)
- Сердце всей автоматизации и контроля.
- REST API для LLM, MCP, CLI, Ollama, внешних моделей, плагинов.
- Централизованное хранение и обновление workflow-данных (tasks.json, meta-log, roadmap, policies и др.).
- Поддержка event-driven сценариев (webhooks, триггеры).

### 2.2. MCP-сервер (gateway к FastAPI)
- MCP-сервер реализует универсальные тулзы:
  - `get_available_actions(context)`
  - `get_workflow_state()`
  - `get_policy(policy_name)`
  - `get_context_data(key)`
  - `run_action(action, params)`
  - `update_context(key, value)`
  - `trigger_event(event, params)`
- Все вызовы MCP маршрутизируются на FastAPI.
- Мультиплексирование: одна MCP-тулза покрывает десятки/сотни сценариев через параметры.

### 2.3. Always-on правила (enforcement policies)
- Только для критичных стандартов (security, branch, logging, session management).
- Всё остальное — через MCP/FastAPI.

### 2.4. CLI, плагины, внешние сервисы
- Подключаются к FastAPI как REST endpoints, Python-модули или через event/webhook-интеграции.
- FastAPI управляет вызовами, логированием, обработкой ошибок.

---

## 3. Типы endpoints и сценарии
### 3.1. Информационные endpoints
- `GET /actions?context=...` — вернуть список разрешённых действий для текущего режима/контекста.
- `GET /workflow/state` — вернуть текущее состояние workflow, активные задачи, режимы, статусы.
- `GET /policy/{name}` — вернуть параметры/описание политики.
- `GET /context/{key}` — вернуть нужные данные из JSON (tasks, roadmap, meta-log и др.).

### 3.2. Action endpoints
- `POST /action` — инициировать действие (логирование, запуск тестов, обновление статуса, создание задачи и др.).
- `POST /context/{key}` — обновить данные (например, статус задачи, запись в meta-log).
- `POST /event` — инициировать событие (webhook, запуск CI/CD, уведомление).

### 3.3. Enforcement endpoints
- `POST /enforce` — проверить/запретить/разрешить действие по политике.
- `GET /enforcement/status` — вернуть статус enforcement для текущего workflow.

---

## 4. Примеры сценариев
- LLM вызывает `GET /actions?context=review` → получает список разрешённых действий для review-режима.
- LLM вызывает `POST /action` с action=log_mode_switch → FastAPI логирует событие, обновляет meta-log, возвращает новый список действий.
- LLM вызывает `GET /context/tasks/123` → получает данные задачи.
- LLM вызывает `POST /enforce` с policy=branch_protection, action=merge → FastAPI возвращает разрешение/запрет.
- LLM вызывает `POST /action` с action=create_task → FastAPI создаёт задачу, пишет в tasks.json, возвращает id.

---

## 5. Чеклист для внедрения (готов к переработке)
1. Создать ветку `epic/mcp-integration-v2` от develop.
2. Спроектировать и реализовать FastAPI-слой с базовыми endpoints (информационные, action, enforcement).
3. Реализовать MCP-сервер как gateway к FastAPI (минимум: get_available_actions, run_action, enforce_policy).
4. Настроить always-on правила для критичных политик.
5. Подключить CLI, плагины, внешние сервисы к FastAPI (REST, Python-модули, webhooks).
6. Протестировать сценарии: смена режима, создание задачи, логирование, enforcement.
7. Документировать API, параметры, сценарии вызова для LLM.
8. Провести пилот на 1-2 ключевых workflow (например, review + release).
9. Зафиксировать lessons learned, обновить архитектуру.
10. Постепенно расширять покрытие (таск-менеджеры, CI/CD, docs, метрики, новые плагины).

---

## 6. Best practices
- Мультиплексировать MCP-тулзы, не плодить endpoints.
- Документировать все сценарии, параметры, API для LLM.
- Централизовать хранение и обновление workflow-данных.
- Использовать event-driven подход для автоматизации.
- Минимизировать always-on правила, всё остальное — через API.
- Тестировать на Linux/Mac, учитывать баги на Windows/WSL.
- Оставлять архитектуру гибкой для доработок.

---

## 7. Риски и caveats
- MCP и custom modes развиваются, возможны баги.
- FastAPI-слой — точка отказа, требует мониторинга.
- Лимит 40 MCP-тулзов — не критичен при мультиплексировании.
- Возможны сложности с интеграцией некоторых CLI/LLM/таск-менеджеров.
- Требуется тщательная документация для LLM.

---

## 8. Рекомендации
- Внедрять FastAPI как "сердце" workflow engine.
- Строить MCP вокруг универсальных шлюзов.
- Документировать все сценарии и API.
- Постепенно расширять покрытие, фиксировать lessons learned.
- Оставлять архитектуру гибкой для изменений.

---

## 9. Ссылки и источники
- [Changelog Cursor 1.0](https://www.cursor.com/changelog)
- [Официальная документация MCP](https://docs.cursor.com/context/model-context-protocol)
- [PulseMCP — каталог MCP-серверов](https://www.pulsemcp.com/clients/cursor-ide)
- [Пример интеграции MCP с Jira (Medium)](https://medium.com/@levi_yehuda/cursor-mcp-a-5-minute-quick-start-guide-3c6f214557d5)
- [Форум Cursor: MCP, custom tools, feedback](https://forum.cursor.com/)

---

_План v2 подготовлен для гибкой доработки и обсуждения. Все предложения и сценарии приветствуются!_ 