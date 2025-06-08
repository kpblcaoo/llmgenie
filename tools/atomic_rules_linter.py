import os
import re
from glob import glob

RULES_DIR = '.cursor/rules'
SUPPORTED_FIELDS = {'description', 'globs', 'alwaysApply'}

# Сбор всех .mdc_ файлов
rule_files = [y for x in os.walk(RULES_DIR) for y in glob(os.path.join(x[0], '*.mdc_'))]

errors = []
roles_covered = set()
modes_covered = set()
all_links = set()
missing_links = set()

for path in rule_files:
    with open(path, encoding='utf-8') as f:
        lines = f.readlines()
    # Парсинг frontmatter
    fm = {}
    in_fm = False
    for line in lines:
        if line.strip() == '---':
            in_fm = not in_fm
            continue
        if in_fm:
            m = re.match(r'^(\w+):\s*(.*)', line)
            if m:
                key, val = m.group(1), m.group(2)
                if key in SUPPORTED_FIELDS:
                    fm[key] = val
    # Проверка frontmatter
    for field in SUPPORTED_FIELDS:
        if field not in fm:
            errors.append(f"{path}: missing field '{field}' in frontmatter")
    # Парсинг Meta
    meta = {}
    meta_start = False
    for line in lines:
        if line.strip() == '## Meta':
            meta_start = True
            continue
        if meta_start and line.startswith('#'):
            break
        if meta_start and line.strip().startswith('- '):
            m = re.match(r'- (\w+): (.*)', line.strip())
            if m:
                meta[m.group(1)] = m.group(2)
    # Coverage по ролям/режимам
    if 'role' in meta:
        roles_covered.add(meta['role'])
    if 'applies to' in meta:
        for mode in re.findall(r'\w+', meta['applies to']):
            modes_covered.add(mode)
    # Сбор @-ссылок
    for line in lines:
        for m in re.findall(r'@([\w\-/\.]+)', line):
            all_links.add(m)
            # Проверка существования файла/директории для ссылок на .md, .json, .mdc, .mdc_, .log
            if any(m.endswith(ext) for ext in ['.md', '.json', '.mdc', '.mdc_', '.log']):
                target = m
                if not os.path.exists(target) and not os.path.exists(os.path.join(RULES_DIR, target)):
                    missing_links.add(m)

# Генерация отчета
print('Atomic Rules Linter Report')
print('===========================')
if errors:
    print('\nFrontmatter errors:')
    for e in errors:
        print('  -', e)
else:
    print('Frontmatter: OK')
print('\nRoles covered:', ', '.join(sorted(roles_covered)))
print('Modes covered:', ', '.join(sorted(modes_covered)))
if missing_links:
    print('\nMissing @-links:')
    for l in sorted(missing_links):
        print('  -', l)
else:
    print('All @-links valid')
print('\nTotal rules checked:', len(rule_files)) 