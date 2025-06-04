# Knowledge Base: Common Best Practices & Workflow

---

## 1. Ведение базы знаний (knowledge base)
- Для каждой среды/модели/интеграции — отдельный файл (cursor.md, ollama.md, openai_api.md, vscode_continue.md, vscode_copilot.md).
- В каждом файле: дата/время поиска или обновления, краткое описание, ссылки на источники, примеры, внедрённые решения, TODO по обновлению.
- Вести временные метки и last_reviewed для ревизии актуальности.
- Все найденные best practices, workflow, решения — фиксировать в knowledge base или decision memos.

## 2. User rules: советы и best practices
- User rules должны быть лаконичными, конкретными, без лишних деталей.
- В user rules — только ссылки и напоминания (например, "Consult knowledge base in knowledge/ and data/knowledge/ before searching externally. Update base if new info is found.").
- Не дублировать сложные правила — выносить их в project rules (.mdc) или knowledge base.
- Регулярно ревизировать user rules, чтобы не было устаревших или дублирующих инструкций.

## 3. Project rules: структура и автоматизация
- Все enforceable/manual правила — только в .mdc-файлах с корректным frontmatter (description, globs, alwaysApply).
- Использовать вложенные каталоги для масштабируемости: core/, workflows/, roles/, languages/, security/, templates/.
- Для agent requested — чёткие, лаконичные descriptions.
- Для auto attached — globs, для always — alwaysApply: true.
- Документировать структуру в ONBOARDING и project_state.json.
- Регулярно ревизировать и избегать дублирования между каталогами.

## 4. Agent requested: гибридные сценарии
- Использовать для ситуативных, ролевых, узких сценариев (code review, docs, security audit и др.).
- Пример frontmatter:
  ```
  ---
  description: When reviewing code, enforce our code review checklist
  alwaysApply: false
  ---
  # Code Review Checklist
  ...
  ```
- Важно: description должен быть чётким и лаконичным, чтобы AI корректно подгружал правило.

## 5. Workflow по ревизии и обновлению
- При поиске новой информации — сразу фиксировать в knowledge base.
- При планировании — смотреть, что уже найдено, что требует обновления.
- AI/CLI может предлагать обновить устаревшие записи или напоминать о ревизии.
- Для каждой записи — временная метка, источник, TODO по обновлению.

## 6. Naming conventions и структура
- Использовать префиксы и нумерацию для порядка и приоритета (core, workflows, roles, languages, security, templates).
- В каждом каталоге — только .mdc-файлы с корректным frontmatter.
- Документировать структуру и naming в ONBOARDING и project_state.json.

## 7. Интеграция с AI/ассистентом
- AI должен использовать knowledge base для поиска best practices и решений до обращения к внешним источникам.
- Все новые best practices и workflow — фиксировать в knowledge base или decision memos.
- При обновлении workflow — добавлять запись в knowledge/common.md и data/knowledge/common.json.

---

_Этот файл — основа для ведения базы знаний, автоматизации, ревизии и передачи best practices в проекте. Регулярно обновляйте и ревизируйте._ 