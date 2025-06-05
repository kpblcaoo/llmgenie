#!/bin/bash

# CLI команды для управления эпиком intelligent_cleanup_integration_2025

echo "=== Эпик: Интеграция систем автоочистки в llmgenie ==="
echo ""

echo "=== Просмотр задач эпика ==="
cat data/tasks.json | jq '.tasks[] | select(.epic == "intelligent_cleanup_integration_2025")'
echo ""

echo "=== Просмотр идей эпика ==="  
cat data/ideas.json | jq '.ideas[] | select(.epic == "intelligent_cleanup_integration_2025")'
echo ""

echo "=== Статистика эпика ==="
echo "Задач всего: $(cat data/tasks.json | jq '[.tasks[] | select(.epic == "intelligent_cleanup_integration_2025")] | length')"
echo "Задач high priority: $(cat data/tasks.json | jq '[.tasks[] | select(.epic == "intelligent_cleanup_integration_2025" and .priority == "high")] | length')"
echo "Общая оценка часов: $(cat data/tasks.json | jq '[.tasks[] | select(.epic == "intelligent_cleanup_integration_2025") | .estimated_hours // 0] | add')"
echo "Идей всего: $(cat data/ideas.json | jq '[.ideas[] | select(.epic == "intelligent_cleanup_integration_2025")] | length')"
echo ""

echo "=== Полезные команды ==="
echo "# Создание ветки для эпика:"
echo "git checkout -b feature/intelligent-cleanup-integration-2025"
echo ""
echo "# Просмотр документации эпика:"
echo "cat docs/epics/intelligent_cleanup_integration_2025.md"
echo ""
echo "# Просмотр найденных паттернов:"
echo "cat docs/archive_analysis/01_architecture_patterns/intelligent_cleanup_system_patterns.md"
echo ""
echo "# Начало работы над первой задачей:"
echo "git checkout feature/intelligent-cleanup-integration-2025"
echo "echo 'TSK-CLEANUP-001 started' >> data/sessions/cleanup_session_$(date +%Y_%m_%d).json" 