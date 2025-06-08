# Аудит atomic rules - Эпик 3 (2025-01-05)

## 🎯 Цель аудита
Проверить соответствие между `@rules_manifest.json` и фактическим состоянием файлов в `.cursor/rules/`, выявить отсутствующие правила, некорректные @-references и fallback'и.

---

## ⚠️ КРИТИЧЕСКИЕ ПРОБЛЕМЫ

### 1. Отсутствующие правила в rules_manifest.json

#### **Core Rules (ОТСУТСТВУЮТ в manifest):**
- [ ] `009_branch_policy.mdc_` - Branch policy (atomic)
- [ ] `010_session_management.mdc_` - Session management (atomic) 
- [ ] `011_logging_and_retrospective.mdc_` - Logging & retrospective (atomic)
- [ ] `012_cli_commands.mdc_` - CLI commands reference and workflow
- [ ] `013_ai_capabilities.mdc_` - AI capabilities and automation
- [ ] `014_project_scope.mdc_` - Project data, symlink policy, and data requirements
- [ ] `015_workflow_modes.mdc_` - When workflow modes and context tags mentioned

#### **Roles Rules (ОТСУТСТВУЮТ в manifest):**
- [ ] `230_project_auditor.mdc` - НЕТ .mdc_ копии! Только .mdc
- [ ] **Sub-rules 220_rules_engineer/** (ВСЕ отсутствуют):
  - [ ] `2201_atomic_rule_structure.mdc_` 
  - [ ] `2202_references_and_crosslinks.mdc_`
  - [ ] `2203_static_analysis_and_validation.mdc_`
  - [ ] `2204_environment_portability.mdc_`
  - [ ] `2205_logging_and_education.mdc_`

---

## 🔍 ПРОБЛЕМЫ С @-REFERENCES

### **Проверка ссылок в текущих правилах manifest:**

#### ✅ КОРРЕКТНЫЕ:
- `001_logging_checkpoints`: `@session_log`, `@ai_workflow.json` - OK
- `005_context_restoration`: `@meta-log`, `@ai_workflow.json` - OK  
- `006_best_practices_recording`: `@docs/decision_memos/` - OK
- `007_decision_analysis`: `@docs/decision_memos/`, `@session_log` - OK

#### ⚠️ ТРЕБУЮТ ПРОВЕРКИ:
- `200_knowledge_engineer`: `@docs/ONBOARDING_LLMSTRUCT.md`, `@docs/BEST_PRACTICES_LLMSTRUCT.md` - **проверить существование**
- `210_reviewer`: `@docs/code_review_checklist.md` - **проверить существование**
- `100_code_review`: `@docs/code_review_checklist.md` - **проверить существование** 
- `400_audit`: `@docs/security_audit_checklist.md` - **проверить существование**
- `900_template_commit`: `@docs/commit_message_template.md` - **проверить существование**

---

## 🔧 ПРОБЛЕМЫ С FALLBACK

### **Отсутствующие fallback (должны быть у всех atomic rules):**
- `002_advice_objectivity` - fallback: null
- `003_language_policy` - fallback: null  
- `004_hypothesis_suggestion` - fallback: null
- `006_best_practices_recording` - fallback: null
- `007_decision_analysis` - fallback: null
- `008_mdc_work_protocol` - fallback: null

---

## 📁 СТРУКТУРНЫЕ ПРОБЛЕМЫ

### **Отсутствующие .mdc_ копии:**
- `roles/230_project_auditor.mdc` - НЕТ .mdc_ версии для работы

### **Дублирование файлов:**
- Все правила имеют и .mdc и .mdc_ версии - это корректно по protocol

---

## 🎯 ПЛАН ИСПРАВЛЕНИЯ

### **Приоритет 1 - Критичные пропуски:**
1. [ ] Добавить все отсутствующие правила в rules_manifest.json
2. [ ] Создать .mdc_ копию для 230_project_auditor.mdc
3. [ ] Проверить существование всех @-referenced файлов
4. [ ] Добавить fallback для всех atomic rules без fallback

### **Приоритет 2 - Стандартизация:**
1. [ ] Проверить соответствие описаний в manifest с фактическим содержимым правил
2. [ ] Валидировать cross-links между правилами
3. [ ] Обновить last_updated даты где необходимо

---

## 📊 СТАТИСТИКА

- **Правил в manifest:** 14
- **Фактических core правил:** 15 (+1 отсутствует)
- **Фактических role правил:** 3 основных + 5 sub-rules (+8 отсутствуют)
- **Общий gap:** ~57% правил отсутствуют в manifest

---

## 🚨 БЛОКЕРЫ ДЛЯ ЭПИКА 3

1. **Невозможно автоматизировать валидацию** без полного manifest
2. **@-references могут быть broken** без проверки файлов
3. **Handoff protocols неполные** без всех role правил
4. **MCP endpoint нельзя реализовать** с неполными данными

---

**Следующий шаг:** Начать исправление с добавления отсутствующих правил в manifest. 