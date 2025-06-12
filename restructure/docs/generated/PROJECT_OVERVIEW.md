# Project Overview

## Core Modules

### core.llmgenie
Main orchestrator for AI workflows. Provides the CLI and API interfaces, implements intelligent task routing across supported models (e.g., Claude, GPT, Ollama), and integrates the Model Context Protocol (MCP) for IDE and agent interoperability.

### core.rag_context
Supplies context-aware data to AI agents and workflows using retrieval-augmented generation (RAG) strategies. Incorporates structured rule logic and context injection via `struct.json`.

### core.struct_tools
Provides tools for structural project analysis, modular indexing, and architecture mapping. Supports tasks like dependency visualization, refactoring preview, and module mapping.

## Module Dependency Diagram

core.llmgenie
├── core.rag_context
└── core.struct_tools

- `core.llmgenie` is the entry point and orchestrator.
- `core.rag_context` and `core.struct_tools` are support modules used for context and structure respectively. 