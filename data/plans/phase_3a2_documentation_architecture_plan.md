# Phase 3A.2: Documentation Architecture Design Plan

**Phase:** 3A.2  
**Duration:** 45-60 minutes  
**Model:** Claude 4 Sonnet  
**Started:** 2025-01-05  
**Session:** session_docs_architecture_2025-01-05  

## Objectives

Спроектировать и реализовать модульную архитектуру документации, используя результаты Phase 3A.1 и учитывая двойственную природу knowledge base (human vs AI).

## Context from Phase 3A.1

✅ **Completed:**
- Modular documentation structure implemented (docs/docs.json + docs/index/)
- AI Knowledge Base analyzed (data/knowledge/ with techs/, envs/, models/, templates/)
- File inventory and categorization done
- Quality assessment completed

## Key Design Constraints

### Dual Knowledge Architecture
1. **Human KB** (docs/): guides, tutorials, decision memos - markdown-based
2. **AI KB** (data/knowledge/): JSON structures, technical configs - machine-readable
3. **Bridge mechanisms**: synchronization and cross-referencing between both

### Technical Context from AI KB
- Smart AI Routing (Ollama vs Claude)
- MCP Server integration (localhost:8000/mcp)
- TaskRouter with 8 task types
- Performance: 11.6s latency, 30-50% cost savings
- Quality validation with AST parsing

## Design Tasks

### 1. Hierarchical Structure Design (15 min)
- Define clear taxonomy for documentation modules
- Establish naming conventions
- Plan directory structure evolution
- Document relationship patterns

### 2. Cross-Reference Standards (15 min)
- Design @-reference system for both human and AI KB
- Create linking patterns between docs/ and data/knowledge/
- Establish validation rules for references
- Plan automated link checking

### 3. Automation Tools Design (10 min)
- Auto-generation strategies for documentation
- Validation tools for consistency
- Update propagation mechanisms
- Integration with existing workflow (ai_workflow.json)

### 4. AI Integration Strategy (10 min)
- How AI should consume modular docs
- Template systems for AI-generated content
- Quality standards for AI contributions
- Human review workflows

## Deliverables

1. **docs/documentation_architecture_design.md** - comprehensive architecture specification
2. Updated cross-reference standards
3. Automation tool recommendations
4. Integration guidelines for AI workflow

## Success Criteria

- [ ] Clear hierarchical structure defined
- [ ] Cross-reference system designed
- [ ] Automation tools specified
- [ ] AI integration strategy documented
- [ ] Ready for Phase 3B implementation

## Links
- Session log: data/logs/sessions/session_docs_architecture_2025-01-05.jsonl
- Context: docs/project_workflow_strategy_june_2025_final.md
- AI KB: data/knowledge/README.md 