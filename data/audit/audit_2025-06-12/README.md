# Аудит llmgenie (2025-06-12)

## Итоговые файлы
- **project_map.md** — карта и структура проекта
- **cleanup_roadmap.md** — дорожная карта по улучшениям
- **audit_checklist.md** — мастер-чеклист аудита

Вся вспомогательная и промежуточная информация: `workfiles/`

---

## Визуализация структуры проекта

### Mermaid-диаграмма (вся архитектура llmgenie)
```mermaid
graph TD
  subgraph "Кодовая база"
    SRC["src/"]
    LLMGENIE["src/llmgenie"]
    RAG["src/rag_context"]
    STRUCT["src/struct_tools"]
    SRC --> LLMGENIE
    SRC --> RAG
    SRC --> STRUCT
  end
  subgraph "Данные и манифесты"
    DATA["data/*"]
    TASKS["data/tasks.json"]
    IDEAS["data/ideas.json"]
    INSIGHTS["data/insights.json"]
    PRS["data/prs.json"]
    MANIFEST["data/project_manifest.json"]
    STRUCTJSON["struct.json"]
    LLMSINDEX["src/.llmstruct_index"]
    DATA --> TASKS
    DATA --> IDEAS
    DATA --> INSIGHTS
    DATA --> PRS
    DATA --> MANIFEST
    DATA --> STRUCTJSON
    DATA --> LLMSINDEX
  end
  subgraph "Базы знаний"
    AIKB["data/knowledge/*"]
    HUMANKB["docs/knowledge/*"]
  end
  subgraph "Документация"
    ONBOARD["docs/ONBOARDING_LLMSTRUCT.md"]
    BEST["docs/BEST_PRACTICES_LLMSTRUCT.md"]
    WORKFLOW["docs/WORKFLOW_LLMSTRUCT_EPIC_MANAGEMENT.md"]
    SECCHK["docs/security_audit_checklist.md"]
    CODECHK["docs/code_review_checklist.md"]
  end
  subgraph "Правила и enforcement"
    RULES[".cursor/rules/rules_manifest.json"]
    CORE[".cursor/rules/core/*"]
    WF[".cursor/rules/workflows/*"]
  end
  subgraph "Автоматизация и CI/CD"
    GHWF[".github/workflows/*"]
    SCRIPTS["scripts/*"]
  end
  subgraph "Логирование и мониторинг"
    LOGS["data/logs/sessions/*"]
    RETRO["data/insights.json"]
  end
  MANIFEST <--> DATA
  MANIFEST <--> AIKB
  MANIFEST <--> HUMANKB
  MANIFEST <--> ONBOARD
  MANIFEST <--> BEST
  MANIFEST <--> WORKFLOW
  MANIFEST <--> SECCHK
  MANIFEST <--> CODECHK
  STRUCTJSON <--> SRC
  STRUCTJSON <--> STRUCT
  STRUCTJSON <--> CODECHK
  RULES <--> CORE
  RULES <--> WF
  RULES <--> GHWF
  RULES <--> SCRIPTS
  RULES <--> MANIFEST
  RULES <--> STRUCTJSON
  RULES <--> LOGS
  RULES <--> RETRO
  GHWF <--> SCRIPTS
  LLMGENIE <--> RAG
  LLMGENIE <--> STRUCT
  LLMGENIE <--> AIKB
  LLMGENIE <--> HUMANKB
  LLMGENIE <--> RULES
  LLMGENIE <--> GHWF
  LLMGENIE <--> LOGS
  RAG <--> STRUCT
  RAG <--> AIKB
  STRUCT <--> AIKB
  STRUCT <--> HUMANKB
  STRUCT <--> LOGS
```

> Диаграмма выше отражает основные связи между кодом, данными, знаниями, документацией, правилами, автоматизацией и логированием в проекте llmgenie.

### PNG-диаграмма структуры проекта
![Структура проекта](project_structure.png)

---

## Структура итоговых файлов аудита (PNG)

![Структура аудита](audit_structure.png) 