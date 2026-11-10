from pathlib import Path
import re, html
root=Path(__file__).resolve().parents[1]
source=Path('E:/Agent-Learning/Agent-Learning/Hot100.md').read_text(encoding='utf-8-sig')
path=root/'_notes/hot100.md';published=path.read_text(encoding='utf-8');count=0
for match in re.finditer(r'```([^\n]*)\n(.*?)\n```',source,re.S):
    first,code=match.groups();group=re.search(r'\bgroup:([^\s]+)',first);tab=re.search(r'\btab:(.*)',first)
    if not group or not tab:continue
    language=first.split()[0]
    old='**'+tab[1].strip()+'**\n\n```'+language+'\n'+code+'\n```'
    marker='<span class="code-meta" data-group="'+html.escape(group[1],quote=True)+'" data-tab="'+html.escape(tab[1].strip(),quote=True)+'" hidden></span>'
    new=marker+'\n\n```'+language+'\n'+code+'\n```'
    if old in published:published=published.replace(old,new,1);count+=1
path.write_text(published,encoding='utf-8')
assert count>0 or 'class="code-meta"' in published
print('Migrated code methods:',count)
