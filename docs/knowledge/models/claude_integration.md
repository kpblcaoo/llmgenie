# Integration: Claude (Anthropic API)

## Логика и поддерживаемые протоколы
- Логика реализуется через Anthropic API (REST API, streaming).
- Поддержка tool use, vision, multimodal.
- MCP поддерживается через Claude Desktop App и claude.ai.
- LSP, ToolSpec, cursor/rules не поддерживаются напрямую (см. integration_matrix).

## Внедрённые возможности
- Anthropic API (REST, streaming)
- Tool use / function calling
- Vision (Claude 3.5 Sonnet, Claude 3 Opus)
- Multimodal (text, images)
- MCP (Claude Desktop App, claude.ai)
- Computer use (experimental)

## Ограничения и несовместимости
- Нет поддержки cursor/rules, LSP, ToolSpec напрямую.
- Rate limits и cost per token.
- Context window ограничения (зависит от модели).
- Нет локального запуска.

## Модели и версии
- Claude 3 Haiku: быстрая, легкая модель
- Claude 3 Sonnet: сбалансированная модель
- Claude 3 Opus: самая мощная модель
- Claude 3.5 Sonnet: улучшенная версия Sonnet
- Claude 3.7 Sonnet: latest с reasoning

## История изменений
- 2025-06-12: Инициализация файла, фиксация текущих возможностей и ограничений (ai_assistant)

## TODO
- Документировать все модели и их возможности
- Оценить интеграцию с MCP серверами
- Добавить примеры использования Computer Use

## Источники
- https://docs.anthropic.com/en/api/
- https://claude.ai/
- https://modelcontextprotocol.io/ 