# Knowledge Base (User)

В этой папке содержатся гайды, best practices и обзоры по основным средам (Cursor, VSCode, Copilot, Ollama, API моделей) и моделям (gpt-4, llama3, mixtral и др.).

- Каждый файл — отдельная среда или модель.
- Структура knowledge base синхронизирована с data/knowledge (json для AI).
- Для пополнения базы знаний используйте роль knowledge-engineer и соответствующий workflow.

# LLMGenie Knowledge Base

База знаний проекта llmgenie с документацией интеграций, моделей и протоколов.

## Структура

### Основные разделы
- `common.md` - общая информация об интеграциях
- `integration_matrix.md` - матрица совместимости
- `workflow_knowledge_engineer.md` - процессы работы с базой знаний

### Технологии и протоколы
- `techs/mcp_model_context_protocol.md` - **NEW** руководство по Model Context Protocol
- `cursor.md` - интеграция с Cursor IDE  
- `ollama.md` - локальные модели через Ollama
- `vscode.md` - интеграция с VS Code

### Модели
- `models/` - детальная информация о поддерживаемых моделях
- `gpt-4.md`, `claude.md`, `llama3.md` и др.

## Недавние обновления

### 2025-01-05: MCP Integration Knowledge
- ✅ Добавлена полная документация по Model Context Protocol
- ✅ Руководство по интеграции MCP + Ollama для task offloading
- ✅ Практические примеры и best practices
- ✅ Troubleshooting и конфигурация

Подробности в `techs/mcp_model_context_protocol.md` 