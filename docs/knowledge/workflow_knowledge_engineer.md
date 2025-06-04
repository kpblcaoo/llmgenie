# Workflow: Knowledge Engineer

## Активация роли
Роль knowledge-engineer активируется автоматически при работе с:
- knowledge base (docs/knowledge/ и data/knowledge/)
- integration matrix
- поиске информации о протоколах/стандартах
- обновлении integration файлов

## Основные workflow

### 1. Ревизия knowledge base
**Когда:** раз в квартал или при обнаружении устаревшей информации

**Шаги:**
1. Проверить last_reviewed метки в integration файлах
2. Найти файлы старше 3 месяцев
3. Проверить официальные источники на обновления
4. Обновить MD и JSON файлы одновременно
5. Добавить записи в history
6. Зафиксировать изменения в event_log

### 2. Пополнение knowledge base
**Когда:** при поиске новой информации или обнаружении новых протоколов/сред/моделей

**Шаги:**
1. Создать integration.md и integration.json для новой сущности
2. Заполнить все обязательные поля (integration, logic_notes, limitations, history)
3. Добавить ссылки на источники
4. Обновить integration_matrix при необходимости
5. Зафиксировать в event_log

### 3. Синхронизация MD/JSON
**Когда:** после любых изменений в knowledge base

**Принципы:**
- MD файлы — для людей (readable format)
- JSON файлы — для LLM и автоматизации (structured data)
- Содержание должно быть синхронизировано
- Добавлять temporal markers (last_reviewed, history)

### 4. Мониторинг протоколов
**Когда:** при работе с интеграциями

**Шаги:**
1. Консультироваться с integration_matrix перед планированием
2. Проверять официальные источники MCP, LSP, ToolSpec, OpenCtx
3. Обновлять статусы поддержки при изменениях
4. Фиксировать breaking changes немедленно

## Качественные критерии

### Обязательные поля для новых integration файлов:
- **integration**: объект с поддерживаемыми протоколами
- **logic_notes**: описание логики интеграции
- **limitations**: явные ограничения
- **incompatibilities**: несовместимости
- **history**: записи об изменениях
- **sources**: ссылки на официальные источники

### Naming conventions:
- **Среды**: `{env}_integration.md/json` (cursor, vscode, ollama)
- **Модели**: `{model}_integration.md/json` (gpt4, claude, llama3)
- **Общие файлы**: `common.md`, `integration_matrix.md`

### Quality gates:
- ✅ MD и JSON файлы синхронизированы
- ✅ Есть ссылки на integration_matrix
- ✅ History записи актуальны
- ✅ Sources указаны
- ✅ Event_log обновлен

## Эскалация

### Критические изменения (немедленно):
- Breaking changes в протоколах
- Новые возможности интеграции
- Конфликты совместимости

### Плановые задачи:
- Квартальная ревизия
- Расширение coverage на новые среды/модели
- Улучшение workflow и автоматизации

## Инструменты
- **Поиск**: web_search для официальных источников
- **Файлы**: синхронная работа с MD и JSON
- **Логирование**: event_log для всех изменений
- **Ревизия**: integration_matrix как single source of truth 