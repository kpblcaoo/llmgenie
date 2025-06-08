# llmgenie MCP Integration Guide

## Overview

llmgenie implements Model Context Protocol (MCP) to provide AI assistants with structured access to handoff validation tools. This enables seamless integration with AI-powered IDEs like Cursor for automated context transfer validation.

## Зачем это нужно? (Практическая ценность)

### Проблема: Context Loss при работе с AI
**Ситуация без handoff validation:**
```
Работаешь с Claude → Нужно переключиться на Ollama → Весь контекст потерян!
     ↓                           ↓                          ↓
Epic в процессе              Новая сессия           Начинаешь с нуля
```

**Что происходит:**
- 🔥 Теряется история решений и reasoning  
- 🔥 Дублируется уже проделанная работа
- 🔥 Повторяются уже исправленные ошибки
- 🔥 Нет понимания текущего статуса и следующих шагов

### Решение: Структурированная передача контекста
**С handoff validation:**
```
Claude работа → Handoff Package → Валидация → Ollama с контекстом
     ↓               ↓              ↓              ↓
Epic прогресс    5 файлов      Score 0.84    Продолжение работы
                 + промпт       ✅ PASS       без потерь
```

**Что получаешь:**
- ✅ **Нет потерь контекста** - новый AI знает что было сделано
- ✅ **Автоматическая проверка** готовности к передаче  
- ✅ **Стандартизированный процесс** - не думаешь что включить
- ✅ **Quality assurance** - AI проверяет completeness до передачи

### Реальные Use Cases

#### 1. Смена AI assistant'ов
```bash
# Работал с Claude в Cursor
"Создай handoff package для передачи работы на Ollama"

# AI автоматически:
# - Собирает 5 типов файлов (summary, lessons, checklist, audit, metadata)  
# - Создает startup prompt с ключевой информацией
# - Генерирует control questions для проверки понимания
# - Валидирует completeness (score 0.8+ = готов к передаче)

# Передаешь пакет в Ollama → контекст полностью сохранен!
```

#### 2. Переключение между проектами/эпиками
```bash
# Завершаешь Epic 4
"Validate Epic 4 handoff package for completion"

# AI проверяет:
# ✅ Все файлы присутствуют? 
# ✅ Lessons learned документированы?
# ✅ Следующие шаги понятны?
# Score 0.84/1.0 → ✅ PASS, можно передавать или архивировать
```

#### 3. Работа в команде
```bash
# Developer A передает работу Developer B
"Валидируй мой handoff package перед отпуском"

# AI: "❌ Missing lessons file, completeness 0.6/1.0 - добавь детали"
# После исправлений: "✅ PASS, handoff ready"
```

#### 4. Backup контекста для длительной работы
```bash
# Работаешь над сложной задачей месяц
"Создавай checkpoint handoff packages каждую неделю"

# Если что-то пойдет не так → всегда можешь вернуться к последнему validated checkpoint
```

## MCP + Ollama: Offloading задач на локальный AI

### Концепция: Cursor → MCP → Ollama для эффективного разделения труда

**Идея:** Использовать MCP для передачи рутинных задач с Cursor/Claude на локальную Ollama, освобождая дорогие API calls для сложных задач.

**Architektura:**
```
┌─────────────┐    MCP     ┌──────────────┐    API     ┌──────────────┐
│   Cursor    │ ─────────→ │ llmgenie MCP │ ─────────→ │    Ollama    │
│  (Claude)   │           │   Server     │           │  (локально)   │
└─────────────┘           └──────────────┘           └──────────────┘
  Сложные задачи          Routing & Quality          Рутинные задачи
  Reasoning              Control & Validation        Code gen, tests
```

### Практические сценарии из Epic 2

На основе lessons learned из Epic 2, где уже экспериментировали с Ollama:

