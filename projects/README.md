# Projects Directory

This directory contains external projects that llmgenie assists with.

## Structure

Each project should be organized as follows:
```projects/
├── project_name/
│   ├── source_code/          # Project source files (symlink or copy)
│   ├── .llmgenie/           # LLMGenie-specific files
│   │   ├── config.json      # Project-specific configuration
│   │   ├── context.json     # Project context cache
│   │   ├── analysis/        # Analysis results
│   │   └── logs/           # Project-specific logs
│   └── README.md           # Project documentation
```

## Project Isolation

Each project is isolated with:
- Separate configuration
- Independent context
- Isolated logging
- Sandboxed execution

## Configuration

Project-specific configuration is loaded from:
1. `config/project_overrides/{project_name}.json`
2. `projects/{project_name}/.llmgenie/config.json`
3. Environment variables with `LLMGENIE_{PROJECT_NAME}_` prefix

## Usage

To work with a project:
```bash
# Initialize project
llmgenie init projects/my_project

# Analyze project
llmgenie analyze projects/my_project

# Start assistant mode
llmgenie assist projects/my_project
```

## Security

- Projects are sandboxed by default
- File access is restricted to project directory
- Network access can be controlled per project
- Sensitive data is isolated per project 