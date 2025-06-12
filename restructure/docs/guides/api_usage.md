# LLMGenie API Usage Guide

**Version:** 1.0
**Phase:** 3C.3
**Created:** 2025-01-05
**Model:** Gemini 2.5 Flash

## 1. Overview

This guide provides detailed instructions on how to interact with the LLMGenie REST API. The API serves as the central interface for smart AI routing, agent execution, handoff validation, and various project insights.

## 2. Base URL and Authentication

**Base URL:** `http://localhost:8000` (assuming default local setup)

**Authentication:** Currently, the API does not require authentication for local development. For production deployments, implement appropriate security measures (e.g., API keys, OAuth2).

## 3. Key Endpoints

### 3.1 POST `/agents/execute` - Smart AI Execution

This is the primary endpoint for executing AI tasks with intelligent model routing (Ollama for routine, Claude for complex).

-   **Method:** `POST`
-   **Description:** Submits a task for AI processing, with automatic model selection.
-   **Request Body (`application/json`):**

    ```json
    {
      "agent_type": "auto" | "ollama" | "claude",
      "task": "string",
      "context": "string" (optional)
    }
    ```

    -   `agent_type`: `auto` (default, LLMGenie decides), `ollama` (force Ollama), `claude` (force Claude).
    -   `task`: The task description for the AI.
    -   `context`: Additional context for the AI.

-   **Example (Auto-routing):**

    ```bash
    curl -X POST http://localhost:8000/agents/execute \
      -H "Content-Type: application/json" \
      -d '{"agent_type": "auto", "task": "Write a Python function to calculate factorial."}'
    ```

-   **Example (Force Ollama):**

    ```bash
    curl -X POST http://localhost:8000/agents/execute \
      -H "Content-Type: application/json" \
      -d '{"agent_type": "ollama", "task": "Summarize this text: Long text goes here."}'
    ```

-   **Example (Force Claude - requires Claude API key in environment):**

    ```bash
    curl -X POST http://localhost:8000/agents/execute \
      -H "Content-Type: application/json" \
      -d '{"agent_type": "claude", "task": "Design a scalable database schema for an e-commerce platform."}'
    ```

### 3.2 POST `/handoff/validate` - Handoff Package Validation

Validates a handoff package to ensure completeness and adherence to standards for context transfer.

-   **Method:** `POST`
-   **Description:** Validates a JSON-based handoff configuration.
-   **Request Body (`application/json`):**

    ```json
    {
      "config": {
        "status_summary": "string",
        "lessons_learned": [],
        "checklist": {},
        "audit_report": {},
        "project_metadata": {},
        "startup_prompt": "string",
        "control_questions": [],
        "success_criteria": "string"
      }
    }
    ```

    *(Note: The `config` structure should align with your `data/ai_workflow.json` handoff_validation checklist.)*

-   **Example:**

    ```bash
    curl -X POST http://localhost:8000/handoff/validate \
      -H "Content-Type: application/json" \
      -d '{"config": {"status_summary": "Phase X completed...", "lessons_learned": [], "checklist": {}, "audit_report": {}, "project_metadata": {}, "startup_prompt": "...", "control_questions": [], "success_criteria": "..."}}'
    ```

### 3.3 GET `/handoff/template` - Handoff Template Retrieval

Retrieves a template for creating a handoff package.

-   **Method:** `GET`
-   **Description:** Returns a JSON template for handoff configuration.
-   **Example:**

    ```bash
    curl http://localhost:8000/handoff/template
    ```

### 3.4 GET `/health` - API Health Check

Checks the operational status of the API.

-   **Method:** `GET`
-   **Description:** Returns the health status of the API.
-   **Example:**

    ```bash
    curl http://localhost:8000/health
    ```

### 3.5 GET `/project/state` - Project State Retrieval

Retrieves the current state of the LLMGenie project.

-   **Method:** `GET`
-   **Description:** Returns the contents of `project_state.json`.
-   **Example:**

    ```bash
    curl http://localhost:8000/project/state
    ```

### 3.6 GET `/mcp` - Model Context Protocol (MCP) Endpoint

Provides an SSE (Server-Sent Events) endpoint for Cursor IDE integration.

-   **Method:** `GET`
-   **Description:** Streams MCP events for IDE context synchronization.
-   **Example:**

    ```bash
    curl http://localhost:8000/mcp
    ```

## 4. Error Handling

-   **HTTP Status Codes:** API will return standard HTTP status codes (e.g., 200 OK, 400 Bad Request, 500 Internal Server Error).
-   **Error Responses:** Error bodies will typically be JSON objects with an `"error"` field and a descriptive message.

## 5. Rate Limiting (Future)

For production deployments, rate limiting will be implemented to prevent abuse and ensure fair usage.

---

**Next Step:** Continue with other practical guides: `troubleshooting.md`, `performance_tuning.md`. 