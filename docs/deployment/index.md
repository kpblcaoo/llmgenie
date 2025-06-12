# Deployment Documentation

This directory contains documentation for deploying llmgenie in different environments.

## Overview

LLMGenie can be deployed in several modes:
- **Standalone** - Independent tool for project analysis
- **Tool Assistant** - Integrated assistant for other projects
- **MCP Server** - Model Context Protocol server
- **Docker Container** - Containerized deployment

## Deployment Modes

### Tool Assistant Mode
Deploy llmgenie as an assistant for other projects:
- Integrates with existing project workflows
- Provides context-aware suggestions
- Maintains project isolation

### MCP Server Mode
Deploy as a Model Context Protocol server:
- Provides structured AI capabilities
- Integrates with Cursor, VSCode, and other editors
- Supports multiple concurrent projects

### Standalone Mode
Deploy as an independent analysis tool:
- Project structure analysis
- Code quality assessment
- Documentation generation

## Deployment Targets

### Local Development
- Direct Python execution
- Virtual environment setup
- Development server mode

### Docker Deployment
- Containerized execution
- Multi-stage builds
- Production-ready images

### Cloud Deployment
- Serverless functions
- Container orchestration
- Scalable infrastructure

## Configuration

Each deployment mode uses specific configuration profiles:
- `dev.json` - Development environment
- `tool.json` - Tool assistant mode
- `prod.json` - Production environment

## See Also
- [Configuration Guide](../configs/index.md)
- [Workflows](../workflows/index.md)
- [Architecture](../architecture/phase2/index.md) 