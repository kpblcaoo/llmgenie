# Integration: Cursor IDE

## Логика и поддерживаемые протоколы
- Основная логика реализуется через .cursor/rules (mdc), поддержка agent requested, auto attached, alwaysApply.
- CLI не обязателен, возможна работа только через rules.
- MCP, OpenCtx, LSP, ToolSpec не поддерживаются (см. integration_matrix).

## Внедрённые возможности
- agent rule (автоматическая активация правил по ключевым словам)
- alwaysApply, globs, manual, auto attached

## Ограничения и несовместимости
- cursor/rules не применимы к Ollama, VSCode, Copilot и др.
- Нет поддержки MCP, OpenCtx, LSP, ToolSpec.

## История изменений
- 2024-06-12: Инициализация файла, фиксация текущих возможностей и ограничений (ai_assistant)
- 2025-06-12: Ревизия: подтверждено отсутствие поддержки MCP, OpenCtx, LSP, ToolSpec, добавлена ссылка на integration_matrix (ai_assistant)

## TODO
- Оценить возможность интеграции OpenCtx/LSP
- Документировать все внедрённые возможности 