# Cross-Reference Standards for LLMGenie Documentation

**Version:** 1.0
**Phase:** 3B.2
**Created:** 2025-01-05
**Source:** docs/documentation_architecture_design.md

## 1. @-Reference System

### 1.1 Syntax

**Syntax:** `@{target_type}:{path}#{anchor}`

### 1.2 Reference Types

- `@human:` - References to docs/ (human-readable)
- `@ai:` - References to data/knowledge/ (AI-readable)
- `@code:` - References to source code
- `@issue:` - References to GitHub issues/PRs
- `@session:` - References to session logs

### 1.3 Examples

```markdown
@human:guides/setup_guide.md#installation
@ai:models/claude_integration.json#performance_metrics
@code:src/llmgenie/task_router/quality_intelligence.py#L45
@session:data/logs/sessions/session_docs_architecture_2025-01-05.jsonl
```

## 2. Bridge Mechanisms Between Human and AI KB

### 2.1 Bidirectional Links

```json
{
  "human_reference": "@human:guides/mcp_setup.md",
  "ai_reference": "@ai:techs/mcp_model_context_protocol.md",
  "sync_status": "synchronized",
  "last_sync": "2025-01-05T12:00:00Z"
}
```

### 2.2 Content Synchronization Rules

1. Technical specs live in AI KB, user guides in Human KB
2. Performance data and configs in AI KB, explanations in Human KB
3. Cross-references must be bidirectional and validated
4. Updates trigger sync validation checks

## 3. Validation Rules

### 3.1 Reference Integrity

- All @-references must resolve to existing files
- Anchors must exist in target documents
- Bidirectional links must be consistent
- Orphaned documents flagged for review

### 3.2 Automated Validation

**Validation Command (proposed):**
```bash
python scripts/validate_docs.py --check-references --check-sync
``` 