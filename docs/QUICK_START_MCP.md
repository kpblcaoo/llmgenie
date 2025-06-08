# 🚀 Quick Start: MCP для чайников

**TL;DR:** Теперь Claude может автоматически создавать файлы и проверять качество работы вместо копипасты.

---

## Что уже работает (Epic 4 ✅):

### 1. Автоматическое создание handoff packages
```bash
# Вместо: "Claude, напиши текст, я скопирую в файлы"
# Теперь: "Claude, создай handoff package через MCP"

Результат: 5 файлов автоматически + валидация quality score
```

### 2. MCP Server запущен
```bash
# Проверить что работает:
curl http://localhost:8000/health
# Ответ: {"status": "healthy"}

# Проверить MCP endpoint:  
curl http://localhost:8000/mcp/messages/
# Ответ: SSE stream подключения
```

### 3. Cursor интеграция готова
```json
// .cursor/mcp.json уже настроен
{
  "mcpServers": {
    "llmgenie-handoff-validator": {
      "transport": {"type": "sse", "url": "http://localhost:8000/mcp/messages/"}
    }
  }
}
```

---

## Как использовать прямо сейчас:

### Шаг 1: Запустить сервер
```bash
cd /home/kpblc/projects/llm/llmgenie
uvicorn src.llmgenie.api.main:app --reload --port 8000
```

### Шаг 2: В Cursor сказать
```
"Создай handoff package для Epic 4 используя MCP tools"
```

### Шаг 3: Получить результат
```
✅ 5 файлов созданы автоматически
✅ Quality score: 0.84/1.0  
✅ Validation: PASS
```

---

## Что планируется (Epic 5 📋):

### MCP + Ollama = Экономия денег
```
Ты: "Объясни код и создай тесты"

Claude: 
- Объяснение → делаю сам (сложная задача)  
- Тесты → отправляю на Ollama (рутинная задача)
- Проверяю качество от Ollama
- Показываю тебе готовый результат

Результат: тратишь меньше на API, получаешь быстрее
```

### Задачи для Ollama:
- ✅ Генерация unit-тестов
- ✅ Объяснение кода  
- ✅ Рефакторинг
- ✅ Changelog
- ✅ Аудит кода

### Задачи для Claude:
- Архитектурные решения
- Сложный debugging
- Code review
- Планирование

---

## Документация

### Для разработчиков:
- **Подробно**: `docs/mcp_integration_guide.md`
- **API**: `src/llmgenie/api/main.py` + Swagger UI
- **Тесты**: `tests/api/test_handoff_validator.py`

### Для пользователей:
- **Handoff примеры**: `docs/memos/epic4/`
- **Troubleshooting**: `docs/mcp_integration_guide.md#troubleshooting`

---

## Если что-то не работает:

### Проблема: MCP не подключается в Cursor
```bash
# Проверить сервер:
curl http://localhost:8000/health

# Проверить конфиг:
cat .cursor/mcp.json

# Рестарт Cursor + сервера
```

### Проблема: Ollama недоступна (для Epic 5)
```bash
# Проверить Ollama:
curl http://localhost:11434/api/version

# Запустить если нужно:
ollama serve
```

### Проблема: "Не понимаю что происходит"
```bash
# Читать логи:
tail -f logs/epic4_session.log

# Проверить статус:
curl http://localhost:8000/validate-handoff -d '{"package_path": "docs/memos/epic4"}'
```

---

**💡 Главное**: Вместо копипасты теперь всё автоматически через MCP! 