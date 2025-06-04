# Записка: Draft YAML/JSON-структуры для enforceable/manual правил .cursor/rules

---

## 1. branch_policy
**Назначение:** Политика ветвления, запрет прямых изменений в develop, только через ветки/PR
**Draft-структура:**
```yaml
name: branch_policy
alwaysApply: true
description: "Enforce branch policy for all work."
content: |
  - Do not make any changes outside of tasks, epics, or ideas unless you are in an active session (a new branch for a task or epic).
  - No substantial changes are allowed directly in develop.
  - All work must be done in a dedicated branch and session.
  - All merges to develop must go through a pull request and review.
  - Emergency hotfixes must be logged and justified in event_log/meta-log.
```
**Комментарий:** enforceable, применяется всегда.

---

## 2. session_management
**Назначение:** Сессионный контроль, логирование, шаблоны логов, elastic workflow
**Draft-структура:**
```yaml
name: session_management
alwaysApply: true
description: "Session control and logging."
content: |
  - Всегда работай в активной сессии, связанной с эпиком
  - Логируй все ключевые события (старт, пауза, завершение, переключение)
  - Используй elastic workflow: /go task → фокусированная сессия → /back с резюме
  - AI должен сверяться с meta-log при переключении сессий
  - Для крупных задач создавай отдельные сессии
  - Для всех рабочих ситуаций (эпики, планирование, обсуждение, debug, тесты и др.) используется сессионный контроль: отдельные event_log, tech_log, meta-log для каждой сессии.
  - Именование: data/sessions/<session_type>_<date>_<custom>.json
  - При смене типа работы — создаются новые логи.
  - Логируется каждое взаимодействие: действия пользователя, AI, системные события.
  - AI обязан подмечать и фиксировать возможности улучшения workflow (insights.json или отдельный лог).
  - Регулярно анализируйте логи для выявления паттернов и улучшений.
```
**Комментарий:** enforceable, применяется всегда.

---

## 3. workflow_modes
**Назначение:** Режимы работы, переключение, фильтрация, логирование
**Draft-структура:**
```yaml
name: workflow_modes
globs: ["*.md", "*.py"]
description: "Workflow modes and context tags."
content: |
  - Основные режимы: [discuss], [meta], [code], [debug], [docs], [test]
  - Комбинированные режимы: [code][debug], [discuss][meta], [docs][meta]
  - Best practices: явно указывай режим в начале сессии или задачи, переключай режимы по мере смены этапа работы, используй режимы для фильтрации задач, логов, инсайтов, AI должен обновлять llm_context и attention_marker при смене режима, для автоматизации и анализа всегда логируй смену режима
```
**Комментарий:** enforceable/manual, применяется к md/py-файлам, может быть вызван вручную.

---

## Для остальных файлов:
- **logging-and-retrospective.mdc, ai-capabilities.mdc, project_scope.mdc, cli-commands.mdc, ai_best_practices.mdc** — оформить как справочники или global rules, добавить инструкции по их использованию в документацию и onboarding.

---

_Проверь draft-структуры, дай комментарии или правки. После согласования — переход к преобразованию и тестированию._ 