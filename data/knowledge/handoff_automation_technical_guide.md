# Handoff Validation System - AI Technical Guide

## System Architecture

### Core Components

1. **HandoffValidator** (`src/llmgenie/api/handoff_validator.py`)
   - Main validation logic
   - Pydantic models for type safety
   - Scoring algorithm implementation
   - File existence and content validation

2. **CLI Tool** (`src/llmgenie/cli/handoff_cli.py`)
   - Command-line interface for all modes
   - Template generation
   - CI/CD integration support

3. **API Endpoints** (`src/llmgenie/api/main.py`)
   - REST API integration
   - FastAPI implementation
   - JSON response formatting

### Validation Algorithm

```python
# Completeness score calculation
completeness_score = (
    0.5 * file_score +      # File validation (50%)
    0.3 * prompt_score +    # Startup prompt (30%) 
    0.2 * questions_score   # Control questions (20%)
)

# Minimum thresholds
MIN_FILES_COUNT = 5
MIN_QUESTIONS_COUNT = 3
MIN_COMPLETENESS_SCORE = 0.8  # 80%
```

### Data Models

#### HandoffPackage
```python
class HandoffPackage(BaseModel):
    from_role: str
    to_role: str
    epic_id: str
    files: List[HandoffFile]
    startup_prompt: str
    control_questions: List[str]
    success_criteria: List[str]
    metadata: Dict
```

#### ValidationResult
```python
class ValidationResult(BaseModel):
    is_valid: bool
    completeness_score: float
    file_validation: Dict[str, bool]
    prompt_validation: StartupPrompt
    questions_validation: ControlQuestions
    missing_files: List[str]
    warnings: List[str]
    recommendations: List[str]
```

## Implementation Details

### File Validation Logic

```python
def _validate_files(self, files: List[HandoffFile]) -> Dict[str, bool]:
    validation = {}
    for file in files:
        file_path = self.project_root / file.path
        exists = file_path.exists()
        file.exists = exists
        if exists:
            file.size_bytes = file_path.stat().st_size
        validation[file.path] = exists and (file.size_bytes or 0) > 0
    return validation
```

### Startup Prompt Analysis

```python
def _validate_startup_prompt(self, prompt: str) -> StartupPrompt:
    prompt_lower = prompt.lower()
    return StartupPrompt(
        includes_status="status" in prompt_lower or "статус" in prompt_lower,
        includes_infrastructure="infrastructure" in prompt_lower,
        includes_lessons="lessons" in prompt_lower or "уроки" in prompt_lower,
        includes_constraints="scope" in prompt_lower or "ограничения" in prompt_lower,
        includes_next_steps="next steps" in prompt_lower
    )
```

### Required File Types Mapping

```python
REQUIRED_FILE_TYPES = [
    "summary",      # Quick overview/status
    "lessons",      # Detailed lessons learned  
    "checklist",    # Original checklist with progress
    "audit",        # Technical/audit report
    "metadata"      # Project state/metadata
]
```

## API Integration Points

### FastAPI Endpoints

#### POST /handoff/validate
- **Input:** HandoffPackage JSON
- **Output:** ValidationResult with detailed analysis
- **Error Handling:** HTTP 500 with error message

#### GET /handoff/template  
- **Output:** Template structure + validation requirements
- **Format:** JSON with nested template object

### CLI Commands Integration

#### validate mode
```bash
python src/llmgenie/cli/handoff_cli.py validate config.json --verbose
# Exit codes: 0 (valid), 1 (invalid)
```

#### check mode (CI/CD)
```bash
python src/llmgenie/cli/handoff_cli.py check config.json --fail-on-warnings
# Minimal output, CI/CD friendly
```

## Workflow Integration

### ai_workflow.json Stage

