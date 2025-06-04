# Integration: VSCode

## Логика и поддерживаемые протоколы
- Логика реализуется через плагины (Copilot, Continue, Ollama и др.), LSP, MCP (agent mode).
- Поддержка LSP, ToolSpec (через плагины), MCP (только в agent mode).
- OpenCtx — экспериментально через Sourcegraph Cody, массово не поддерживается (см. integration_matrix).
- cursor/rules не поддерживаются.

## Внедрённые возможности
- LSP (через плагины)
- ToolSpec (через плагины)
- MCP (agent mode)
- Интеграция с Copilot, Continue, Ollama

## Ограничения и несовместимости
- Нет поддержки cursor/rules, MCP вне agent mode, OpenCtx — только экспериментально.

## История изменений
- 2024-06-12: Инициализация файла, фиксация текущих возможностей и ограничений (ai_assistant)
- 2025-06-12: Ревизия: уточнены статусы MCP, LSP, ToolSpec, OpenCtx, добавлена ссылка на integration_matrix (ai_assistant)

## TODO
- Документировать все внедрённые возможности
- Оценить возможность интеграции OpenCtx 