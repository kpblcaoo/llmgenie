# Integration: Copilot

## Логика и поддерживаемые протоколы
- Логика реализуется через плагины для VSCode, JetBrains, Neovim.
- MCP поддерживается только через VSCode agent mode.
- LSP, ToolSpec, OpenCtx, cursor/rules не поддерживаются (см. integration_matrix).

## Внедрённые возможности
- Интеграция с VSCode, JetBrains, Neovim
- MCP (через VSCode agent mode)

## Ограничения и несовместимости
- Нет поддержки cursor/rules, MCP вне VSCode agent mode, LSP, ToolSpec, OpenCtx.

## История изменений
- 2024-06-12: Инициализация файла, фиксация текущих возможностей и ограничений (ai_assistant)
- 2025-06-12: Ревизия: уточнён статус MCP, LSP, ToolSpec, OpenCtx, добавлена ссылка на integration_matrix (ai_assistant)

## TODO
- Документировать все внедрённые возможности
- Оценить возможность интеграции LSP/OpenCtx 