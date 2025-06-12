# LLMGenie Documentation Architecture Design

**Version:** 1.0  
**Phase:** 3A.2  
**Created:** 2025-01-05  
**Model:** Claude 4 Sonnet  

## Executive Summary

Comprehensive architectural design for modular documentation system supporting dual knowledge bases: Human-readable documentation (docs/) and AI-readable knowledge base (data/knowledge/). Design ensures consistency, automation, and seamless cross-referencing between both systems.

## 1. Hierarchical Structure Design

### 1.1 Unified Taxonomy

**Root Categories:**
```
llmgenie/
├── docs/                     # Human Knowledge Base
│   ├── docs.json            # Central modular index
│   ├── index/               # Modular JSON documents  
│   ├── guides/              # Step-by-step tutorials
│   ├── architecture/        # System design documents
│   ├── decisions/           # Decision memos and ADRs
│   ├── workflows/           # Process documentation
│   └── archive/             # Historical documents
└── data/knowledge/          # AI Knowledge Base
    ├── README.md            # AI KB overview
    ├── common.json          # Shared entities and taxonomy
    ├── capabilities/        # LLMGenie project capabilities & features
    ├── techs/               # Technical integrations
    ├── envs/                # Environment configurations
    ├── models/              # AI/LLM model specifics
    ├── templates/           # Reusable templates
    └── projects/            # External projects knowledge
        ├── internal/        # Internal development projects
        └── commercial/      # Client/commercial projects
```

### 1.2 Naming Conventions

**Human KB (docs/):**
- **Files:** `lowercase_with_underscores.md`
- **Directories:** `lowercase_singular` (guides, architecture, decisions)
- **Index files:** `category_name.json` in `docs/index/`
- **Archives:** `docs/archive/{year}/{category}/`

**AI KB (data/knowledge/):**
- **Files:** `snake_case.json` for configs, `.md` for technical guides
- **Categories:** `plural_nouns` (techs, envs, models, templates)
- **Integration files:** `{technology}_integration.json`
- **Versioning:** Include `last_reviewed` dates in JSON metadata

### 1.3 Directory Structure Evolution Plan

**Phase 1 (Current):** Basic modular structure ✅
**Phase 2 (Next):** Enhanced categorization with guides/ and architecture/
**Phase 3 (Future):** Automated cross-reference validation
**Phase 4 (Advanced):** AI-assisted content generation and synchronization

## 2. Cross-Reference Standards

### 2.1 @-Reference System

**Syntax:** `@{target_type}:{path}#{anchor}`

**Reference Types:**
- `@human:` - References to docs/ (human-readable)
- `@ai:` - References to data/knowledge/ (AI-readable)  
- `@code:` - References to source code
- `@issue:` - References to GitHub issues/PRs
- `@session:` - References to session logs

**Examples:**
```markdown
@human:guides/setup_guide.md#installation
@ai:models/claude_integration.json#performance_metrics
@code:src/llmgenie/task_router/quality_intelligence.py#L45
@session:data/logs/sessions/session_docs_architecture_2025-01-05.jsonl
```

### 2.2 Bridge Mechanisms Between Human and AI KB

**Bidirectional Links:**
```json
{
  "human_reference": "@human:guides/mcp_setup.md",
  "ai_reference": "@ai:techs/mcp_model_context_protocol.md",
  "sync_status": "synchronized",
  "last_sync": "2025-01-05T12:00:00Z"
}
```

**Content Synchronization Rules:**
1. Technical specs live in AI KB, user guides in Human KB
2. Performance data and configs in AI KB, explanations in Human KB
3. Cross-references must be bidirectional and validated
4. Updates trigger sync validation checks

### 2.3 Validation Rules

**Reference Integrity:**
- All @-references must resolve to existing files
- Anchors must exist in target documents
- Bidirectional links must be consistent
- Orphaned documents flagged for review

**Automated Validation:**
```bash
# Validation command (proposed)
python scripts/validate_docs.py --check-references --check-sync
```

## 3. Automation Tools Design

### 3.1 Auto-Generation Strategies

**Documentation Generators:**
```python
# docs/generators/
├── api_docs_generator.py     # From code annotations
├── config_docs_generator.py  # From JSON schemas  
├── changelog_generator.py    # From git history
└── cross_ref_generator.py    # Reference maps
```

**Integration with Workflow:**
- Triggered by AI workflow stages (ai_workflow.json)
- Pre-commit hooks for validation
- CI/CD integration for docs deployment
- Session-based updates during development

### 3.2 Update Propagation

**Change Detection:**
```json
{
  "watchers": [
    {
      "source": "src/llmgenie/task_router/",
      "triggers": ["@human:architecture/task_routing.md", "@ai:techs/task_routing_config.json"]
    },
    {
      "source": "data/knowledge/models/",
      "triggers": ["@human:guides/model_selection.md"]
    }
  ]
}
```

**Propagation Rules:**
1. Code changes → update technical docs
2. AI KB updates → sync human explanations
3. Performance data changes → update both KBs
4. New integrations → generate documentation templates

### 3.3 Quality Assurance

**Validation Pipeline:**
1. **Syntax Check:** Markdown linting, JSON validation
2. **Reference Check:** @-reference resolution
3. **Content Check:** Consistency between Human/AI KB
4. **Quality Check:** Completeness scores for new documents

## 4. AI Integration Strategy

### 4.1 AI Consumption Patterns

**How AI Should Read Documentation:**
```python
# AI reading priority
1. data/knowledge/common.json          # Core entities and taxonomy
2. data/knowledge/capabilities/        # LLMGenie project capabilities
3. data/knowledge/{domain}/            # Domain-specific configs
4. data/knowledge/projects/{project}/  # Project-specific context (if applicable)
5. docs/index/{domain}.json            # Human-readable summaries
6. docs/guides/{specific_guide}.md     # Detailed procedures
```

