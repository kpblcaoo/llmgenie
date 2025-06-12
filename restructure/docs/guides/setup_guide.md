# LLMGenie Setup Guide

**Version:** 1.0
**Phase:** 3C.3
**Created:** 2025-01-05
**Model:** Gemini 2.5 Flash

## 1. Overview

This guide provides a step-by-step process for setting up the LLMGenie project locally, including its core components, API, and Ollama integration for cost-effective AI routing. LLMGenie orchestrates AI workflows with smart routing between various models (like Ollama and Claude) and integrates with IDEs like Cursor via the Model Context Protocol (MCP).

## 2. Prerequisites

Before you begin, ensure you have the following installed:

-   Python 3.9+
-   Docker (for Ollama)
-   `pip` (Python package installer)
-   `git` (for cloning the repository)
-   `curl` (for testing API endpoints)

## 3. Project Setup

### 3.1 Clone the Repository

First, clone the LLMGenie repository from your source control:

```bash
git clone <your-llmgenie-repo-url>
cd llmgenie
```

### 3.2 Install Dependencies

It's recommended to create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt # (Assuming requirements.txt exists with all deps)
```

### 3.3 Set Up Environment Variables (if applicable)

Create a `.env` file in the project root based on a `.env.example` (if provided) and fill in any necessary API keys or configurations.

## 4. Ollama Integration (Local AI Inference)

LLMGenie is designed to work seamlessly with Ollama for local, cost-effective AI model inference. Ensure Ollama is running and has the necessary models pulled.

### 4.1 Install and Run Ollama

Follow the official Ollama installation instructions for your OS: [https://ollama.ai/](https://ollama.ai/)

After installation, run Ollama:

```bash
ollama serve
```

### 4.2 Pull Recommended Models

LLMGenie's TaskRouter is configured to use specific Ollama models for tasks like code generation. Pull these models:

```bash
ollama pull mistral:7b-instruct
ollama pull codellama:7b
ollama pull mistral:latest
```

**Status:** Ollama running on `localhost:11434` with `mistral:7b-instruct`, `codellama:7b`, `mistral:latest` available.

## 5. Model Context Protocol (MCP) Integration for Cursor IDE

LLMGenie integrates with Cursor IDE via the Model Context Protocol (MCP) server, running on `localhost:8000/mcp`.

### 5.1 Verify MCP Server Status

Once the LLMGenie API is running (see Section 6), you can verify the MCP server:

```bash
curl http://localhost:8000/mcp
```

**Expected Output:** Streaming SSE pings, indicating the MCP server is active.

### 5.2 Configure Cursor IDE (Optional)

To enable full integration with Cursor IDE, ensure your Cursor configuration (`.cursor/mcp.json`) is set to use `llmgenie-handoff-validator` at `localhost:8000/mcp`.

## 6. Running the LLMGenie API

The LLMGenie API is built with FastAPI and serves as the central point for smart AI routing and other functionalities.

### 6.1 Start the API Server

Navigate to the project root and run the FastAPI application. (Assuming `main.py` is the entry point)

```bash
uvicorn src.llmgenie.api.main:app --host 0.0.0.0 --port 8000 --reload
```

### 6.2 Test API Endpoints

**Smart Agent Execution (Example):**

```bash
# Code generation (should route to Ollama)
curl -X POST localhost:8000/agents/execute \
  -H "Content-Type: application/json" \
  -d '{"agent_type": "auto", "task": "def add_numbers(a, b): return a + b"}'

# Architecture planning (should route to Claude - requires Claude API key)
curl -X POST localhost:8000/agents/execute \
  -H "Content-Type: application/json" \
  -d '{"agent_type": "auto", "task": "Design microservice architecture for user management"}'
```

**Handoff Validation (Example):**

```bash
curl -X POST localhost:8000/handoff/validate \
  -H "Content-Type: application/json" \
  -d '{"config": "your_handoff_config_json_here"}'
```

## 7. CLI Usage (Optional)

LLMGenie also provides CLI tools for managing tasks and sessions.

```bash
python src/llmgenie/cli/handoff_cli.py validate config.json --verbose
python src/llmgenie/cli/handoff_cli.py template output.json
```

## 8. Troubleshooting

-   **Ollama not running:** Ensure `ollama serve` is active.
-   **API connection issues:** Check port 8000 is not blocked and `uvicorn` is running.
-   **Model routing issues:** Verify `project_state.json` and `data/knowledge/capabilities/core_features.json` for correct configurations.

---

**Next Step:** Continue with other practical guides: `api_usage.md`, `troubleshooting.md`, `performance_tuning.md`. 