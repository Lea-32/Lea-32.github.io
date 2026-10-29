"""Export an Obsidian vault without modifying it. Requires Pillow and PyYAML."""
from pathlib import Path
import re, json, hashlib, argparse, html
import yaml
from PIL import Image

p = argparse.ArgumentParser()
p.add_argument('vault', type=Path)
p.add_argument('--output', type=Path, default=Path(__file__).parent)
a = p.parse_args()
root, out = a.vault.resolve(), a.output.resolve()
notes = sorted(f for f in root.rglob('*.md') if not any(s.startswith('.') for s in f.relative_to(root).parts))
assets = [f for f in root.rglob('*') if f.is_file() and not any(s.startswith('.') for s in f.relative_to(root).parts)]
slugs = {f: re.sub(r'[^a-z0-9]+', '-', f.stem.lower()).strip('-') or 'note-' + hashlib.sha256(f.relative_to(root).as_posix().encode()).hexdigest()[:10] for f in notes}
assert len(set(slugs.values())) == len(slugs), 'Duplicate slugs; choose unique note names.'
warnings, converted = [], []
(out / '_notes').mkdir(exist_ok=True)
(out / 'assets' / 'notes').mkdir(parents=True, exist_ok=True)

def resolve(target, source):
    exact = (source.parent / target).resolve()
    if exact in assets: return exact
    hits = [f for f in assets if f.name == Path(target).name or (not Path(target).suffix and f.stem == target)]
    return hits[0] if len(hits) == 1 else None

for source in notes:
    body = source.read_text(encoding='utf-8-sig')
    source_front = re.match(r'^---\r?\n(.*?)\r?\n---(?:\r?\n|$)', body, re.S)
    metadata = yaml.safe_load(source_front[1]) or {} if source_front else {}
    if not isinstance(metadata, dict):
        raise ValueError(f'{source.name}: front matter must be a mapping')
    existing_path = out / '_notes' / (slugs[source] + '.md')
    existing = {}
    if existing_path.exists():
        previous = re.match(r'^---\n(.*?)\n---', existing_path.read_text(encoding='utf-8'), re.S)
        if previous:
            existing = yaml.safe_load(previous[1]) or {}
    body = re.sub(r'^---\r?\n.*?\r?\n---\r?\n', '', body, count=1, flags=re.S)
    body = re.sub(r'(?m)^(!\[\[[^\]\n]+)\]\s*$', r'\1]]', body)
    def wiki(m):
        embedded, target, alias = m.group(1), m.group(2), m.group(3)
        path, _, anchor = target.partition('#')
        found = resolve(path, source)
        if not found:
            warnings.append({'note': source.name, 'missing': target})
            return '**[附件缺失：' + html.escape(target) + ']**' if embedded else html.escape(alias or target)
        if found in slugs:
            url = '/notes/' + slugs[found] + '/'
            if anchor: url += '#' + re.sub(r'\s+', '-', anchor.strip().lower())
            if embedded: warnings.append({'note':source.name, 'note_embed_as_link':target})
            return '[' + (alias or found.stem) + '](' + url + ')'
        dest = 'assets/notes/' + hashlib.sha256(found.relative_to(root).as_posix().encode()).hexdigest()[:16]
        if found.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp']:
            dest += '.webp'
            if not (out / dest).exists():
                with Image.open(found) as im:
                    im.thumbnail((1800, 1800))
                    im.save(out / dest, 'WEBP', quality=88, method=6)
        else:
            import shutil
            dest += found.suffix
            shutil.copy2(found, out / dest)
        label = found.stem
        if embedded and dest.endswith('.webp'):
            width = ' width="' + alias + '"' if alias and alias.isdigit() else ''
            return '<img src="/' + dest + '" alt="' + html.escape(label, quote=True) + '" loading="lazy"' + width + '>'
        return '[' + (alias or found.name) + '](/' + dest + ')'
    # Protect code fences from prose conversions; normalize Obsidian tab labels.
    parts = re.split(r'(```[^\n]*\n.*?\n```)', body, flags=re.S)
    for i, part in enumerate(parts):
        if i % 2:
            if part.startswith('```column-settings'):
                parts[i] = ''
                continue
            first, rest = part.split('\n', 1)
            lang = first[3:].split()[0] if first[3:].split() else ''
            label = re.search(r'tab:(.*)', first)
            parts[i] = ('**' + label.group(1).strip() + '**\n\n' if label else '') + '```' + lang + '\n' + rest
            continue
        part = re.sub(r'(!?)\[\[([^\]|]+)(?:\|([^\]]+))?\]\]', wiki, part)
        part = re.sub(r'(?m)^\s*--- (?:start-multi-column[^\n]*|column-break ---|end-multi-column)\s*$', '', part)
        part = re.sub(r'(?m)^(>\s*)\[!([^\]]+)\][+-]?\s*(.*)$', lambda m:m[1]+'**'+(m[3] or m[2])+'**', part)
        part = re.sub(r'==([^=\n]+)==', r'<mark>\1</mark>', part)
        parts[i] = re.sub(r'%%.*?%%', '', part, flags=re.S)
    body = ''.join(parts)
    title = str(metadata.get('title', existing.get('title', source.stem)))
    allowed = {'papers', 'stacks', 'algorithms', 'projects', 'notes'}
    category = metadata.get('category', existing.get('category', 'notes'))
    if category not in allowed:
        raise ValueError(f'{source.name}: category must be one of {sorted(allowed)}')
    front_data = {'layout': 'note', 'title': title, 'permalink': '/notes/' + slugs[source] + '/', 'category': category}
    for field in ['description', 'tags', 'date']:
        value = metadata.get(field, existing.get(field))
        if value is not None:
            front_data[field] = value
    if 'tags' in front_data and isinstance(front_data['tags'], str):
        front_data['tags'] = [front_data['tags']]
    front = '---\n' + yaml.safe_dump(front_data, allow_unicode=True, sort_keys=False) + '---\n'
    # Raw prevents code examples from being interpreted as Liquid template instructions.
    (out / '_notes' / (slugs[source]+'.md')).write_text(front + '{% raw %}\n' + body.replace('{% endraw %}', '{% endraw %}{{ "{% endraw %}" }}{% raw %}') + '\n{% endraw %}\n', encoding='utf-8')
    converted.append({'title':title, 'slug':slugs[source], 'source':source.relative_to(root).as_posix()})
(out / 'import-report.json').write_text(json.dumps({'notes':converted, 'warnings':warnings}, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'notes':len(notes), 'images':len(list((out/'assets/notes').glob('*'))), 'warnings':warnings}, ensure_ascii=False))
