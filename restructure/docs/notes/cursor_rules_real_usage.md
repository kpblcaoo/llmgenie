# 🧠 Как заставить Cursor AI реально следовать правилам: методика для llmstruct

## 1. Проблема
Cursor поддерживает мощную систему project rules (.mdc), user rules и memories. На практике агент часто игнорирует даже критические правила, если считает их нерелевантными, или если их слишком много/они нечеткие. Это приводит к потере дисциплины, ошибкам, нарушению workflow и даже потере данных.

## 2. Причины игнорирования правил
- Слишком много правил — агент "теряется" и выбирает только часть.
- Слишком общие или длинные descriptions — агент не понимает, когда применять.
- Нет alwaysApply: true — правило не попадает в контекст.
- Изменения в правилах не вступают в силу без перезапуска чата.
- User Rules не используются для критических инструкций.
- Агенту разрешено "решать", что релевантно — и он часто ошибается.

## 3. Рекомендации для стабильной работы правил

### A. Минимализм и конкретика
- Оставь только самые важные правила (workflow, безопасность, session control).
- Каждое правило — отдельный .mdc файл, не более 10-20 строк.
- Description всегда начинается с "USE WHEN ..." или "ALWAYS ...".

### B. Критические правила — только alwaysApply: true
```
---
description: ALWAYS enforce workflow discipline and session logging
globs:
alwaysApply: true
---
```

### C. User Rules — дублируй туда ключевые инструкции
В Cursor Settings > Rules добавь:
```
ALWAYS:
- Check ai_workflow.json at session start
- Start session log before any work
- Use [meta][code][debug] modes
- Log all actions in event_log/tech_log/meta-log
- NEVER delete files without explicit user permission
```

### D. Перезапуск чата после изменений
После любого изменения в .mdc — Command-N (новый чат).

### E. Проверка применения
В начале каждой сессии спроси у Cursor: "Какие правила сейчас в контексте?"  Если нужного нет — перезапусти чат.

### F. Встроенные напоминания
Включи в User Rules: "If you have not started a session log, prompt the user to do so before any work."

### G. Регулярный аудит
Раз в неделю/спринт — проверяй, какие правила реально работают, а какие игнорируются.  Удаляй или переписывай неработающие.

## 4. Пример минимального набора правил для llmstruct

### .cursor/rules/workflow_enforcement.mdc
```
---
description: ALWAYS enforce workflow discipline and session logging
globs:
alwaysApply: true
---
- Check ai_workflow.json at session start
- Start session log before any work
- Use [meta][code][debug] modes
- Log all actions in event_log/tech_log/meta-log
- NEVER delete files without explicit user permission
```

### User Rules (Cursor Settings > Rules)
```
ALWAYS:
- Check ai_workflow.json at session start
- Start session log before any work
- Use [meta][code][debug] modes
- Log all actions in event_log/tech_log/meta-log
- NEVER delete files without explicit user permission
If you have not started a session log, prompt the user to do so before any work.
```

## 5. Что делать, если агент всё равно игнорирует правила?
- В начале каждой сессии вручную вставляй ключевые workflow правила в prompt.
- Используй legacy `.cursorrules` для критических инструкций (иногда работает надёжнее).
- Пиши issue/feedback в Cursor — система развивается, баги бывают.

## 6. Резюме
- Проблема не в правилах, а в дисциплине применения.
- Минимализм, конкретика, alwaysApply, user rules, ручной контроль — вот что реально работает.
- Не бойся вручную напоминать агенту о правилах — это часть реального advanced workflow. 