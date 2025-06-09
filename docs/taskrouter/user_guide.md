# TaskRouter: Руководство пользователя

## 🎯 Введение

Это практическое руководство поможет вам эффективно использовать TaskRouter для маршрутизации задач между различными языковыми моделями.

## 🚀 Быстрый старт

### Запуск системы

```bash
# 1. Активация окружения
source .venv/bin/activate

# 2. Запуск FastAPI сервера
uvicorn src.llmgenie.api.main:app --host 0.0.0.0 --port 8000 --reload

# 3. Проверка готовности
curl http://localhost:8000/health
```

### Первый запрос

```bash
curl -X POST "http://localhost:8000/agents/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_type": "auto",
    "task": "Создай функцию для сортировки списка",
    "context": {"file_types": [".py"]}
  }'
```

## 🎯 Выбор типа агента

### `auto` - Автоматический (рекомендуется)

**Когда использовать**: В большинстве случаев
**Что делает**: Автоматически анализирует задачу и выбирает оптимальную модель

```json
{
  "agent_type": "auto",
  "task": "Любая задача",
  "context": {}
}
```

**Примеры автоматического выбора**:
- "Напиши функцию" → `codellama:7b` (быстро)
- "Спроектируй архитектуру" → `claude-3-5-sonnet` (качественно)
- "Создай документацию" → `mistral:7b-instruct` (сбалансированно)

### `ollama` - Принудительно Ollama

**Когда использовать**: 
- Быстрая обработка важнее качества
- Экспериментирование с локальными моделями
- Ограниченный интернет/бюджет

```json
{
  "agent_type": "ollama", 
  "task": "Задача для быстрой обработки",
  "context": {}
}
```

### `claude` - Принудительно Claude

**Когда использовать**:
- Критически важные решения
- Сложный анализ и планирование  
- Максимальное качество результата

```json
{
  "agent_type": "claude",
  "task": "Критически важная задача", 
  "context": {}
}
```

### `smart` - Алиас для `auto`

Синоним для `auto`, введен для совместимости.

## 📝 Оптимизация запросов

### Контекст помогает маршрутизации

```json
{
  "agent_type": "auto",
  "task": "Оптимизируй код",
  "context": {
    "file_types": [".py", ".js"],     // Подсказка о типе задачи
    "file_count": 15,                 // Масштаб проекта  
    "dependencies": ["fastapi", "react"], // Технологии
    "project_type": "web_api"         // Тип проекта
  }
}
```

### Формулировка задач

#### ✅ Хорошие формулировки

```
❇️ Конкретные задачи:
"Создай REST API endpoint для регистрации пользователей с валидацией email"

❇️ Указание технологий:
"Реализуй аутентификацию JWT в FastAPI с middleware"

❇️ Указание сложности:
"Спроектируй архитектуру микросервисов для e-commerce платформы"
```

#### ❌ Плохие формулировки

```
❌ Слишком общие:
"Помоги с кодом"

❌ Без контекста:
"Сделай лучше"

❌ Многозначные:
"Исправь всё"
```

## 📊 Интерпретация результатов

### Структура ответа

```json
{
  "agent_id": "auto_20250609_031416",
  "status": "success",
  "result": {
    "message": "Результат выполнения",
    "model": "codellama:7b",                    // Выбранная модель
    "execution_time": 11.018291,               // Время выполнения (сек)
    "routing_reasoning": "Task: code_generation | Complexity: simple | Selected: codellama:7b | Reasoning...",
    "confidence_score": 0.8,                   // Уверенность в классификации
    "context": {"file_types": [".py"]}
  },
  "error": null
}
```

### Анализ reasoning

**Формат**: `"Task: {type} | Complexity: {level} | Selected: {model} | {explanation}"`

**Примеры**:
```
"Task: code_generation | Complexity: simple | Selected: codellama:7b | Ollama preferred: routine task matching established patterns"

"Task: architecture_planning | Complexity: critical | Selected: claude-3-5-sonnet | Claude preferred: complex reasoning or critical decision required"
```

### Метрики производительности

- **execution_time < 15s**: Отличная производительность
- **15s < execution_time < 30s**: Нормальная производительность  
- **execution_time > 30s**: Медленно (возможно, стоит проверить Ollama)