#### ✅ Эффективно для Ollama:
```bash
# 1. Генерация unit-тестов
"Создай тесты для функции validate_handoff_package"
→ MCP → Ollama → качественные тесты

# 2. Объяснение кода  
"Объясни что делает этот endpoint"
→ MCP → Ollama → понятное объяснение

# 3. Рефакторинг по шаблонам
"Переименуй переменные в camelCase"
→ MCP → Ollama → автоматический рефакторинг

# 4. Генерация changelog
"Создай changelog по git commits"
→ MCP → Ollama → структурированный changelog

# 5. Аудит кода по правилам
"Проверь код на соответствие PEP8"
→ MCP → Ollama → список нарушений
```

#### ❌ Оставить для Claude/GPT:
- Архитектурные решения
- Сложный debugging  
- Code review с контекстом
- Планирование эпиков
- Интеграция компонентов

### Реализация MCP-Ollama интеграции

#### 1. Добавить Ollama endpoint в MCP сервер
```python
# В src/llmgenie/api/main.py
from llmgenie.integrations.ollama_client import OllamaClient

@app.post("/mcp/ollama/generate")
async def ollama_generate(task: str, model: str = "llama3.2"):
    """Offload task to local Ollama"""
    client = OllamaClient()
    return await client.generate(task, model)
```

#### 2. Routing logic по сложности
```python
# Автоматический routing
def should_use_ollama(task: str) -> bool:
    ollama_patterns = [
        "create test", "generate test", "explain code", 
        "refactor", "rename", "changelog", "audit"
    ]
    return any(pattern in task.lower() for pattern in ollama_patterns)
```

#### 3. Quality control для Ollama результатов
```python
# Validation pipeline
async def validate_ollama_result(task: str, result: str) -> bool:
    """Проверяем качество результата от Ollama"""
    if "create test" in task:
        return "def test_" in result and "assert" in result
    if "explain" in task:
        return len(result) > 50 and not "I don't know" in result
    return True
```

### Конфигурация в .cursor/mcp.json
```json
{
  "mcpServers": {
    "llmgenie-ollama": {
      "command": "uvicorn",
      "args": ["llmgenie.api.main:app", "--port", "8001"],
      "transport": {
        "type": "sse",
        "url": "http://localhost:8001/mcp/messages/"
      },
      "capabilities": {
        "tools": {
          "validate_handoff": "Validate handoff package quality",
          "generate_with_ollama": "Generate code/tests with local Ollama",
          "explain_code": "Explain code using Ollama",
          "refactor_code": "Refactor code using Ollama"
        }
      }
    }
  }
}
```

### Пример workflow в Cursor:
```
Пользователь: "Создай handoff package и объясни каждую функцию в коде"

Cursor (Claude):
1. "Создаю handoff package" → сложная задача, делаю сам
2. "Объясни функции" → простая задача → MCP → Ollama
3. Получаю объяснения от Ollama
4. Объединяю результаты и показываю пользователю

Результат: экономия API calls, быстрее выполнение рутинных задач
```

## What is MCP?

Model Context Protocol (MCP) is an open standard that enables AI applications to connect with external tools and data sources through a standardized interface. Think of it as "USB-C for AI applications" - it provides a universal way for AI assistants to discover and use tools.

## Простыми словами: что это даёт лично тебе?

### Без MCP (сейчас):
```
Ты: "Claude, создай handoff package"
Claude: "Вот текст, скопируй и сохрани в файлы вручную"
Ты: *тратишь 10 минут на копипасту и создание файлов*
```

### С MCP (после внедрения):
```
Ты: "Claude, создай handoff package"  
Claude: *автоматически создает 5 файлов через MCP, валидирует, показывает score*
Ты: "Готово! Score 0.84/1.0 ✅"
```

### С MCP + Ollama (планируемое):
```
Ты: "Объясни этот код и создай для него тесты"
Claude: "Объяснение делаю сам, тесты отправляю на Ollama"
*Ollama генерирует тесты локально, Claude проверяет качество*
Claude: "Вот объяснение + качественные тесты"

Результат: экономишь деньги на API, получаешь результат быстрее
```

## llmgenie MCP Server

Our MCP server provides these tools for AI assistants:

### Available Tools

1. **`validate_handoff_package`** - Validates handoff package completeness
   - Checks minimum 5 files requirement
   - Validates startup prompt content  
   - Analyzes control questions coverage
   - Returns completeness score and recommendations

