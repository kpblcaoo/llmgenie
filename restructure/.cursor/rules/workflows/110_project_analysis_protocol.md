---
description: "Project Analysis Protocol - Based on real llmgenie analysis experience"
alwaysApply: false
---

# Project Analysis Protocol

## Meta
Based on successful llmgenie project analysis (Jan 2025)
Combines model switching strategy with incremental verification

## Core Principles

### 1. Reality-First Approach
- ❌ Don't assume code works until tested
- ✅ Test basic imports and instantiation first
- ✅ Separate environment issues from code issues
- ✅ Question documentation claims vs actual functionality

### 2. Model Selection Strategy
- **Gemini 2.5 Flash**: Large files (>10KB), comprehensive analysis, free 1M context
- **Claude 4 Sonnet**: Complex logic analysis, integration patterns, smaller files
- **Manual Checkpoints**: Stop for model switching, validate results
- **Incremental Handoffs**: Document findings for next model/phase

### 3. Phase Structure
```
Phase 1: Reconnaissance (proven detailed)
├── 1A: Large file analysis (Gemini)
├── 1B: Architecture mapping (Claude) 
└── 1C: Deep code analysis (Mixed models)

Phase 2+: Develop iteratively based on Phase 1 results
- Don't over-plan theoretical phases
- Build next phase prompts based on actual findings
- Test hypotheses before complex implementation
```

## Practical Workflow

### Before Analysis:
1. Environment check: `source venv/bin/activate`
2. Basic imports test: `python -c "import main_module"`
3. File structure mapping: Know where critical files are

### During Analysis:
1. **Large files** → Gemini 2.5 Flash with detailed analysis
2. **Small files** → Claude 4 Sonnet for logic patterns  
3. **Manual checkpoints** between model switches
4. **Document findings** immediately, don't rely on memory

### After Analysis:
1. **Test key components** individually
2. **Create practical file map** for next steps
3. **Honest assessment** of what works vs what's theoretical
4. **Build next phase** based on real results, not plans

## File Organization

### Generated Documentation:
```
docs/
├── {component}_analysis_phase_1c.md (detailed analysis)
├── cleanup_ready_assessment.md (practical status)
└── session_protocol_lessons.md (what we learned)
```

### Session Logging:
```
data/logs/sessions/
└── session_{type}_{date}_{topic}.jsonl
```

## Anti-Patterns to Avoid

- ❌ Over-detailed planning of untested phases
- ❌ Assuming complex architectures work without verification  
- ❌ Creating theoretical documentation before practical testing
- ❌ Model switching without validation checkpoints
- ❌ Proceeding with broken foundational components

## Success Metrics

- ✅ Basic environment and imports working
- ✅ Key components tested individually
- ✅ Clear file location map for next steps
- ✅ Honest assessment of working vs theoretical
- ✅ Protocol recorded for future replication

## Integration with Cleanup Process

This analysis protocol prepares for cleanup by:
1. Identifying what actually works (keep/enhance)
2. Mapping file locations (know what to clean)
3. Separating working from broken components
4. Building confidence through incremental verification
5. Creating practical action plans, not theoretical ones

---

**Status**: Proven effective in llmgenie analysis  
**Usage**: For any complex project analysis requiring model coordination 