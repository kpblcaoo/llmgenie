import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(8, 6))

# Основные блоки
blocks = [
    ("project_map.md", (0.5, 0.9)),
    ("cleanup_roadmap.md", (0.2, 0.7)),
    ("audit_checklist.md", (0.8, 0.7)),
    ("workfiles/", (0.5, 0.4)),
]

# Связи (start_idx, end_idx)
arrows = [
    (0, 1), (0, 2), (0, 3),
    (1, 3), (2, 3)
]

for name, (x, y) in blocks:
    ax.add_patch(mpatches.FancyBboxPatch((x-0.08, y-0.04), 0.16, 0.08,
        boxstyle="round,pad=0.02", fc="#e0e0e0", ec="#333"))
    ax.text(x, y, name, ha='center', va='center', fontsize=12, fontweight='bold')

for start, end in arrows:
    x0, y0 = blocks[start][1]
    x1, y1 = blocks[end][1]
    ax.annotate('', xy=(x1, y1+0.04), xytext=(x0, y0-0.04),
                arrowprops=dict(arrowstyle="->", lw=2, color="#666"))

# Подпапка workfiles
ax.add_patch(mpatches.FancyBboxPatch((0.32, 0.18), 0.36, 0.12,
    boxstyle="round,pad=0.02", fc="#f5f5f5", ec="#888"))
ax.text(0.5, 0.24, "...все вспомогательные и промежуточные файлы...", ha='center', va='center', fontsize=10)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')
plt.tight_layout()
plt.savefig('../audit_structure.png', dpi=200) 