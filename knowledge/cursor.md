---
date_created: 2024-06-09
source: user/assistant discussion, epic rule automation
---
# Knowledge Base: Cursor IDE

## 1. Project rules (.cursor/rules)
- Только .mdc-файлы с frontmatter (description, globs, alwaysApply).
- Вложенные каталоги поддерживаются (core/, workflows/, roles/ и т.д.).
- Примеры frontmatter для всех типов правил.
- Особенности работы agent requested, auto attached, manual, always.

## 2. User rules
- Только plain text, глобальны для всех проектов.
- Советы по формулировке, ограничения, best practices.

## 3. Инсайты и баги
- В каких случаях rules не применяются (например, из-за длины промпта, конфликтов, багов в старых версиях).
- Как ревизировать и обновлять правила.
- Как использовать context picker и UI для управления правилами.

## 4. Workflow по ревизии и автоматизации
- Как ревизировать правила, избегать дублирования, поддерживать naming.
- Как интегрировать с AI/ассистентом и decision memos.

## 5. Источники и ссылки
- Документация Cursor, форумы, найденные best practices, примеры.

## 6. TODO/обновления
- Что требует ревизии, какие правила устарели, что добавить/обновить.

## 7. Анализ текущих автоматизированных правил
- Уже автоматизированы: branch_policy, workflow_modes, session_management, ai_best_practices, project_scope, ai-capabilities, cli-commands, logging-and-retrospective.
- Используются: alwaysApply (для базовых стандартов), globs (для файловых паттернов), agent requested (для ситуативных и ролевых сценариев).
- Вложенная структура каталогов поддерживается (core, workflows, roles, languages, security, templates).
- Naming: префиксы и нумерация для порядка и приоритета.

## 8. Примеры frontmatter для всех типов правил
### AlwaysApply (базовые стандарты)
```
---
description: Enforce branch policy for all work
alwaysApply: true
---
# Branch Policy
...
```
### Globs (файловые паттерны)
```
---
description: Apply Python code style to all .py files
globs:
  - "**/*.py"
---
# Python Code Style
...
```
### Agent Requested (ситуативные/ролевые)
```
---
description: When reviewing code, enforce our code review checklist
alwaysApply: false
---
# Code Review Checklist
...
```

## 9. Workflow ревизии и добавления новых правил
- Для базовых стандартов — использовать alwaysApply.
- Для файловых паттернов — использовать globs.
- Для ситуативных, ролевых, узких сценариев — использовать agent requested с чётким description.
- Все новые правила писать с расширением .md, после ревизии переименовывать в .mdc.
- Регулярно ревизировать правила на дубли, избыточность, общность описаний.
- Документировать структуру и изменения в onboarding и project_state.json.
- Новые инсайты и решения фиксировать в decision memos с датой и источником.

## 10. Итоги и lessons learned по decision memos
- Вся структура каталогов, draft-форматы, workflow ревизии и автоматизации, best practices и сценарии agent requested — зафиксированы в decision_memos (см. structured_drafts_01.md, structured_analysis_01.md, structured_checklist.md, cursor_rules_checklist.md, agent_requested_analysis_01.md).
- Для enforceable/manual правил — использовать frontmatter с alwaysApply, globs, description, content.
- Для ситуативных/ролевых — agent requested с чётким description.
- Workflow ревизии: анализ, преобразование, тестирование, обновление документации, архивация.
- Lessons learned: регулярная ревизия, автоматизация, прозрачность, человеко-центричный подход.
- Рекомендации: внедрять автоматическую ревизию, расширять enforcement, интегрировать с CI/CD и внешними платформами.
- Все новые правила оформлять как .md с frontmatter, после ревизии переименовывать в .mdc.
- Документировать изменения в onboarding, project_state.json, rules_manifest.json.

## 11. Финализация: переход на новую структуру правил
- Вся система переведена на новую структуру .cursor/rules (core, workflows, roles, languages, security, templates).
- Все правила оформлены с frontmatter (description, alwaysApply, globs, agent requested).
- Workflow ревизии, рекомендации и lessons learned зафиксированы в ONBOARDING_LLMGENIE.md, project_state.json, rules_manifest.json, decision memos.
- Регулярная ревизия, автоматизация и прозрачность — основа поддержки системы.
- Все новые задачи и доработки фиксировать в tasks.json.
- Для новых участников: см. ONBOARDING_LLMGENIE.md и decision_memos/* для полного контекста.

_Сессия по переходу на новую структуру правил завершена. Все дальнейшие задачи — в tasks.json._

---

_См. decision_memos/* для подробностей и истории обсуждений._

_Этот файл содержит все специфичные для Cursor IDE практики, инсайты, workflow и баги. Универсальные best practices — в knowledge/common.md. Все новые инсайты по Cursor фиксируются здесь и в decision memos с датой и источником._ 

_Актуализировано с учётом decision_memos/cursor_rules_structure_proposal_01.md и decision_memos/cursor_rules_agent_requested_analysis_01.md._ 