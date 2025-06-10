# LLMGenie Performance Tuning Guide

**Version:** 1.0
**Phase:** 3C.3
**Created:** 2025-01-05
**Model:** Gemini 2.5 Flash

## 1. Overview

This guide provides recommendations and strategies for optimizing the performance of the LLMGenie project. It focuses on reducing latency, improving throughput, and optimizing resource utilization, particularly for AI model inference.

## 2. Key Performance Metrics

-   **Latency:** Time taken to complete a single task (e.g., API response time, code generation time).
-   **Throughput:** Number of tasks processed per unit of time.
-   **API Cost Savings:** Reduction in expenditure on external LLM APIs (primarily through Ollama integration).
-   **Resource Utilization:** CPU, GPU, memory, and network usage.

## 3. Ollama Optimization

Ollama is crucial for cost-effective local AI inference. Optimizing its performance directly impacts LLMGenie's efficiency.

### 3.1 Model Selection

-   **Smaller Models:** For routine tasks (e.g., simple code generation, summarization), prefer smaller, faster Ollama models (e.g., `mistral:7b-instruct`, `codellama:7b`).
-   **Quantized Models:** Use quantized versions of models if available (`-q4_0`, `-q8_0`) to reduce memory footprint and increase inference speed, potentially at a slight quality trade-off.

### 3.2 Hardware Acceleration

-   **GPU Usage:** Ensure Ollama is configured to use your GPU if available. This significantly speeds up inference.
-   **Sufficient RAM:** Allocate enough RAM to Ollama to load models fully into memory, avoiding disk swaps.

### 3.3 Ollama Server Configuration

-   **Dedicated Instance:** For heavy workloads, consider running Ollama on a dedicated machine or Docker container.
-   **Keep Alive:** Configure `ollama serve` with `--keep-alive` to prevent models from being unloaded between requests.

## 4. LLMGenie API (FastAPI) Optimization

### 4.1 Asynchronous Operations

-   **`async/await`:** Ensure FastAPI endpoints and underlying logic (especially interactions with LLMs) use `async/await` for non-blocking I/O.
-   **`run_in_threadpool`:** Use `uvicorn.run_in_threadpool` for blocking operations (e.g., some database calls, synchronous third-party libraries) to prevent blocking the event loop.

### 4.2 Worker Processes

-   **Uvicorn Workers:** Increase the number of Uvicorn workers based on your CPU cores to handle more concurrent requests.
    ```bash
    uvicorn src.llmgenie.api.main:app --host 0.0.0.0 --port 8000 --workers 4
    ```

### 4.3 Response Optimization

-   **Pydantic Models:** Use Pydantic models for request and response validation/serialization. This ensures efficient data handling.
-   **Streaming Responses (SSE):** For long-running AI tasks, consider streaming responses (as seen in `/mcp` endpoint) to provide real-time updates and improve perceived latency.

## 5. Smart AI Routing Optimization

LLMGenie's core strength is intelligent model routing. Optimize its configuration for maximum benefit.

### 5.1 Task Classifier Tuning

-   **Accuracy:** Regularly evaluate the `TaskClassifier`'s accuracy. A more accurate classifier ensures tasks are routed to the most optimal model.
-   **Confidence Thresholds:** Adjust confidence thresholds for task classification to balance between cost savings (Ollama) and quality (Claude).

### 5.2 Quality Validator Tuning

-   **Validation Logic:** Optimize the `QualityValidator`'s logic to be efficient and effective. Avoid overly complex or slow validation steps.
-   **Fallback Strategy:** Review and fine-tune the automatic fallback logic. Ensure it correctly identifies low-quality outputs and switches to a premium model when necessary.

## 6. General Code Optimization

-   **Profiling:** Use Python profiling tools (e.g., `cProfile`, `py-spy`) to identify performance bottlenecks in your code.
-   **Caching:** Implement caching for frequently accessed data or expensive computations.
-   **Database Optimization:** If applicable, optimize database queries and indexing.
-   **Efficient Data Structures:** Use appropriate Python data structures for better performance (e.g., `set` for fast lookups).

## 7. Monitoring and Logging

-   **Structured Logging:** Implement structured logging for performance metrics (latency, model usage, errors) to easily analyze data.
-   **Monitoring Tools:** Integrate with monitoring tools (e.g., Prometheus, Grafana) to track real-time performance and identify trends.
-   **Alerting:** Set up alerts for critical performance deviations (e.g., high latency, increased error rates).

---

**Next Step:** Document the completion of Phase 3C and prepare for Phase 4A. 