```json
"handoff_validation": {
  "description": "Валидация handoff пакета перед передачей контекста",
  "checklist": [
    "Создать handoff конфигурацию (JSON) с минимум 5 файлами",
    "Включить файлы типов: summary, lessons, checklist, audit, metadata",
    "Составить startup prompt с статусом, инфраструктурой, уроками, ограничениями",
    "Подготовить контрольные вопросы (минимум 3)",
    "Запустить валидацию: python src/llmgenie/cli/handoff_cli.py validate config.json",
    "Обеспечить completeness score >= 80%",
    "Исправить предупреждения и рекомендации валидатора"
  ],
  "automation": {
    "api_endpoint": "POST /handoff/validate",
    "cli_tool": "src/llmgenie/cli/handoff_cli.py",
    "template_endpoint": "GET /handoff/template",
    "ci_integration": "handoff_cli.py check --fail-on-warnings"
  }
}
```

### Atomic Rule Integration

Rule: `016_context_transfer_protocol.mdc_`
- Universal 3-phase protocol: Preparation → Transfer Package → Validation
- Applies to any handoff scenario
- Domain-agnostic implementation

## Testing Results

### Real Epic 3 Package (88% score)

**Files used:**
- `docs/memos/2024-06-epic-mcp-integration-epic3-standards-handoff.md` (summary)
- `data/knowledge/handoff_best_practices_synthesis_2025-01-05.md` (lessons)
- `data/audit/rules_audit_epic3_2025-01-05.md` (audit)
- `project_state.json` (metadata)

**Validation breakdown:**
- File validation: 4/4 files exist and non-empty ✅
- Prompt validation: status ✅, infrastructure ✅, lessons ✅, constraints ❌, next steps ❌  
- Questions validation: 5 questions, covers status ✅, technical ✅, scope ✅

## Error Handling & Fallbacks

### Import Fallback
```python
try:
    from .handoff_validator import HandoffPackage, ValidationResult, HandoffValidator
except ImportError:
    # Fallback for direct execution
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    from handoff_validator import HandoffPackage, ValidationResult, HandoffValidator
```

### CLI Error Handling
- FileNotFoundError: Clear error message + exit code 1
- JSON parsing errors: Descriptive error + exit code 1
- Validation failures: Detailed breakdown + exit code 1

## Performance Considerations

### File I/O Optimization
- Lazy file reading (only when needed)
- Path validation before content reading
- Efficient file existence checking

### Memory Management
- Streaming file processing for large files
- Minimal memory footprint for validation
- Garbage collection friendly implementation

## Extension Points

### Custom Validation Rules
```python
def add_custom_validator(self, validator_func):
    """Add custom validation logic"""
    self.custom_validators.append(validator_func)
```

### Domain-Specific Adaptations
- Software development: code review checklists
- Scientific research: data validation requirements
- Business processes: compliance checkpoints
- Education: learning outcome validation

## AI/LLM Integration Patterns

### Context Transfer Protocol
1. **Package Creation:** AI generates handoff config based on current state
2. **Validation:** Automated validation ensures completeness
3. **Transfer:** Validated package passed to target AI/human
4. **Restoration:** Target uses startup prompt + control questions

### Ollama Integration (Future)
```python
def create_ollama_handoff_prompt(validated_package: HandoffPackage) -> str:
    """Generate Ollama-specific handoff prompt from validated package"""
    return f"""
    Role: {validated_package.to_role}
    Context: {validated_package.startup_prompt}
    Files: {[f.path for f in validated_package.files]}
    Validation: {validated_package.control_questions}
    """
```

## Security Considerations

### File Access Controls
- Restricted to project root directory
- No arbitrary file system access
- Path traversal protection

### Input Validation
- Pydantic model validation
- JSON schema enforcement  
- Size limits on inputs

## Monitoring & Logging

### Validation Metrics
- Completeness score distribution
- Common failure patterns
- File type usage statistics

### Session Integration
```python
# Automatic logging to session logs
checkpoint = {
    "action": "handoff_validation",
    "package_id": package.epic_id,
    "completeness_score": result.completeness_score,
    "validation_status": result.is_valid
}
```

---

**Related Files:**
- Implementation: `src/llmgenie/api/handoff_validator.py`
- CLI: `src/llmgenie/cli/handoff_cli.py` 
- API: `src/llmgenie/api/main.py`
- Workflow: `data/ai_workflow.json`
- Rules: `.cursor/rules/core/016_context_transfer_protocol.mdc_`
- Knowledge: `data/knowledge/handoff_best_practices_synthesis_2025-01-05.md` 