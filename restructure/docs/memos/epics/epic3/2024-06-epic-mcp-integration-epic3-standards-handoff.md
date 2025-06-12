# Эпик 3: Стандартизация и автоматизация правил, handoff и передачи контекста

**Цель:**
Внедрить стандартизированную, автоматизированную систему управления atomic rules, handoff между сессиями/чатами и передачей контекста, используя @rules_manifest.json как центральный реестр.

---

## Чеклист эпика

### 1. Актуализация и аудит правил ✅
- [x] Ознакомиться с содержимым @rules_manifest.json (структура, ссылки, актуальность).
- [x] Сверить все существующие atomic rules с их реализацией в .cursor/rules/ и документацией.
- [x] Проверить наличие и корректность @-references и cross-links для всех правил.
- [x] Зафиксировать устаревшие, дублирующие или неиспользуемые правила (отметить для рефакторинга/удаления).
- [x] Проверить, что все правила имеют fallback и инструкции для логирования.

### 2. Интеграция lessons learned и best practices
- [x] Извлечь lessons learned по handoff и передаче контекста из docs/memos/2024-06-epic-mcp-integration-masterplan-v2.md и context_transfer_guide.md.
- [x] Зафиксировать новые best practices в .cursor/rules/ и knowledge base.
- [x] Обновить/создать atomic rule для передачи контекста между сессиями (ссылаясь на context_transfer_guide.md).

### 3. Автоматизация handoff и передачи контекста ✅
- [x] Спроектировать и реализовать MCP/CLI endpoint для автоматической проверки completeness пакета передачи (минимум 5 файлов, prompt, контрольные вопросы).
- [x] Добавить автоматическую валидацию передачи контекста в workflow (CI/CD или MCP).
- [x] Зафиксировать шаблон handoff-пакета и инструкции для команды.

### 4. Документирование и прозрачность ✅
- [x] Обновить документацию по atomic rules, handoff и передачам контекста (docs/ и .cursor/rules/).
- [x] Зафиксировать все изменения и решения в decision log и session log.
- [x] Подготовить summary и lessons learned по результатам эпика.

### 5. Контроль качества и ретроспектива ✅
- [x] Провести code review и аудит новых/обновлённых правил (использовать workflows/100_code_review.mdc_).
- [x] **Применить .mdc_ work protocol:** переименовать все .mdc_ файлы в .mdc после review.
- [x] **Обновить rules_manifest.json:** изменить все file references с .mdc_ на .mdc.
- [x] Провести финальную валидацию rules_manifest.json (no cycles, valid references).
- [x] Провести ретроспективу: что улучшилось, какие проблемы остались, что автоматизировать дальше.

---

## Ключевые артефакты для handoff и ссылок:
- @rules_manifest.json
- .cursor/rules/ (atomic rules)
- docs/memos/2024-06-epic-mcp-integration-masterplan-v2.md
- data/audit/context_transfer_guide.md
- docs/memos/2024-06-epic-mcp-integration-epic1-phase0.md
- docs/memos/2024-06-epic-mcp-integration-epic2-bg-agents-pilot.md
- @project_state.json
- session log, decision log

---

## Startup prompt для новой сессии

```
[discuss][meta] Запускаю Эпик 3: стандартизация и автоматизация правил, handoff и передачи контекста.

- Центральный реестр правил: @rules_manifest.json
- Lessons learned и best practices интегрированы из предыдущих фаз (см. masterplan v2, context_transfer_guide.md)
- Цель: автоматизировать handoff, передачу контекста, поддерживать актуальность и прозрачность atomic rules.
- Ключевые артефакты и чеклист — см. выше.

Готов к уточнению задач и старту работы!
``` 