2. **`get_handoff_template`** - Provides handoff package template
   - Returns template structure with required files
   - Includes validation criteria and requirements
   - Provides example content for each file type

## Setup Instructions

### For Cursor IDE Users

1. **Start the MCP Server**
   ```bash
   cd src
   python -m llmgenie.api.main
   ```
   The server will start on `http://localhost:8000` with MCP endpoint at `/mcp`

2. **Configure Cursor MCP**
   
   The project already includes `.cursor/mcp.json`:
   ```json
   {
     "mcpServers": {
       "llmgenie-handoff-validator": {
         "description": "llmgenie handoff validation and workflow management tools",
         "transport": {
           "type": "sse",
           "url": "http://localhost:8000/mcp"
         },
         "env": {}
       }
     }
   }
   ```

3. **Verify Integration**
   - Restart Cursor if it was running
   - Open Cursor Chat/Agent
   - Ask: "What handoff validation tools are available?"
   - The AI should discover and list the MCP tools

### Usage Examples

#### Validate Current Epic
```
"Please validate the Epic 4 handoff package using available tools"
```

#### Get Handoff Template  
```
"Show me the handoff package template and requirements"
```

#### Create New Handoff Package
```
"Help me create a handoff package for Epic 5 using the template"
```

## Technical Details

### Architecture
- **FastAPI Server**: Provides REST API and MCP integration
- **fastapi-mcp**: Library handling MCP protocol implementation  
- **SSE Transport**: Server-Sent Events for real-time communication
- **HandoffValidator**: Core validation logic with Pydantic models

### Endpoints
- `/mcp` - MCP protocol endpoint (SSE)
- `/handoff/validate` - Direct REST API validation
- `/handoff/template` - Template retrieval
- `/docs` - OpenAPI documentation

### CI/CD Integration
The MCP server is automatically tested in CI/CD:
- Basic validation functionality tests
- Epic 4 handoff package validation
- Completeness scoring and reporting

## Troubleshooting

### Common Issues

1. **"MCP server not found"**
   - Ensure the FastAPI server is running on port 8000
   - Check that `.cursor/mcp.json` exists in project root
   - Restart Cursor IDE

2. **"Tools not available"**
   - Verify MCP endpoint responds: `curl http://localhost:8000/mcp`
   - Check server logs for errors
   - Ensure operation_id is set on FastAPI endpoints

3. **"Validation always fails"**
   - Check file paths are relative to project root
   - Ensure all required file types are included
   - Verify startup prompt includes key elements

### Debug Commands

```bash
# Test MCP endpoint
curl -H "Accept: text/event-stream" http://localhost:8000/mcp

# Test validation directly
curl -X POST http://localhost:8000/handoff/validate \
  -H "Content-Type: application/json" \
  -d '{"from_role":"test","to_role":"test","epic_id":"test","files":[],"startup_prompt":"test","control_questions":[],"success_criteria":[]}'

# Run local validation test
python test_handoff_validation.py
```

## Best Practices

### For Handoff Packages
1. **Include all 5 required file types**: summary, lessons, checklist, audit, metadata
2. **Write comprehensive startup prompts** with status, infrastructure, lessons, constraints, next steps  
3. **Create meaningful control questions** covering status, technical details, and scope
4. **Keep files current** and remove outdated information

### For AI Assistants
1. **Use MCP tools proactively** when working with handoffs
2. **Validate before major context transfers** to ensure completeness
3. **Follow recommendations** from validation reports
4. **Update handoff packages** when significant changes occur

## Future Enhancements

- [ ] Resource support (read-only access to project files)
- [ ] Integration with more AI platforms (Claude Desktop, etc.)
- [ ] Enhanced validation rules and scoring
- [ ] Automated handoff package generation
- [ ] Integration with project management tools

## Links

- [MCP Official Documentation](https://github.com/modelcontextprotocol)
- [Cursor MCP Guide](https://docs.cursor.com/context/model-context-protocol)
- [FastAPI MCP Library](https://pypi.org/project/fastapi-mcp/)
- [Epic 4 Requirements](./memos/epic4/epic4_requirements_and_lessons.md) 