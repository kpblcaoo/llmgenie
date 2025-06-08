import sys
sys.path.append('src')
from llmgenie.api.handoff_validator import HandoffValidator, HandoffPackage, HandoffFile

# Validate current Epic 4 handoff package
epic4_package = HandoffPackage(
    from_role='coder',
    to_role='reviewer',
    epic_id='epic4',
    files=[
        HandoffFile(path='docs/memos/epic4/epic4_requirements_and_lessons.md', type='summary', priority=1),
        HandoffFile(path='docs/memos/epic4/epic4_lessons_learned.md', type='lessons', priority=2),
        HandoffFile(path='docs/memos/epic4/epic4_checklist.md', type='checklist', priority=3),
        HandoffFile(path='src/llmgenie/api/handoff_validator.py', type='audit', priority=4),
        HandoffFile(path='src/llmgenie/api/main.py', type='audit', priority=5),
        HandoffFile(path='project_state.json', type='metadata', priority=6)
    ],
    startup_prompt='Resume Epic 4: MCP/CLI enforcement & handoff validation. Status: MCP integration completed, CI/CD integration in progress. Infrastructure: FastAPI + MCP working, tests passing. Lessons: Cursor supports MCP natively, fastapi-mcp simplifies integration. Next: complete CI/CD integration, documentation, validation on real packages.',
    control_questions=[
        'What is the current Epic 4 completion status?',
        'Are MCP endpoints working and tested?', 
        'What remaining tasks need completion?'
    ],
    success_criteria=[
        'MCP integration working in Cursor',
        'CI/CD validates handoff packages automatically',
        'All Epic 4 checklist items completed'
    ]
)

validator = HandoffValidator('.')
result = validator.validate_package(epic4_package)

print('=== Epic 4 Handoff Validation Report ===')
print(f'Overall validation: {"✅ PASS" if result.is_valid else "❌ FAIL"}')
print(f'Completeness score: {result.completeness_score:.2f}/1.0')
print(f'Files validation: {result.file_validation}')
print(f'Missing file types: {result.missing_files}')
print(f'Warnings: {result.warnings}')
print(f'Recommendations: {result.recommendations}')

if result.completeness_score < 0.8:
    print('⚠️  Handoff package completeness below 80% - consider improving before handoff')
else:
    print('✅ Handoff package meets quality standards') 