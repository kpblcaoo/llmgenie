import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

fig, ax = plt.subplots(figsize=(12, 8))

# Блоки: (имя, x, y, цвет)
blocks = [
    ("src/llmgenie", 0.1, 0.8, '#e0e0e0'),   # 0
    ("src/rag_context", 0.1, 0.6, '#e0e0e0'), # 1
    ("src/struct_tools", 0.1, 0.4, '#e0e0e0'), # 2
    ("data/*", 0.4, 0.9, '#f5f5f5'),         # 3
    ("data/project_manifest.json", 0.4, 0.8, '#f5f5f5'), # 4
    ("struct.json", 0.4, 0.7, '#f5f5f5'),    # 5
    ("src/.llmstruct_index", 0.4, 0.6, '#f5f5f5'), # 6
    ("data/knowledge/*", 0.7, 0.9, '#d0f0c0'), # 7
    ("docs/knowledge/*", 0.7, 0.8, '#d0f0c0'), # 8
    ("docs/ONBOARDING_LLMSTRUCT.md", 0.7, 0.7, '#c0e0ff'), # 9
    ("docs/BEST_PRACTICES_LLMSTRUCT.md", 0.7, 0.6, '#c0e0ff'), # 10
    ("docs/WORKFLOW_LLMSTRUCT_EPIC_MANAGEMENT.md", 0.7, 0.5, '#c0e0ff'), # 11
    ("docs/security_audit_checklist.md", 0.7, 0.4, '#c0e0ff'), # 12
    ("docs/code_review_checklist.md", 0.7, 0.3, '#c0e0ff'), # 13
    (".cursor/rules/rules_manifest.json", 0.4, 0.4, '#ffe0c0'), # 14
    (".cursor/rules/core/*", 0.4, 0.3, '#ffe0c0'), # 15
    (".cursor/rules/workflows/*", 0.4, 0.2, '#ffe0c0'), # 16
    (".github/workflows/*", 0.1, 0.2, '#f0d0ff'), # 17
    ("scripts/*", 0.1, 0.1, '#f0d0ff'), # 18
    ("data/logs/sessions/*", 0.7, 0.1, '#f0f0a0'), # 19
    ("data/insights.json", 0.7, 0.2, '#f0f0a0'), # 20
]

for name, x, y, color in blocks:
    ax.add_patch(mpatches.FancyBboxPatch((x-0.07, y-0.03), 0.14, 0.06,
        boxstyle="round,pad=0.02", fc=color, ec="#333"))
    ax.text(x, y, name, ha='center', va='center', fontsize=10, fontweight='bold')

# Связи (все индексы должны быть в диапазоне 0..20)
arrows = [
    (3, 4), (4, 7), (4, 8), (4, 9), (4, 10), (4, 11), (4, 12), (4, 13),
    (5, 0), (5, 2), (5, 13),
    (14, 15), (14, 16), (14, 17), (14, 4), (14, 5), (14, 19), (14, 20),
    (0, 1), (0, 2), (0, 14), (0, 17), (0, 19),
    (1, 2), (1, 7),
    (2, 7), (2, 8), (2, 19),
]
for i, j in arrows:
    if 0 <= i < len(blocks) and 0 <= j < len(blocks):
        x0, y0 = blocks[i][1:3]
        x1, y1 = blocks[j][1:3]
        ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="->", lw=1.5, color="#666", alpha=0.7))

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')
plt.tight_layout()
plt.savefig('../project_structure.png', dpi=200) 