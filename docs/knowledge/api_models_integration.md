# Integration: API коммерческих моделей

## Логика и поддерживаемые протоколы
- Логика реализуется через API (OpenAI, Anthropic, Google, Cohere и др.).
- MCP, OpenCtx, LSP, ToolSpec, cursor/rules не поддерживаются (см. integration_matrix).

## Внедрённые возможности
- API (OpenAI, Anthropic, Google, Cohere и др.)

## Ограничения и несовместимости
- Нет поддержки cursor/rules, MCP, OpenCtx, LSP, ToolSpec.

## История изменений
- 2024-06-12: Инициализация файла, фиксация текущих возможностей и ограничений (ai_assistant)
- 2025-06-12: Ревизия: подтверждено отсутствие поддержки MCP, OpenCtx, LSP, ToolSpec, добавлена ссылка на integration_matrix (ai_assistant)

## TODO
- Документировать все внедрённые возможности
- Оценить возможность интеграции LSP/OpenCtx 