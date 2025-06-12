# 🧠 LLMGenie

Оркестрация, автоматизация и интеграция AI-ассистентов и workflow с smart routing между моделями.

## 🚀 Что это?

LLMGenie — это система для умной оркестрации AI-ассистентов с автоматическим выбором модели (Ollama для быстрых задач, Claude для сложных), интеграцией с Cursor IDE через MCP и полной автоматизацией workflow.

## 📁 Структура проекта

```
restructure/
├── core/                    # Исходный код
│   ├── llmgenie/           # Основной оркестратор
│   ├── rag_context/        # RAG и контекстные инструменты
│   └── struct_tools/       # Структурные инструменты
├── docs/                   # Документация
├── archive/                # Архивные файлы
├── unused/                 # Неиспользуемые файлы
├── requirements.txt        # Зависимости
├── pyproject.toml         # Конфигурация проекта
└── README.md              # Этот файл
```

## ✨ Основные возможности

### 🎯 Smart AI Routing
- **TaskRouter**: автоматическая классификация задач
- **Ollama integration**: локальные модели для экономии API
- **Claude integration**: продвинутые задачи
- **Quality validation**: автоматический fallback при низком качестве

### 🔗 Cursor IDE Integration
- **MCP server**: интеграция через Model Context Protocol
- **Handoff validation**: передача контекста между сессиями
- **Real-time tools**: 11 инструментов (5 RAG + 6 Struct)

### 📊 Workflow Automation
- **CLI interface**: управление через командную строку
- **FastAPI server**: REST API для интеграции
- **Session management**: управление сессиями и контекстом

## 🛠 Установка

### Предварительные требования
- Python 3.8+
- Ollama (для локальных моделей)
- API ключи для Claude (Anthropic)

### Установка зависимостей

```bash
# Установка основных зависимостей
pip install -r requirements.txt

# Или с использованием pyproject.toml
pip install -e .

# Установка dev зависимостей
pip install -e .[dev]
```

### Настройка Ollama

```bash
# Установка моделей для Ollama
ollama pull mistral:7b-instruct
ollama pull codellama:7b
```

## 🚀 Быстрый старт

### 1. CLI использование

```bash
# Запуск основной команды
python core/llmgenie/cli.py --help

# Выполнение задачи с автоматическим routing
python core/llmgenie/cli.py execute "Создай функцию для сложения чисел"
```

### 2. API сервер

```bash
# Запуск FastAPI сервера
uvicorn core.llmgenie.api.main:app --host 0.0.0.0 --port 8000

# MCP endpoint доступен на http://localhost:8000/mcp
```

### 3. Cursor IDE интеграция

Добавьте в `.cursor/mcp.json`:

```json
{
  "servers": {
    "llmgenie-handoff-validator": {
      "command": "curl",
      "args": ["-N", "http://localhost:8000/mcp"],
      "env": {}
    }
  }
}
```

## 📖 Документация

### Основные руководства
- [Быстрый старт с MCP](docs/QUICK_START_MCP.md)
- [Руководство по TaskRouter](docs/taskrouter/user_guide.md)
- [MCP интеграция](docs/mcp_integration_guide.md)
- [API документация](docs/guides/api_usage.md)

### Архитектура
- [Обзор системы](docs/PROJECT_VISION.md)
- [Архитектурные решения](docs/architecture/)
- [Многоагентная оркестрация](docs/orchestration/README.md)

## 🧪 Тестирование

```bash
# Запуск всех тестов
pytest

# Запуск с покрытием
pytest --cov=core --cov-report=html

# Линтинг
black core/
flake8 core/
mypy core/
```

## 🔧 Разработка

### Установка для разработки

```bash
# Клонирование репозитория
git clone <repository-url>
cd llmgenie

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# Установка в режиме разработки
pip install -e .[dev]

# Установка pre-commit hooks
pre-commit install
```

### Структура модулей

- **core/llmgenie/**: основной модуль оркестрации
  - `api/`: FastAPI endpoints
  - `task_router/`: система роутинга задач
  - `modules/`: CLI модули и команды
  - `orchestration/`: многоагентная оркестрация

- **core/rag_context/**: RAG и контекстные инструменты
  - `embedder.py`: эмбеддинги и поиск
  - `retriever.py`: извлечение контекста
  - `cursor_intelligence.py`: интеграция с Cursor

- **core/struct_tools/**: структурные инструменты
  - `structure_analyzer.py`: анализ кода
  - `mcp_interface.py`: MCP интеграция

## 📊 Производительность

### Метрики TaskRouter
- **Code generation latency**: 11.6s (Ollama codellama:7b)
- **Classification confidence**: 0.8+ для большинства задач
- **API cost savings**: 30-50% для рутинных задач

### MCP Tools
- **RAG tools**: 0.02s init, 36 docs, 70 chunks
- **Struct tools**: 54 modules, 272 functions, 58 classes

## 🤝 Вклад в проект

1. Fork репозиторий
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в branch (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📄 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.

## 🔗 Полезные ссылки

- [Документация](docs/)
- [Примеры использования](docs/examples/)
- [Troubleshooting](docs/guides/troubleshooting.md)
- [Roadmap](docs/ROADMAP_STRATEGIC_2025.md)

## 📞 Поддержка

Если у вас есть вопросы или проблемы:
1. Проверьте [документацию](docs/)
2. Поищите в [Issues](https://github.com/llmgenie/llmgenie/issues)
3. Создайте новый Issue с подробным описанием

---

**Made with ❤️ by LLMGenie Team** 