# Универсальные интерфейсы для RAG системы

**Цель:** Создать универсальную архитектуру доступа к RAG системе через различные интерфейсы

## 🏗️ Архитектура

```
         🧠 Core RAG Engine
         ├── PromptEnhancer
         ├── ContextRetriever  
         ├── SimpleEmbedder
         └── Loaders
                   ↑
         ┌─────────┴─────────┐
         │   Transport Layer  │
         └─────────┬─────────┘
                   ↓
    ┌─────────────┼─────────────┐
    │             │             │
📡 MCP Server  📜 HTTP API  💻 CLI Tool
    │             │             │
    ↓             ↓             ↓
🔧 Cursor      🌐 Web Apps  📜 Scripts
🔧 VSCode      🔗 Services  🖥️ Terminal  
🔧 Claude      📱 Mobile    🤖 Automation
```

## 📦 Интерфейсы

### 1. **MCP Server** (для IDE интеграций)
- **Cursor**: Прямая интеграция через stdio
- **VSCode**: Расширения с MCP поддержкой  
- **Claude Desktop**: Подключение как MCP сервер

**Инструменты:**
- `enhance_prompt` - улучшение промптов
- `get_relevant_rules` - поиск правил
- `get_project_structure` - структура проекта
- `get_system_stats` - статистика
- `refresh_index` - обновление индекса

### 2. **HTTP API** (для веб-интеграций)
- **REST API** с Swagger документацией
- **CORS** поддержка для веб-приложений
- **JSON** форматы запросов/ответов

**Endpoints:**
- `POST /enhance` - улучшение промптов
- `POST /rules/search` - поиск правил
- `GET /project/structure` - структура проекта
- `GET /stats` - статистика системы
- `POST /admin/refresh` - обновление индекса

### 3. **CLI Tool** (для командной строки)
- Поддержка **JSON** и **текстового** вывода
- Интеграция в **скрипты** и **автоматизацию**
- **Unix-friendly** команды

**Команды:**
```bash
python -m rag_context.interfaces.cli_tool enhance "Create new API endpoint"
python -m rag_context.interfaces.cli_tool search "authentication rules" --max-rules 5
python -m rag_context.interfaces.cli_tool stats --json
python -m rag_context.interfaces.cli_tool refresh
python -m rag_context.interfaces.cli_tool struct
```

### 4. **WebSocket Server** (для real-time)
- **Двунаправленная** связь
- **Broadcast** уведомления
- **JSON** протокол сообщений

**Actions:**
- `enhance_prompt` - улучшение промптов
- `search_rules` - поиск правил
- `get_project_structure` - структура проекта
- `get_stats` - статистика
- `refresh_index` - обновление индекса
- `ping` - проверка соединения

## 🚀 Развертывание

### Зависимости

**Базовые (уже установлены):**
```bash
sentence-transformers faiss-cpu langchain-community beautifulsoup4
```

**Дополнительные интерфейсы:**
```bash
# MCP Server
pip install mcp

# HTTP API  
pip install fastapi uvicorn

# WebSocket Server
pip install websockets
```

### Для Cursor/VSCode (MCP)
```bash
# 1. Установка зависимостей
pip install mcp

# 2. Создание конфигурации
python -m rag_context.interfaces.mcp_server --save-config

# 3. Запуск в stdio режиме
python -m rag_context.interfaces.mcp_server
```

### Для HTTP API
```bash
# 1. Установка зависимостей
pip install fastapi uvicorn

# 2. Запуск сервера
python -m rag_context.interfaces.http_api --host 0.0.0.0 --port 8001

# 3. Доступ к Swagger UI
# http://localhost:8001/docs
```

### Для CLI
```bash
# Прямое использование
python -m rag_context.interfaces.cli_tool enhance "Create API endpoint"
python -m rag_context.interfaces.cli_tool search "rules" --json
```

### Для WebSocket
```bash
# 1. Установка зависимостей
pip install websockets

# 2. Запуск сервера
python -m rag_context.interfaces.websocket_server --host localhost --port 8002

# 3. Пример клиентского кода
python -m rag_context.interfaces.websocket_server --example
```

## 🔧 Конфигурация

