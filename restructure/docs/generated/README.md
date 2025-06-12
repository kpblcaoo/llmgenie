# LLMGenie (restructured)

> Orchestration, automation, and integration of AI assistants and workflows with smart routing between models.

## Directory Overview

- `core/` — Main source code modules:
    - `llmgenie/` — Orchestration, CLI, API, TaskRouter, MCP integration
    - `rag_context/` — Context enhancement and RAG tools
    - `struct_tools/` — Project structure analysis and modular index tools
- `docs/` — Documentation, onboarding, best practices, architecture, plans
- `archive/` — Archived, backup, and legacy files
- `unused/` — Unused, large, or temporary files (e.g., bfg.jar, caches)
- `.cursor/` — Cursor IDE rules, session configs, and automation settings
- `logs/` — Logs and reports for restructuring, testing, and validation
- `tests/` — Test suite for all core modules

## Installation

```bash
# Install in editable mode (recommended for development)
pip install -e .

# Or use pyproject.toml (PEP 517/518)
pip install .
```

## Basic Usage

### CLI

Run the main CLI:
```bash
python -m core.llmgenie.cli <command> [options]
```
Or, if installed as a script:
```bash
llmgenie <command> [options]
```

### API

Run the FastAPI server (for MCP, TaskRouter, etc):
```bash
uvicorn core.llmgenie.api.main:app --reload
```

## Further Documentation

- [Onboarding & Best Practices](../docs/ONBOARDING_LLMGENIE.md)
- [Quick Start MCP](../docs/QUICK_START_MCP.md)
- [Project Vision](../docs/PROJECT_VISION.md)
- [Struct Tools Guide](../docs/struct_tools_README.md)
- [TaskRouter User Guide](../docs/taskrouter/user_guide.md)
- [Full Documentation Index](../docs/) 