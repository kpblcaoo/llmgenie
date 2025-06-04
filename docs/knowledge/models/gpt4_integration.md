# Integration: GPT-4 (OpenAI API)

## Логика и поддерживаемые протоколы
- Логика реализуется через OpenAI API (REST API, streaming).
- Поддержка function calling, tool use, vision, multimodal.
- MCP, LSP, ToolSpec, cursor/rules не поддерживаются напрямую (см. integration_matrix).
- Интеграция возможна через клиенты (VSCode, Claude Desktop, кастомные приложения).

## Внедрённые возможности
- OpenAI API (REST, streaming)
- Function calling / tool use
- Vision (GPT-4V, GPT-4o)
- Multimodal (text, images)
- JSON mode, structured outputs

## Ограничения и несовместимости
- Нет поддержки cursor/rules, MCP, LSP, ToolSpec напрямую.
- Rate limits и cost per token.
- Context window ограничения (зависит от модели).
- Нет локального запуска.

## Модели и версии
- GPT-4 (legacy): 8K/32K context
- GPT-4 Turbo: 128K context
- GPT-4o: multimodal, быстрее и дешевле
- GPT-4o mini: облегченная версия

## История изменений
- 2025-06-12: Инициализация файла, фиксация текущих возможностей и ограничений (ai_assistant)

## TODO
- Документировать все модели и их возможности
- Оценить интеграцию с MCP клиентами
- Добавить примеры использования

## Источники
- https://platform.openai.com/docs/api-reference
- https://platform.openai.com/docs/models 