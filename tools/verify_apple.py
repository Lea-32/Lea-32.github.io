from pathlib import Path
import re, json, subprocess, tempfile
import yaml

root=Path(__file__).resolve().parents[1]
categories=yaml.safe_load((root/'_data/categories.yml').read_text(encoding='utf-8'))
allowed={c['id'] for c in categories}
for path in (root/'_notes').glob('*.md'):
    text=path.read_text(encoding='utf-8');data=yaml.safe_load(text.split('---',2)[1]);assert data['category'] in allowed
for category in categories:
    assert (root/'categories'/(category['id']+'.html')).exists()
for path in [root/'assets/site.js',root/'_layouts/default.html',root/'_layouts/note.html',root/'search.html']:
    text=path.read_text(encoding='utf-8')
    scripts=[text] if path.suffix=='.js' else re.findall(r'<script>(.*?)</script>',text,re.S)
    for script in scripts:
        script=re.sub(r'\{\{.*?\}\}','/search.json',script)
        subprocess.run(['node','--check'],input=script,text=True,check=True,capture_output=True)

# Exercise importing with source metadata, published metadata and a default category.
with tempfile.TemporaryDirectory() as directory:
    temp=Path(directory); vault=temp/'vault';out=temp/'out';vault.mkdir();out.mkdir()
    source=vault/'paper.md';source.write_text('---\ntitle: A Paper\ncategory: papers\ntags: [LLM]\n---\n## Method\nText',encoding='utf-8')
    subprocess.run(['python',str(root/'import_obsidian.py'),str(vault),'--output',str(out)],check=True,capture_output=True)
    path=out/'_notes/paper.md'; first=path.read_text(encoding='utf-8'); front=yaml.safe_load(first.split('---',2)[1]);assert front['category']=='papers' and front['tags']==['LLM']
    source.write_text('## Updated method\nNew text',encoding='utf-8')
    subprocess.run(['python',str(root/'import_obsidian.py'),str(vault),'--output',str(out)],check=True,capture_output=True)
    second=path.read_text(encoding='utf-8');assert yaml.safe_load(second.split('---',2)[1])['category']=='papers' and 'New text' in second
    source.write_text('---\ncategory: invalid\n---\nText',encoding='utf-8')
    result=subprocess.run(['python',str(root/'import_obsidian.py'),str(vault),'--output',str(out)],capture_output=True)
    assert result.returncode!=0

css=(root/'assets/apple.scss').read_text(encoding='utf-8')
assert 'gradient' not in css and 'prefers-reduced-motion' in css
print('PASS: taxonomy routes, note metadata, JavaScript syntax, source metadata, reimport preservation, invalid category rejection, style constraints')
