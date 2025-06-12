# Configuration Documentation

This directory contains documentation for llmgenie configuration system.

## Overview

LLMGenie uses a hierarchical configuration system with:
- Base defaults in `config/defaults.json`
- Profile-specific overrides in `config/profiles/`
- Project-specific overrides in `config/project_overrides/`

## Configuration Files

### Core Configuration
- **defaults.json** - Base configuration settings
- **profiles/** - Environment-specific profiles (dev, tool, prod)
- **project_overrides/** - Project-specific configuration overrides

### Profiles
- **dev.json** - Development environment settings
- **tool.json** - Tool assistant mode settings
- **prod.json** - Production environment settings (to be created)

## Configuration Schema

```json
{
  "llmgenie": {
    "version": "string",
    "mode": "assistant|tool_assistant|standalone",
    "default_profile": "string",
    "logging": { ... },
    "workspace": { ... },
    "ai_models": { ... },
    "features": { ... }
  }
}
```

## Usage

Configuration is loaded in this order:
1. Base defaults
2. Profile-specific overrides
3. Project-specific overrides
4. Environment variables
5. Command-line arguments

## See Also
- [Deployment Guide](../deployment/index.md)
- [Workflows](../workflows/index.md) 