### Cursor MCP Config (`.cursor/mcp.json`)
```json
{
  "mcpServers": {
    "llmgenie-rag": {
      "command": "python",
      "args": ["-m", "rag_context.interfaces.mcp_server"],
      "env": {
        "PYTHONPATH": "."
      }
    }
  }
}
```

### VSCode Extension Settings
```json
{
  "mcp.servers": {
    "llmgenie-rag": {
      "command": "python", 
      "args": ["-m", "rag_context.interfaces.mcp_server"]
    }
  }
}
```

## 🎯 Использование

### **MCP Integration**
```python
# В Cursor/VSCode/Claude Desktop
# Вызов через MCP tools:
enhance_prompt(query="Create API endpoint", max_context=2000)
get_relevant_rules(query="authentication", max_rules=3)
```

### **HTTP API Integration**
```python
import httpx

async with httpx.AsyncClient() as client:
    # Enhance prompt
    response = await client.post("http://localhost:8001/enhance", json={
        "query": "Create API endpoint",
        "max_context": 2000
    })
    
    # Search rules
    response = await client.get("http://localhost:8001/rules/search", params={
        "query": "authentication",
        "max_rules": 3
    })
```

### **CLI Integration**
```bash
#!/bin/bash
# Автоматизация через CLI
ENHANCED=$(python -m rag_context.interfaces.cli_tool enhance "Create API" --json)
echo "Enhanced prompt: $ENHANCED"

RULES=$(python -m rag_context.interfaces.cli_tool search "auth" --json)
echo "Relevant rules: $RULES"
```

### **WebSocket Integration** 
```javascript
const ws = new WebSocket('ws://localhost:8002');

ws.onopen = () => {
    // Enhance prompt
    ws.send(JSON.stringify({
        "id": "req-1",
        "action": "enhance_prompt", 
        "params": {"query": "Create API endpoint"}
    }));
};

ws.onmessage = (event) => {
    const response = JSON.parse(event.data);
    console.log('Enhanced:', response.result.enhanced_query);
};
```

## 🎯 Преимущества универсальной архитектуры

### ✅ **Единый источник истины**
- Все интерфейсы используют один Core RAG Engine
- Консистентность результатов
- Централизованная конфигурация

### ✅ **Масштабируемость**
- Легко добавлять новые интерфейсы
- Модульная архитектура
- Независимое развитие компонентов

### ✅ **Совместимость**
- Работает с любыми IDE поддерживающими MCP
- Веб-интеграции через REST API
- Командная строка для автоматизации
- Real-time через WebSocket

### ✅ **Производительность**
- Общий кэш embeddings
- Переиспользование индексов
- Оптимизированная загрузка

## 📊 Поддерживаемые сценарии

### 🔧 **IDE Интеграция**
- Контекстно-зависимые подсказки в коде
- Автоматическое улучшение промптов
- Поиск релевантных правил проекта

### 🌐 **Веб-приложения**
- Чат-боты с контекстом проекта
- Документация с smart-поиском
- API для внешних сервисов

### 💻 **Автоматизация**
- CI/CD пайплайны с контекстом
- Скрипты генерации кода
- Batch-обработка документов

### 📱 **Real-time приложения**
- Live чаты с контекстом
- Уведомления об изменениях
- Collaborative editing

## 🛡️ Безопасность

- **Validation** всех входящих запросов
- **CORS** настройки для веб-интеграций
- **Rate limiting** (при необходимости)
- **Логирование** всех операций

## 📈 Мониторинг

- **Health checks** для всех интерфейсов
- **Статистика** использования по интерфейсам
- **Performance metrics** для каждого транспорта
- **Error tracking** с детализацией

---

## ✅ **Итог: Простая и мощная архитектура!**

Универсальная архитектура решает проблему:
1. **Cursor/VSCode** ✅ нативная интеграция через MCP
2. **Веб-приложения** ✅ REST API интеграция  
3. **Командная строка** ✅ автоматизация и скрипты
4. **Real-time приложения** ✅ WebSocket интеграция
5. **Будущие платформы** ✅ легко добавлять новые интерфейсы

Все интерфейсы используют **единое ядро**, обеспечивая консистентность и простоту поддержки.

**Размер venv (~6 ГБ)** - нормально для AI/ML проектов с PyTorch + CUDA.

**MCP интеграция** - готова для Cursor с официальным Python SDK. 