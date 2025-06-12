# Decision Memo: Optimization of Cursor Rules, Roles, and Modes Integration

**Date:** 2024-06-XX
**Author:** AI Assistant (llmstruct)
**Context:** Project: llmgenie

---

## 1. Background & Motivation

Cursor's project rules system is powerful, but to maximize its effectiveness for LLM-driven workflows, we need:
- Clear, atomic rules with correct frontmatter (description, globs, alwaysApply)
- Logical linkage between rules, roles, and dialog modes ([meta], [debug], [knowledge], etc.)
- Automatic or semi-automatic invocation of relevant roles/rules based on user intent or mode
- Maintainability and auditability via manifest and @-references

## 2. Current Limitations
- Cursor does **not** natively support auto-invocation of rules by dialog mode (e.g., [meta], [debug])
- Only `description`, `globs`, `alwaysApply` are supported in frontmatter; extra fields are ignored
- @-references work for including files, but not for dynamic role activation
- Manual referencing of rules/roles is possible, but not always efficient
- Risk of rule bloat, duplication, or broken links if not managed systematically

## 3. Best Practices (2024)
- **Atomic rules**: Each rule covers one responsibility, is concise, and testable
- **Minimal frontmatter**: Only `description`, `globs`, `alwaysApply` in YAML frontmatter
- **@-references**: Use in body to link to roles, checklists, templates, or docs
- **Manifest tracking**: Maintain a manifest (rules_manifest.json) to map rules, roles, and their relationships
- **Workflow rules**: Create dedicated rules for key dialog modes (e.g., [knowledge], [meta][debug]) that include @-references to relevant roles
- **Regular audits**: Periodically review and prune rules for relevance and correctness

## 4. Proposed Workflow & Structure

### 4.1. Rule Structure
- All rules in `.cursor/rules/` with only required frontmatter fields
- Body may include:
  - Usage context ("Use when in [knowledge] mode...") - может ограничить. наоборот, при вызове [knowledge] нам надо сноску на релевантную роль .cursor/rules/roles/200_knowledge_engineer.mdc(внутри даже mdc_ все ссылки на mdc, мы же потом всё переименуем, когда закончим)
  - @-references to roles, docs, or templates

### 4.2. Role Integration
- Each role (e.g., knowledge_engineer, rules_engineer, reviewer) has its own .mdc rule file
- Atomic sub-rules for complex roles in subfolders (e.g., 220_rules_engineer/2201_atomic_rule_structure.mdc)
- Roles are referenced in workflow rules via @-links

### 4.3. Mode-Driven Workflow Rules
- For each key dialog mode (e.g., [knowledge], [meta][debug], [test]), create a workflow rule:
  - `description`: Use when in [mode] or performing [task]
  - `globs`: relevant files (or *)
  - Body: @-reference to the relevant role(s) and docs
- Example:
  ```markdown
  ---
  description: Use when discussing or updating project knowledge ([knowledge] mode).
  globs: docs/knowledge/**/*.md
  alwaysApply: false
  ---
  - When this rule is active, include @roles/200_knowledge_engineer.mdc for guidance.
  - Reference @docs/ONBOARDING_LLMSTRUCT.md for onboarding best practices.
  ```

### 4.4. Manifest & Audit
- Maintain `rules_manifest.json` with:
  - All rules, their globs, and @-references
  - Mapping of dialog modes to workflow rules and roles
  - Last audit date/status
- Use scripts or linters to check for broken @-links and unused rules

## 5. Rationale
- **Clarity**: Atomic, mode-driven rules make it clear when and why each rule/role is used
- **Maintainability**: Manifest and @-references ensure traceability and easy updates
- **Scalability**: New modes, roles, or workflows can be added without breaking existing structure
- **AI Efficiency**: Concise, relevant rules improve LLM context and reduce confusion

## 6. Risks & Mitigations
- **Risk**: Cursor may change rule format requirements
  - *Mitigation*: Regularly monitor Cursor updates and adjust rules accordingly
- **Risk**: Rule bloat or duplication
  - *Mitigation*: Enforce atomicity, regular audits, and manifest tracking
- **Risk**: Broken @-links
  - *Mitigation*: Automated link checking scripts
- **Risk**: Overcomplication
  - *Mitigation*: Keep rules as simple and focused as possible

## 7. Next Steps
1. Refactor all rules to minimal frontmatter and atomic structure
2. Create workflow rules for each key dialog mode, referencing relevant roles
3. Update/maintain rules_manifest.json with all relationships
4. Implement scripts for link checking and rule audits
5. Document this workflow in onboarding and best practices docs
6. Review and iterate after initial deployment

---

**Prepared by:** AI Assistant (llmstruct)
**For review by:** Project Lead, Knowledge Engineer, Rules Engineer 