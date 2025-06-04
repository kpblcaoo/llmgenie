# Integration: Llama3 (Meta)

## Логика и поддерживаемые протоколы
- Логика реализуется через локальный запуск (Ollama, LM Studio, HuggingFace) или API.
- Поддержка tool use (через внешние обертки), multimodal в новых версиях.
- MCP, LSP, ToolSpec, cursor/rules не поддерживаются напрямую (см. integration_matrix).
- Интеграция через Ollama, LM Studio, Continue для VSCode.

## Внедрённые возможности
- Локальный запуск (Ollama, LM Studio, GPT4All)
- API через внешние сервисы
- Tool use (через обертки)
- Fine-tuning возможности
- Открытый код и веса

## Ограничения и несовместимости
- Нет поддержки cursor/rules, MCP, LSP, ToolSpec напрямую.
- Требует значительные вычислительные ресурсы для локального запуска.
- Tool use не встроенный, требует дополнительные решения.
- Ограниченная поддержка multimodal (зависит от версии).

## Модели и версии
- Llama 3.2: 1B, 3B (lightweight), 11B, 90B (vision)
- Llama 3.1: 8B, 70B, 405B
- Llama 3: 8B, 70B (legacy)
- Разные квантизации (Q4, Q5, Q8, FP16)

## История изменений
- 2025-06-12: Инициализация файла, фиксация текущих возможностей и ограничений (ai_assistant)

## TODO
- Документировать все модели и квантизации
- Оценить tool use решения
- Добавить примеры локального запуска

## Источники
- https://ollama.ai/
- https://huggingface.co/meta-llama
- https://github.com/meta-llama/llama3 