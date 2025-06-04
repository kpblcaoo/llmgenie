# Аналитическая записка №1: Анализ и план доработки .cursor/rules для Cursor IDE

---

| Файл/Правило                | Описание/Назначение                | Тип (enforceable/manual/best practice) | Глобальное/проектное | globs/alwaysApply/manual | Требует доработки? | Draft-структура/замечания |
|-----------------------------|-------------------------------------|----------------------------------------|---------------------|-------------------------|--------------------|---------------------------|
| branch_policy.mdc           | Политика ветвления, запрет прямых изменений в develop, только через ветки/PR | enforceable           | проектное              | alwaysApply        | да                 | name: branch_policy\nalwaysApply: true\ndescription: "Enforce branch policy for all work."\ncontent: "..." |
| session-management.mdc      | Сессионный контроль, логирование, шаблоны логов, elastic workflow           | enforceable/manual    | проектное              | alwaysApply/manual | да                 | name: session_management\nalwaysApply: true\ndescription: "Session control and logging."\ncontent: "..." |
| logging-and-retrospective.mdc| Логирование, ретроспектива, lessons learned                                 | best practice         | проектное              | manual             | да                 | Возможно декомпозиция: logging (enforceable), retrospective (manual) |
| ai-capabilities.mdc         | Возможности и ограничения AI, automation, контроль сессий                    | best practice/manual  | проектное              | manual             | да                 | name: ai_capabilities\ndescription: "AI capabilities and automation."\ncontent: "..." |
| project_scope.mdc           | Политика symlink, структура project data, требования к данным                | best practice         | проектное              | manual             | да                 | Возможно оставить как справочник, либо выделить enforceable части |
| cli-commands.mdc            | Справочник CLI-команд, workflow, примеры                                    | best practice         | проектное              | manual             | да                 | Оставить как справочник, не автоматизировать |
| workflow-modes.mdc          | Режимы работы, переключение, фильтрация, логирование                        | enforceable/manual    | проектное              | globs/manual       | да                 | name: workflow_modes\nglobs: ["*.md", "*.py"]\ndescription: "Workflow modes and context tags."\ncontent: "..." |
| ai_best_practices.mdc       | Best practices для AI, language policy, trade-off анализ                     | best practice         | глобальное             | manual             | да                 | Оставить как справочник, добавить инструкцию по global rules |

---

## Следующие шаги:
- Для каждого enforceable/manual правила — подготовить draft YAML/JSON-структуру.
- Для best practice/справочников — оформить как отдельные docs или global rules.
- Согласовать с пользователем draft-структуры и доработки.

_Записка для согласования и доработки. После ревью — переход к преобразованию и тестированию._ 