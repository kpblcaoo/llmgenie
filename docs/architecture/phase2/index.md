# Phase 2 Architecture Documentation

This directory contains architectural documentation for llmgenie Phase 2 - Tool Assistant Mode.

## Overview

Phase 2 transforms llmgenie from a standalone tool into a comprehensive assistant for other projects. The architecture focuses on:
- Modular design for easy integration
- Project isolation and sandboxing
- Scalable configuration system
- Multi-mode operation support

## Architecture Components

### Core Components
- **Configuration System** - Hierarchical configuration management
- **Project Manager** - Project isolation and lifecycle management
- **Context Engine** - Project context analysis and maintenance
- **Workflow Engine** - Automated workflow execution

### Integration Layer
- **MCP Server** - Model Context Protocol implementation
- **Editor Plugins** - Cursor/VSCode integration
- **CLI Interface** - Command-line tool interface
- **API Gateway** - REST/GraphQL API endpoints

### AI Components
- **RAG Context** - Retrieval-Augmented Generation system
- **Struct Tools** - Project structure analysis tools
- **Model Router** - AI model selection and routing
- **Quality Intelligence** - Code quality assessment

## Design Principles

### Modularity
- Loosely coupled components
- Plugin-based architecture
- Configurable feature sets

### Isolation
- Project sandboxing
- Resource isolation
- Security boundaries

### Scalability
- Horizontal scaling support
- Async processing
- Resource optimization

### Extensibility
- Plugin system
- Custom workflow support
- Third-party integrations

## Deployment Architecture

### Standalone Mode
```
┌─────────────────┐
│   LLMGenie CLI  │
├─────────────────┤
│  Core Engine    │
├─────────────────┤
│  Local Storage  │
└─────────────────┘
```

### Tool Assistant Mode
```
┌─────────────────┐    ┌─────────────────┐
│   Editor/IDE    │◄──►│   MCP Server    │
└─────────────────┘    ├─────────────────┤
                       │  LLMGenie Core  │
┌─────────────────┐    ├─────────────────┤
│  Project Files  │◄──►│ Project Manager │
└─────────────────┘    └─────────────────┘
```

### Server Mode
```
┌─────────────────┐    ┌─────────────────┐
│   Web Client    │◄──►│   API Gateway   │
├─────────────────┤    ├─────────────────┤
│   CLI Client    │◄──►│  LLMGenie Core  │
├─────────────────┤    ├─────────────────┤
│  MCP Client     │◄──►│ Storage Layer   │
└─────────────────┘    └─────────────────┘
```

## Configuration Architecture

### Hierarchical Configuration
1. **Base Defaults** (`config/defaults.json`)
2. **Profile Overrides** (`config/profiles/*.json`)
3. **Project Overrides** (`config/project_overrides/*.json`)
4. **Environment Variables**
5. **Runtime Parameters**

### Profile System
- **dev** - Development environment
- **tool** - Tool assistant mode
- **prod** - Production environment
- **custom** - User-defined profiles

## See Also
- [Configuration Guide](../../configs/index.md)
- [Deployment Guide](../../deployment/index.md)
- [Workflows](../../workflows/index.md) 