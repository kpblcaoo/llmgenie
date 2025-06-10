# LLMGenie Troubleshooting Guide

**Version:** 1.0
**Phase:** 3C.3
**Created:** 2025-01-05
**Model:** Gemini 2.5 Flash

## 1. Overview

This guide provides common troubleshooting steps for issues you might encounter while setting up or operating LLMGenie. It covers API connectivity, Ollama integration, model routing, and general workflow problems.

## 2. General Troubleshooting Steps

-   **Check Logs:** Always start by reviewing the session logs (`data/logs/sessions/session_*.jsonl`) and meta-logs (`data/logs/meta_log.jsonl`) for error messages or unusual activity.
-   **Verify Dependencies:** Ensure all project dependencies are installed and up to date (`pip install -r requirements.txt`).
-   **Restart Services:** A simple restart of Ollama, FastAPI, or your IDE can often resolve transient issues.
-   **Check Network Connectivity:** Confirm that required ports (e.g., 8000 for FastAPI, 11434 for Ollama) are not blocked by firewalls or other applications.
-   **Consult Documentation:** Refer to the `LLMGenie Setup Guide` (`@human:guides/setup_guide.md`) and API Usage Guide (`@human:guides/api_usage.md`) for correct setup and usage.

## 3. Common Issues and Solutions

### 3.1 API Connection Issues

**Problem:** Cannot connect to the LLMGenie API (e.g., `curl: (7) Failed to connect to localhost port 8000`).

**Solution:**
1.  **Is FastAPI Running?** Ensure the FastAPI server is active. You should see output similar to `INFO:     Uvicorn running on http://0.0.0.0:8000` in your terminal.
    ```bash
    uvicorn src.llmgenie.api.main:app --host 0.0.0.0 --port 8000 --reload
    ```
2.  **Port Conflict?** Another application might be using port 8000. Try changing the port in your `uvicorn` command (e.g., `--port 8001`).
3.  **Firewall:** Check if your firewall is blocking connections to port 8000.

### 3.2 Ollama Integration Problems

**Problem:** LLMGenie fails to use Ollama models, or Ollama is not responding.

**Solution:**
1.  **Is Ollama Server Running?** Open a separate terminal and run `ollama serve`.
2.  **Are Models Pulled?** Ensure you have pulled the necessary models (`ollama pull codellama:7b`, `ollama pull mistral:7b-instruct`, etc.) as specified in the Setup Guide.
3.  **Ollama Port:** By default, Ollama runs on `localhost:11434`. Verify this is correct and not blocked.
4.  **Model Routing Configuration:** Check `project_state.json` and `data/knowledge/capabilities/core_features.json` to ensure Ollama models are correctly configured for smart routing.

### 3.3 Model Routing Issues (Auto-routing not working as expected)

**Problem:** Tasks are not being routed to the expected AI model (e.g., code generation goes to Claude instead of Ollama).

**Solution:**
1.  **Task Classifier Accuracy:** Review the `task_classifier.py` logic. The classifier might be misinterpreting the task type.
2.  **Model Router Logic:** Inspect `model_router.py` to understand its decision-making process based on task complexity and model availability.
3.  **`project_state.json` & `core_features.json`:** Ensure model assignments and capabilities are accurately reflected in these files.
4.  **Fallback Triggered?** If Ollama returns low-quality results, the `QualityValidator` might automatically switch to a premium model (Claude). Check logs for `QualityValidator` fallback events.

### 3.4 Handoff Validation Failures

**Problem:** `POST /handoff/validate` returns errors or a low completeness score.

**Solution:**
1.  **Check Handoff Configuration:** Review your handoff JSON structure. It must align with the `handoff_validation` checklist in `data/ai_workflow.json`.
2.  **Required Fields:** Ensure all mandatory fields (e.g., `status_summary`, `lessons_learned`, `checklist`) are present and correctly populated.
3.  **File Existence:** If your `handoff_config` references specific files, ensure those files exist at the specified paths.
4.  **Control Questions:** Verify that the required number of control questions (minimum 3) is included.

### 3.5 General AI Output Quality Issues

**Problem:** AI-generated content is not meeting quality expectations.

**Solution:**
1.  **Prompt Engineering:** Refine your task prompts. Clear, concise, and detailed prompts lead to better results.
2.  **Context Provision:** Provide sufficient context to the AI for its task.
3.  **Model Selection:** For critical tasks, consider explicitly forcing a premium model (e.g., Claude) instead of relying solely on auto-routing.
4.  **`QualityValidator` Thresholds:** Adjust quality validation thresholds if necessary to be more strict or lenient.
5.  **Review `data/knowledge/`:** Ensure the AI Knowledge Base is up-to-date and accurate for the relevant domain.

---

**Next Step:** Continue with the final practical guide: `performance_tuning.md`. 