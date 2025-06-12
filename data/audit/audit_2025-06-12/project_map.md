# Карта связей проекта llmgenie (2025-06-12)

## 1. Кодовая база (src/)
- src/llmgenie — CLI, API, TaskRouter, Orchestration, MCP-интеграция
- src/rag_context — RAG-инфраструктура, session context, code discovery
- src/struct_tools — Архитектурный анализ, struct.json, modular index

## 2. Данные и манифесты
- data/tasks.json, data/ideas.json, data/insights.json, data/prs.json — основные project data
- data/project_manifest.json — реестр всех project data файлов
- struct.json, src/.llmstruct_index — архитектурная карта кода

## 3. Базы знаний
- data/knowledge/* — AI-база знаний (паттерны, code extraction)
- docs/knowledge/* — Human-база знаний (гайды, best practices)

## 4. Документация
- docs/ONBOARDING_LLMSTRUCT.md, docs/BEST_PRACTICES_LLMSTRUCT.md — гайды, лучшие практики
- docs/WORKFLOW_LLMSTRUCT_EPIC_MANAGEMENT.md — workflow по эпикам
- docs/security_audit_checklist.md, docs/code_review_checklist.md — чеклисты

## 5. Правила и enforcement
- .cursor/rules/rules_manifest.json — манифест всех atomic rules
- .cursor/rules/core/*, .cursor/rules/workflows/* — enforcement, branch policy, code review, context transfer

## 6. Автоматизация и CI/CD
- .github/workflows/* — CI/CD workflow
- scripts/* — скрипты автоматизации, интеграций

## 7. Логирование и мониторинг
- data/logs/sessions/* — session logs, event_log, tech_log
- data/insights.json — lessons learned, ретроспектива

## 8. Связи и интеграции
- project_manifest.json ↔ все project data, knowledge, документация
- struct.json ↔ src/, архитектурный анализ, code review
- rules_manifest.json ↔ enforcement, workflow, автоматизация
- prompts_collection.json ↔ workflow, автоматизация, AI
- MCP/RAG/struct_tools ↔ src/, автоматизация, архитектурный анализ

---

## Actionable:
- [ ] Проверить актуальность и связи всех элементов
- [ ] Устранить дубли, пробелы, неиспользуемые файлы
- [ ] Связать базы знаний с кодом и документацией через project_manifest.json
- [ ] Автоматизировать enforcement и интеграции (workflow, CI/CD, MCP)
- [ ] Регулярно проводить аудит и чистку структуры 