# 🏗️ Struct Tools - Powerful Project Structure Analysis

Dedicated toolset for comprehensive project structural analysis using `struct.json` and modular index from `llmstruct`.

## 🎯 Purpose

**struct_tools** provides specialized functionality for:
- **Architecture analysis** - understanding module relationships and dependencies
- **Complexity assessment** - quantifying code complexity for refactoring decisions  
- **Impact analysis** - evaluating refactoring risks and affected components
- **Call graph exploration** - tracing function calls and dependencies
- **Automated reporting** - generating comprehensive architecture documentation

## 🚀 Quick Start

### Installation
```bash
# Ensure llmstruct is available
pip install -r requirements.txt

# Make CLI executable
chmod +x scripts/struct-tools
```

### Basic Usage
```bash
# Generate project structure analysis
./scripts/struct-tools generate src

# Get project overview
./scripts/struct-tools overview

# Analyze specific module
./scripts/struct-tools module src/llmgenie/task_router.py --complexity --impact

# Search for functions
./scripts/struct-tools search "router"

# Find function callers
./scripts/struct-tools callers TaskClassifier

# Generate architecture report
./scripts/struct-tools report -o architecture_analysis.md
```

## 📋 Available Commands

### `generate` - Create Structure Analysis
```bash
./scripts/struct-tools generate [directory] [options]

Options:
  --force, -f          Force regeneration even if files are fresh
  --exclude-dir DIR    Exclude directories from analysis
```

### `overview` - Project Statistics
```bash
./scripts/struct-tools overview
```
Shows: modules count, functions, classes, call edges, dependencies, modular index status.

### `module` - Module Analysis
```bash
./scripts/struct-tools module <module_path> [options]

Options:
  --dependencies, -d   Show module dependencies and imports
  --complexity, -c     Show complexity metrics and code statistics
  --impact, -i         Show refactoring impact analysis
```

### `search` - Function Search
```bash
./scripts/struct-tools search <pattern>
```
Find functions by name pattern across the entire project.

### `callers` - Call Graph Analysis
```bash
./scripts/struct-tools callers <function_name> [options]

Options:
  --module MODULE      Limit search to specific module
```

### `report` - Architecture Documentation
```bash
./scripts/struct-tools report [options]

Options:
  --output, -o FILE    Output file path (default: architecture_report.md)
```

## 🔧 Cursor IDE Integration (MCP)

struct_tools provides 6 specialized MCP tools for Cursor IDE:

- `@struct_generate` - Generate structure analysis
- `@struct_overview` - Quick project statistics  
- `@struct_analyze_module` - Deep module analysis
- `@struct_search_functions` - Find functions by pattern
- `@struct_find_callers` - Call graph exploration
- `@struct_generate_report` - Comprehensive documentation

### Usage in Cursor
```
@struct_overview
@struct_generate src --force
@struct_analyze_module src/llmgenie/task_router.py
@struct_search_functions "classifier"
@struct_find_callers TaskClassifier
@struct_generate_report architecture_review.md
```

## 📊 Understanding Output

### Complexity Metrics
- **Functions/Classes Count** - Quantitative measures
- **Code Lines** - Total lines of actual code
- **Average/Max Lengths** - Function and class size metrics
- **Complexity Score** - Composite metric (functions×1 + classes×3 + params×0.5 + methods×1.5)

### Risk Assessment
- **LOW** - No external dependencies (safe to refactor)
- **MEDIUM** - Few dependencies (coordinate changes)
- **HIGH** - Multiple dependencies (comprehensive testing required)
- **CRITICAL** - Heavily used (architectural review mandatory)

### Complexity Score Guidelines
- **0-10:** Simple module (low risk)
- **11-30:** Medium complexity (standard review)
- **31-50:** High complexity (detailed analysis required)
- **51+:** Critical complexity (architectural review mandatory)

## 🎯 When to Use

### ✅ High Value Scenarios
- **Epic/task planning** - Understanding scope and dependencies
- **Refactoring preparation** - Assessing impact and risks
- **Architecture reviews** - Comprehensive structural analysis
- **Code reviews** - Validating changes don't break patterns
- **Knowledge transfer** - Documenting system structure
- **Onboarding** - Understanding project architecture

### ❌ Avoid for
- **Daily development** - Routine bug fixes, simple features
- **CI/CD pipelines** - Performance overhead in automation
- **Test writing** - Usually not architecture-dependent
- **Documentation updates** - Non-structural changes

## 🔄 Integration with Existing Tools

### Complementary to RAG System
- **RAG** - Rules retrieval, context enhancement, daily development
- **struct_tools** - Architecture analysis, refactoring planning, complexity assessment
- **Together** - Complete development intelligence system

### Workflow Integration
1. **Pre-epic:** Generate baseline structure + report
2. **Active development:** Analyze modules before major changes
3. **Pre-commit:** Check impact of changes
4. **Pre-merge:** Validate architectural consistency
5. **Post-epic:** Document structural insights

## 📁 Files and Structure

### Generated Files
- `struct.json` - Complete project structure (193KB for llmgenie)
- `src/.llmstruct_index/` - Modular per-file analysis
- `architecture_report.md` - Human-readable analysis report

### File Management
- **Different projects:** Use separate struct.json files
- **Version control:** Consider adding struct.json to .gitignore (dynamic)
- **Archival:** Save snapshots for major milestones
- **Reports:** Keep versioned reports for historical reference

## 🚨 Best Practices

### Performance
- **Incremental analysis:** Only regenerate when needed (1+ hour cache)
- **Targeted analysis:** Use modular index for specific modules
- **Exclude patterns:** Skip tests/, __pycache__, venv/ directories
- **Parallel workflows:** Run alongside other tools

### Quality Gates
- Generate fresh analysis before major architectural work
- Compare struct.json diffs to understand change impact
- Document architectural insights and decisions
- Use complexity metrics to guide refactoring priorities

## 🔗 Related Documentation

- `docs/struct_json_strategy.md` - Philosophy and usage strategy
- `.cursor/rules/tools/001_struct_tools_best_practices.mdc` - Detailed best practices
- `MCP_OPTIMIZATION_REPORT.md` - Integration with MCP system

## 💡 Examples

### Epic Planning Workflow
```bash
# 1. Generate baseline
./scripts/struct-tools generate src --force

# 2. Get overview
./scripts/struct-tools overview

# 3. Analyze key modules
./scripts/struct-tools module src/llmgenie/task_router.py --complexity --impact

# 4. Generate planning report
./scripts/struct-tools report -o epic_planning_baseline.md
```

### Refactoring Analysis
```bash
# 1. Analyze target module
./scripts/struct-tools module src/target/module.py --all

# 2. Find all callers
./scripts/struct-tools callers TargetFunction

# 3. Search for related functions
./scripts/struct-tools search "target"

# 4. Generate impact report
./scripts/struct-tools report -o refactoring_impact_analysis.md
```

---

**struct_tools** - Making project architecture visible, understandable, and actionable. 🚀 