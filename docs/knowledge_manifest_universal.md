# Universal Knowledge Manifest & Migration Guide

**Date**: 2025-01-05  
**Epic**: json_audit_effectiveness_2025  
**Task**: TSK-AUDIT-006  

## Atomic Rules Architecture (2025)

### 1. Структура atomic-правил
- Каждый .mdc_ файл — atomic: 1 задача, 1 зона ответственности, тестируемость, без побочных эффектов
- Все правила описаны в rules_manifest.json (id, file, description, @-references, fallback, last_updated)
- @-references только для расширения, кросс-ссылок, справки, логирования
- Fallback: log to temp file and notify rules_engineer
- Все справочные материалы вынесены в docs/

### 2. Каталоги и нумерация
- core/ — базовые best practices, context, logging, policy
- roles/ — atomic-правила для ролей (knowledge_engineer, reviewer, rules_engineer)
- workflows/ — atomic-правила для процессов (code_review и др.)
- security/ — atomic-правила для аудита
- templates/ — atomic-правила для шаблонов (commit, docs и др.)

### 3. Manifest и кросс-ссылки
- rules_manifest.json — единый источник правды для всех atomic-правил
- Для каждого правила: id, file, description, @-references, fallback, last_updated
- Все @-references валидируются и документируются
- Нет циклических или битых ссылок

### 4. Fallback-логика
- Если session_log или справочный файл недоступен — log to temp file and notify rules_engineer
- Все ошибки и обходы фиксируются в session_log

### 5. Инструкции для команды
- Все изменения только в .mdc_ копиях (atomic-правила)
- После тестов и ревью — ручная замена оригиналов
- Все новые правила и справки — только через manifest и docs/
- Для новых участников: см. ONBOARDING_LLMSTRUCT.md
- Для ревизии: используйте rules_manifest.json и dependency-таблицы

### 6. Примеры паттернов @-reference
```yaml
## @-References
- @session_log: For logging all actions
- @docs/code_review_checklist.md: For full checklist
- @rules_manifest.json: For manifest and dependency tables
```

### 7. Multi-environment поддержка
- Все atomic-правила и manifest легко адаптируются для Cursor, VSCode, CLI, API
- Универсальные идентификаторы и структура
- Адаптеры для других сред — через manifest и docs/

---

## Related Files:
- Manifest: .cursor_new/rules/rules_manifest.json
- Atomic Rules: .cursor_new/rules/*/*mdc_
- Docs: docs/
- Session Log: data/logs/sessions/session_context_optimization_2025_01_05.jsonl
- ONBOARDING: docs/ONBOARDING_LLMSTRUCT.md 