**Context Loading Strategy:**
- Load common.json first for shared vocabulary
- Load domain-specific AI KB for technical details
- Reference human guides for procedural context
- Validate understanding through cross-references

### 4.2 AI Content Generation Templates

**Template System:**
```markdown
# AI-Generated Content Template
## Metadata
- Generated: {timestamp}
- Model: {model_name}
- Source: {@ai:path/to/source.json}
- Human Review: {required|optional}

## Content
{generated_content}

## Validation
- [ ] Technical accuracy verified
- [ ] Cross-references validated  
- [ ] Human review completed (if required)
```

**Quality Standards:**
- All AI-generated content marked with metadata
- Technical content requires human validation
- Cross-references auto-generated and validated
- Version control for generated content iterations

### 4.3 Human Review Workflows

**Review Triggers:**
- New AI-generated technical documentation
- Changes to critical system components
- Cross-reference inconsistencies detected
- Performance metric updates

**Review Process:**
1. AI generates content with metadata
2. Automated validation (syntax, references)
3. Human review for accuracy and clarity
4. Merge to documentation with approval
5. Update cross-reference mappings

## 5. Implementation Roadmap

### Phase 3B: Structure Implementation (Next)
- [ ] Create enhanced directory structure
- [ ] Implement @-reference system
- [ ] Set up basic validation scripts
- [ ] Migrate existing docs to new structure

### Phase 3C: Automation Setup
- [ ] Implement auto-generation tools
- [ ] Set up change detection and propagation
- [ ] Create quality assurance pipeline
- [ ] Integrate with AI workflow

### Phase 4: Advanced Features
- [ ] AI-assisted content generation
- [ ] Real-time synchronization
- [ ] Advanced analytics and insights
- [ ] Multi-language support

## 6. Success Metrics

**Quality Metrics:**
- Reference integrity: 100% valid @-references
- Sync status: <24h lag between Human/AI KB updates
- Coverage: All technical components documented
- Automation: 80% of routine docs auto-generated

**Usage Metrics:**
- AI comprehension: Reduced context-loading time
- Human usability: Faster onboarding and troubleshooting
- Maintenance: Reduced manual documentation effort
- Accuracy: Fewer docs-related support issues

## 7. LLMGenie Capabilities Knowledge & External Projects

### 7.1 Project Capabilities (data/knowledge/capabilities/)

**Core Capabilities Documentation:**
```json
// capabilities/core_features.json
{
  "smart_routing": {
    "description": "Automatic model selection (Ollama vs Claude)",
    "performance": "30-50% cost savings, 11.6s latency",
    "use_cases": ["code_generation", "architecture_planning"]
  },
  "task_classification": {
    "types": 8,
    "confidence_scoring": true,
    "fallback_logic": "comprehensive"
  },
  "quality_validation": {
    "languages": ["python", "javascript", "text"],
    "ast_parsing": true,
    "fallback_available": true
  },
  "mcp_integration": {
    "server": "localhost:8000/mcp",
    "transport": "SSE",
    "cursor_ide_ready": true
  }
}
```

**Capability Categories:**
- `core_features.json` - Main system capabilities
- `api_endpoints.json` - Available API functionality  
- `performance_metrics.json` - Benchmarks and limitations
- `integration_points.json` - How to integrate with external systems
- `roadmap_features.json` - Planned capabilities (with timelines)

### 7.2 External Projects Structure (data/knowledge/projects/)

**Project Categories:**

**Internal Projects (`internal/`):**
- Personal development projects
- Experimental features
- Learning/research projects
- Open source contributions

**Commercial Projects (`commercial/`):**
- Client work
- Revenue-generating projects  
- Professional services
- Consulting engagements

**Project Knowledge Template:**
```json
// projects/{category}/{project_name}/
├── project_config.json      # Basic project info
├── capabilities_used.json   # Which LLMGenie features
├── custom_prompts.json      # Project-specific prompts
├── integration_notes.md     # How LLMGenie is integrated
├── performance_data.json    # Project-specific metrics
└── lessons_learned.md       # What worked/didn't work
```

### 7.3 AI Context Loading for Projects

**Project-Aware AI Loading:**
```python
# When working on external project
1. Load standard LLMGenie capabilities
2. Load project-specific context:
   - data/knowledge/projects/{category}/{project}/
   - Project custom prompts and configurations
   - Previous lessons learned and best practices
3. Apply project-specific quality standards
4. Use project-appropriate model routing
```

**Benefits:**
- AI understands project-specific constraints
- Reuses successful patterns across projects
- Maintains quality standards per project type
- Enables revenue tracking and optimization

### 7.4 Commercial Project Considerations

**Revenue Protection:**
- Client-specific knowledge isolated in commercial/
- Access controls for sensitive project data
- Performance tracking for billing optimization
- Success metrics for client reporting

**Reusability:**
- Abstract successful patterns to templates/
- Build capability improvements back into core
- Maintain competitive advantages in capabilities/
- Scale learnings across commercial engagements

## 8. Links and References

**Implementation Plan:** @human:data/plans/phase_3a2_documentation_architecture_plan.md  
**Session Log:** @session:data/logs/sessions/session_docs_architecture_2025-01-05.jsonl  
**AI Workflow:** @ai:data/ai_workflow.json  
**Current Structure:** @human:docs/docs.json  
**AI Knowledge Base:** @ai:data/knowledge/README.md  

---

**Architecture Status:** ✅ Design Complete - Ready for Phase 3B Implementation 