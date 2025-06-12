# Handoff Validation System - User Guide

## Overview

Система автоматической валидации handoff пакетов для передачи контекста между ролями, сессиями и участниками проекта. Обеспечивает структурированный, воспроизводимый процесс передачи контекста с автоматической проверкой completeness.

## Quick Start

### 1. Создание handoff пакета

```bash
# Генерация шаблона
python src/llmgenie/cli/handoff_cli.py template my_handoff.json

# Редактирование конфигурации
nano my_handoff.json
```

### 2. Валидация пакета

```bash
# Полная валидация с детальным выводом
python src/llmgenie/cli/handoff_cli.py validate my_handoff.json --verbose

# CI/CD режим (минимальный вывод)
python src/llmgenie/cli/handoff_cli.py check my_handoff.json --fail-on-warnings
```

### 3. API использование

```bash
# Получение шаблона
curl -X GET "http://localhost:8000/handoff/template"

# Валидация через API
curl -X POST "http://localhost:8000/handoff/validate" \
  -H "Content-Type: application/json" \
  -d @my_handoff.json
```

## Структура Handoff Пакета

### Обязательные поля

```json
{
  "from_role": "coder",           // Источник передачи
  "to_role": "reviewer",          // Получатель
  "epic_id": "epic3-standards",   // Идентификатор эпика/задачи
  "files": [...],                 // Минимум 5 файлов
  "startup_prompt": "...",        // Prompt для восстановления контекста
  "control_questions": [...],     // Минимум 3 контрольных вопроса
  "success_criteria": [...],      // Критерии успешного продолжения
  "metadata": {...}               // Дополнительные метаданные
}
```

### Обязательные типы файлов

1. **summary** - Краткий обзор/статус
2. **lessons** - Детальные lessons learned
3. **checklist** - Оригинальный checklist с прогрессом
4. **audit** - Технический/аудит отчет
5. **metadata** - Состояние проекта/метаданные

## Validation Criteria

### Scoring System (100%)

- **Files (50%)** - Все файлы существуют и не пустые
- **Startup Prompt (30%)** - Включает статус, инфраструктуру, уроки, ограничения, следующие шаги
- **Control Questions (20%)** - Покрывают статус, технические аспекты, scope

### Minimum Requirements

- ✅ **5+ файлов** всех обязательных типов
- ✅ **80%+ completeness score**
- ✅ **3+ контрольных вопроса**
- ✅ **Startup prompt** с ключевыми компонентами

## Real World Example

### Epic 3 Handoff Package (88% score)

```json
{
  "from_role": "coder",
  "to_role": "reviewer",
  "epic_id": "epic3-standards-handoff-automation",
  "files": [
    {
      "path": "docs/memos/2024-06-epic-mcp-integration-epic3-standards-handoff.md",
      "type": "summary",
      "priority": 1
    },
    {
      "path": "data/knowledge/handoff_best_practices_synthesis_2025-01-05.md",
      "type": "lessons",
      "priority": 2
    },
    {
      "path": "data/audit/rules_audit_epic3_2025-01-05.md",
      "type": "audit",
      "priority": 4
    },
    {
      "path": "project_state.json",
      "type": "metadata",
      "priority": 5
    }
  ],
  "startup_prompt": "[review] Resuming Epic 3: Standards and automation of atomic rules, handoff and context transfer. Status: automation phase completed with full handoff validation system. Infrastructure: FastAPI endpoints, CLI tool, atomic rules updated. Lessons: structured validation critical for handoff quality. Constraints: must maintain .mdc_ work protocol. Next: validate real-world usage, complete documentation.",
  "control_questions": [
    "What is current Epic 3 status and what automation components have been implemented?",
    "What technical components (API, CLI, validators) are ready for testing?",
    "What scope constraints must be maintained including .mdc_ work protocol?",
    "How should the handoff validation workflow be integrated with CI/CD?",
    "What are the immediate next steps for completing Epic 3?"
  ]
}
```

## CLI Commands Reference

### validate
```bash
python src/llmgenie/cli/handoff_cli.py validate <config.json> [--verbose] [--project-root DIR]
```
- Полная валидация с детальным анализом
- `--verbose` - показать детальную breakdown валидации
- `--project-root` - указать корень проекта (по умолчанию: текущая директория)

### template
```bash
python src/llmgenie/cli/handoff_cli.py template <output.json>
```
- Генерация шаблона handoff пакета
- Создает базовую структуру для редактирования

### check
```bash
python src/llmgenie/cli/handoff_cli.py check <config.json> [--fail-on-warnings]
```
- CI/CD режим с минимальным выводом
- `--fail-on-warnings` - завершать с ошибкой при предупреждениях
- Возвращает exit code 0 (success) или 1 (failure)

## API Endpoints

### GET /handoff/template
Получение шаблона handoff пакета.

**Response:**
```json
{
  "template": {...},
  "validation_requirements": {...}
}
```

### POST /handoff/validate
Валидация handoff пакета.

**Request:** HandoffPackage JSON
**Response:** ValidationResult с детальным анализом

## Best Practices

### 1. Preparation Phase
- Собрать все ключевые файлы до создания пакета
- Проверить актуальность содержимого файлов
- Убедиться что файлы содержат релевантную информацию

### 2. Startup Prompt Guidelines
- **Status** - четкий текущий статус и прогресс
- **Infrastructure** - техническое состояние, готовые компоненты
- **Lessons** - ключевые выводы и уроки
- **Constraints** - ограничения scope, протоколы
- **Next Steps** - конкретные следующие действия

### 3. Control Questions Design
- Вопросы о статусе и прогрессе
- Технические вопросы о готовности компонентов
- Вопросы о scope и ограничениях
- Вопросы о workflow и интеграции

### 4. CI/CD Integration
```yaml
# GitHub Actions example
- name: Validate Handoff Package
  run: |
    python src/llmgenie/cli/handoff_cli.py check handoff_config.json --fail-on-warnings
```

## Troubleshooting

### Common Issues

**Low Completeness Score**
- Проверить существование всех файлов
- Убедиться что файлы не пустые
- Дополнить startup prompt недостающими компонентами

**Missing File Types**
- Добавить файлы всех 5 обязательных типов
- Проверить правильность указания типов в конфигурации

**API Connection Issues**
- Убедиться что FastAPI сервер запущен: `python src/llmgenie/api/main.py`
- Проверить порт 8000: `curl http://localhost:8000/health`

## Integration with Workflow

Handoff validation интегрируется с:
- **ai_workflow.json** - stage `handoff_validation`
- **Atomic rules** - `016_context_transfer_protocol`
- **Session logs** - автоматическое логирование
- **CI/CD pipelines** - проверка quality gates

## Universal Applications

Система handoff validation применима для:
- **Software Development** - передача между разработчиками
- **Scientific Research** - передача между исследователями  
- **Business Processes** - передача между отделами
- **Education** - передача между преподавателями
- **AI/LLM workflows** - передача между AI моделями

---

**Links:**
- [Handoff Best Practices](../data/knowledge/handoff_best_practices_synthesis_2025-01-05.md)
- [Context Transfer Protocol](../.cursor/rules/core/016_context_transfer_protocol.mdc_)
- [API Documentation](API.md)
- [Project State](../project_state.json) 