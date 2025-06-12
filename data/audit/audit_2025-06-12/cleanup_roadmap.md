# Actionable Roadmap для чистки и развития llmgenie (2025-06-12)

## 1. Автоматизация enforcement-правил
- [ ] Внедрить pre-commit и CI/CD enforcement для branch policy, code review, commit message, context transfer
- [ ] Интегрировать MCP/RAG/struct_tools в автоматизацию (workflow, тесты, архитектурный анализ)

## 2. Связи и синхронизация knowledge
- [ ] Связать AI и human базы знаний с кодом и документацией через project_manifest.json
- [ ] Добавить сквозные ссылки и автоматическую синхронизацию knowledge

## 3. Чистка структуры
- [ ] Удалить дубли, устаревшие и неиспользуемые файлы (код, данные, документация)
- [ ] Провести ревизию всех project data и knowledge файлов

## 4. Покрытие workflow-этапов
- [ ] Добавить промты и автоматизацию для всех этапов workflow (pause_restore, handoff_validation, rag_enhancement_workflow)
- [ ] Связать чеклисты из документации с промтами и автоматизацией

## 5. Регулярный аудит и поддержка прозрачности
- [ ] Ввести регулярный чеклист аудита структуры и связей
- [ ] Автоматизировать проверку связей и актуальности project_manifest.json, rules_manifest.json

## 6. Документирование и best practices
- [ ] Фиксировать все изменения и лучшие практики в .cursor/rules/ и docs
- [ ] Обновлять onboarding и best practices при каждом крупном изменении

---

## Приоритеты:
1. Enforcement и автоматизация (pre-commit, CI/CD, MCP)
2. Чистка дублей и устаревших элементов
3. Связи и knowledge синхронизация
4. Покрытие workflow-этапов и автоматизация
5. Регулярный аудит и поддержка прозрачности
6. Документирование и поддержка onboarding 