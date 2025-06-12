# Аудит архитектуры и кода (2025-06-12)

## 1. Инвентаризация src/

(см. src_inventory.txt)

## 2. Ключевые подпапки (llmgenie, rag_context, struct_tools)

(см. src_submodules_inventory.txt)

## 3. Архитектурные артефакты (struct.json, .llmstruct_index)

(см. struct_json_info.txt, llmstruct_index_info.txt)

## 4. Проблемы и пробелы:
- [ ] Проверить, все ли модули реально используются
- [ ] Найти и отметить "мертвый" код
- [ ] Сверить struct.json и .llmstruct_index с реальной структурой src/
- [ ] Проверить связи между кодом, документацией и правилами 