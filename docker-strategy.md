# 🐳 LLMGenie Docker Strategy

## 🎯 Цель: Удобное развертывание без раздувания образов

### Проблема: Размер зависимостей
- **Ollama models**: 4-7GB каждая модель
- **Python deps**: ~500MB  
- **llmstruct**: ~100MB
- **Project code**: ~50MB

### 💡 Решение: Multi-container + volumes

## 📦 Архитектура контейнеров

### 1. llmgenie-core (Base service)
```dockerfile
FROM python:3.11-slim
# Только Python dependencies + llmgenie код
# Размер: ~600MB
```

### 2. ollama-service (Optional)
```dockerfile  
FROM ollama/ollama:latest
# Ollama + models в отдельном контейнере
# Размер: 4-7GB, но опциональный
```

### 3. Development volumes
```yaml
volumes:
  - ./projects:/workspace/projects  # Проекты пользователя
  - ./cache:/workspace/.cache       # Кэш и struct.json
  - ./models:/workspace/models      # Модели (опционально)
```

## 🚀 Docker Compose Example

```yaml
version: '3.8'

services:
  llmgenie:
    build: .
    ports:
      - "8000:8000"  # MCP server
    volumes:
      - ./projects:/workspace/projects
      - ./cache:/workspace/.cache
      - ./config:/workspace/config
    environment:
      - PYTHONPATH=/workspace/src
    command: python -m rag_context.interfaces.mcp_server

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ./models:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0
    # Запускается только если нужен

  struct-tools:
    build: .
    volumes:
      - ./projects:/workspace/projects
      - ./cache:/workspace/.cache
    entrypoint: ["python", "-m", "struct_tools.cli_interface"]
    # On-demand container для анализа
```

## 🔧 Optimized Dockerfile

```dockerfile
# Multi-stage build для минимизации размера
FROM python:3.11-slim as base

# System dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base as runtime
WORKDIR /workspace

# Copy only necessary code
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY .cursor/ ./.cursor/

# Make scripts executable
RUN chmod +x scripts/*

# Setup Python path
ENV PYTHONPATH=/workspace/src

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Default command
CMD ["python", "-m", "rag_context.interfaces.mcp_server"]
```

## 📋 Usage Patterns

### Development Mode
```bash
# Запуск для разработки проекта X
docker-compose -f docker-compose.dev.yml up llmgenie

# Анализ структуры проекта Y
docker-compose run struct-tools generate /workspace/projects/project-y/src
```

### Production Mode
```bash
# Только MCP server + RAG
docker run -p 8000:8000 -v $(pwd)/projects:/workspace/projects llmgenie:latest
```

### Multi-project Mode
```bash
# Разные проекты, один llmgenie
docker run -v /path/to/projects:/workspace/projects llmgenie struct-tools generate project-a/src
docker run -v /path/to/projects:/workspace/projects llmgenie struct-tools generate project-b/src
```

## 🎯 Benefits

### Размер оптимизирован:
- **Core image**: ~600MB (без моделей)
- **С Ollama**: +4-7GB только если нужно
- **Модели в volume**: не пересобираются

### Гибкость:
- **Разные проекты** через volumes
- **Опциональный Ollama** (можно использовать внешний)
- **Отдельные контейнеры** для разных задач

### Production-ready:
- **Health checks**
- **Multi-stage builds**
- **Minimal attack surface** 