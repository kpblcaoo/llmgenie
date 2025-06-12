# Руководство по пополнению Knowledge Base

## Для кого
Этот документ предназначен для пользователей, которые хотят добавить новые среды, модели или обновить существующую информацию в knowledge base.

## Структура knowledge base

### Папки:
- `docs/knowledge/` — документация для людей (markdown)
- `data/knowledge/` — структурированные данные для LLM (json)
- `docs/knowledge/templates/` — шаблоны для новых integration файлов

### Типы интеграций:
- **Среды**: Cursor, VSCode, Ollama, etc. (`docs/knowledge/{env}_integration.md`)
- **Модели**: GPT-4, Claude, Llama3, etc. (`docs/knowledge/models/{model}_integration.md`)
- **Общие**: integration_matrix, common, workflow

## Добавление новой среды

### Шаг 1: Копирование шаблона
```bash
cp docs/knowledge/templates/env_integration_template.md docs/knowledge/{your_env}_integration.md
cp data/knowledge/templates/env_integration_template.json data/knowledge/envs/{your_env}_integration.json
```

### Шаг 2: Заполнение шаблона
1. Заменить все `{PLACEHOLDER}` на актуальные значения
2. Указать поддерживаемые протоколы в integration объекте
3. Добавить все возможности, ограничения, несовместимости
4. Указать официальные источники

### Шаг 3: Обновление integration_matrix
Добавить новую среду в таблицу в `docs/knowledge/integration_matrix.md`

### Шаг 4: Логирование
Добавить запись в `data/sessions/event_log_meta_rules_activation.json`:
```json
{
  "timestamp": "YYYY-MM-DDTHH:MM:SS+03:00",
  "event": "new_env_added",
  "author": "user_name",
  "details": "Добавлена новая среда {ENV_NAME} в knowledge base"
}
```

## Добавление новой модели

### Аналогично средам, но:
- Использовать `model_integration_template.md/json`
- Сохранять в `docs/knowledge/models/` и `data/knowledge/models/`
- Указать технические характеристики (context window, pricing, performance)

## Обновление существующих integration файлов

### При обнаружении изменений:
1. Обновить MD и JSON файлы синхронно
2. Добавить запись в `history` раздел JSON файла
3. Обновить `last_reviewed` метку
4. Зафиксировать в event_log

### Что обновлять:
- Новые возможности в `implemented_features`
- Изменения в протоколах в `integration` объекте
- Новые ограничения в `limitations`
- Источники в `sources`

## Протоколы и стандарты

### Поддерживаемые протоколы:
- **rules**: .cursor/rules (только для Cursor)
- **cli**: Command Line Interface
- **api**: REST API
- **mcp**: Model Context Protocol (VSCode, Claude Desktop)
- **lsp**: Language Server Protocol (VSCode, IDE)
- **toolspec**: Tool specification (VSCode плагины)

### Статусы поддержки:
- `true` — полная поддержка
- `false` — не поддерживается
- Добавлять пояснения в `logic_notes`

## Quality checklist

Перед отправкой изменений проверить:
- ✅ MD и JSON файлы синхронизированы
- ✅ Все {PLACEHOLDER} заменены
- ✅ Удалены _notes и _template_instructions из JSON
- ✅ Добавлены ссылки на источники
- ✅ Обновлен integration_matrix при необходимости
- ✅ Добавлена запись в event_log
- ✅ History записи актуальны

## Помощь и поддержка

### При вопросах:
1. Консультироваться с `docs/knowledge/workflow_knowledge_engineer.md`
2. Проверять `docs/knowledge/integration_matrix.md` для существующих интеграций
3. Использовать knowledge-engineer роль AI для автоматизации

### Автоматизация:
AI с ролью knowledge-engineer может:
- Автоматически заполнять шаблоны
- Синхронизировать MD и JSON файлы
- Проверять официальные источники
- Обновлять integration_matrix
- Логировать изменения

## Примеры

См. существующие файлы:
- `docs/knowledge/cursor_integration.md` — пример среды
- `docs/knowledge/models/claude_integration.md` — пример модели
- `data/knowledge/envs/vscode_integration.json` — пример JSON структуры 