- **confidence_score > 0.8**: Высокая уверенность в выборе
- **confidence_score 0.5-0.8**: Средняя уверенность
- **confidence_score < 0.5**: Низкая уверенность (неопределенная задача)

## 🔧 Типичные сценарии

### Разработка кода

```bash
# Генерация функций
curl -X POST "http://localhost:8000/agents/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_type": "auto",
    "task": "Создай функцию для валидации email адреса с регулярными выражениями",
    "context": {"file_types": [".py"], "project_type": "web_api"}
  }'
# → Выберет codellama:7b

# Рефакторинг
curl -X POST "http://localhost:8000/agents/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_type": "auto", 
    "task": "Оптимизируй этот SQL запрос для большой базы данных",
    "context": {"file_types": [".sql"], "file_count": 50}
  }'
# → Может выбрать claude для оптимизации
```

### Архитектурное планирование

```bash
curl -X POST "http://localhost:8000/agents/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_type": "auto",
    "task": "Спроектируй архитектуру микросервисов для платформы онлайн-обучения с масштабированием до 100k пользователей",
    "context": {"project_type": "microservices", "scale": "large"}
  }'
# → Выберет claude-3-5-sonnet
```

### Документация

```bash
curl -X POST "http://localhost:8000/agents/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_type": "auto",
    "task": "Создай README для Python проекта с установкой, использованием и примерами",
    "context": {"file_types": [".md"], "project_type": "python_library"}
  }'
# → Выберет mistral:7b-instruct
```

### Отладка

```bash
curl -X POST "http://localhost:8000/agents/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_type": "auto",
    "task": "Найди ошибку в этом коде: [код с ошибкой]",
    "context": {"file_types": [".py"], "error_type": "runtime"}
  }'
# → Обычно выберет ollama для быстрого анализа
```

## 🐛 Troubleshooting

### Медленная работа

**Проблема**: Запросы выполняются дольше 30 секунд

**Решения**:
1. Проверьте статус Ollama: `curl http://localhost:11434/api/tags`
2. Убедитесь что модели загружены: `ollama list`
3. Перезапустите Ollama: `ollama serve`

### Неподходящий выбор модели

**Проблема**: TaskRouter выбирает не ту модель

**Решения**:
1. Улучшите контекст в запросе
2. Уточните формулировку задачи
3. Используйте принудительный выбор (`ollama`/`claude`)

**Пример улучшения**:
```json
// Плохо
{
  "task": "помоги с API",
  "context": {}
}

// Хорошо  
{
  "task": "Создай REST API endpoint для аутентификации пользователей с JWT токенами",
  "context": {
    "file_types": [".py"],
    "project_type": "web_api", 
    "complexity": "moderate"
  }
}
```

### Ошибки подключения

**Проблема**: Ошибки соединения с моделями

**Ollama ошибки**:
```bash
# Проверка статуса
curl http://localhost:11434/api/tags

# Перезапуск
ollama serve

# Загрузка моделей
ollama pull mistral:7b-instruct
ollama pull codellama:7b
```

**Claude ошибки**:
- Проверьте API ключ в переменных окружения
- Убедитесь в наличии кредитов на аккаунте
- Временно используйте `"agent_type": "ollama"`

## 📈 Мониторинг эффективности

### Анализ логов

```bash
# Просмотр логов FastAPI
tail -f logs/fastapi.log

# Анализ времени выполнения
grep "execution_time" logs/fastapi.log | sort -n
```

### Оптимизация использования

1. **Отслеживайте паттерны**: Какие задачи чаще направляются к каждой модели
2. **Измеряйте качество**: Сравнивайте результаты разных моделей  
3. **Настраивайте контекст**: Добавляйте релевантную информацию

## 🔄 Интеграция с workflow

TaskRouter автоматически учитывает контекст llmgenie workflow:

```python
# В режиме [code] - автоматический фокус на code_generation
# В режиме [docs] - приоритет documentation задач  
# В режиме [discuss] - более частое использование claude
```

## 📞 Получение помощи

1. **Документация**: Полная документация в `docs/taskrouter/`
2. **Тесты**: Примеры использования в `tests/test_task_router.py`
3. **Логи**: Анализ поведения через session logs
4. **Issues**: Создание задач для улучшений

---

**Совет**: Начните с `"agent_type": "auto"` и экспериментируйте с контекстом для оптимальных результатов! 