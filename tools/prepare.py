from pathlib import Path
import json, re, html
import mistune
root = Path(__file__).resolve().parents[1]
preview = root / 'preview'
preview.mkdir(exist_ok=True)
css = (root/'assets/main.scss').read_text(encoding='utf-8').split('@import "minima";')[1]
css += '\n*{box-sizing:border-box}body{margin:0}main,header,footer{max-width:800px;margin:auto;padding:24px}nav{display:flex;gap:24px;flex-wrap:wrap}h1,h2,h3{line-height:1.5}h1{font-size:32px}p{margin:0 0 18px}a{text-decoration:none}pre{overflow:auto;border:1px solid #deddd2;border-radius:6px}code{font-size:14px}table{border-collapse:collapse}td,th{padding:10px;border:1px solid #deddd2}img{max-width:100%;height:auto}blockquote{border-left:3px solid #64816c;margin:20px 0;padding:16px;background:#f2eee4}footer{border-top:1px solid #deddd2;color:#6b756b}details{margin-bottom:24px}'
renderer = mistune.create_markdown(escape=False, plugins=['table','strikethrough','url'])
report = json.loads((root/'import-report.json').read_text(encoding='utf-8'))
notes = report['notes']
links = '<nav><a href="index.html">Lea 的学习笔记</a><a href="index.html#notes">全部笔记</a><a href="about.html">关于</a></nav>'
mathscript = "<script>window.MathJax={tex:{inlineMath:[['$','$']],displayMath:[['$$','$$']]},options:{skipHtmlTags:['script','style','pre','code']}};</script><script defer src='https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-chtml.js'></script>"
def page(title, body):
    return '<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>'+html.escape(title)+'</title><style>'+css+'</style><header>'+links+'</header><main>'+body+'</main><footer>Lea · 记录学习，整理思考，分享实践。<p>设计预览 · 公式依赖网络加载</p></footer>'+mathscript+'</html>'
for note in notes:
    text = (root/'_notes'/(note['slug']+'.md')).read_text(encoding='utf-8')
    body = text.split('---',2)[2].replace('{% raw %}', '').replace('{% endraw %}', '')
    assert '![[ ' not in body
    body = body.replace('src="/assets/', 'src="../assets/')
    for target in notes: body = body.replace('/notes/'+target['slug']+'/',target['slug']+'.html')
    # Preserve TeX before Markdown consumes backslashes, underscores and stars.
    maths=[]
    def protect(m): maths.append(m[0]); return 'MATHPLACEHOLDER'+str(len(maths)-1)+'END'
    parts=re.split(r'(```[^\n]*\n.*?\n```)', body, flags=re.S)
    for i in range(0,len(parts),2): parts[i]=re.sub(r'\$\$.*?\$\$|(?<!\$)\$(?!\$)[^\n$]+\$', protect, parts[i], flags=re.S)
    rendered=renderer(''.join(parts))
    for i, math in enumerate(maths): rendered=rendered.replace('MATHPLACEHOLDER'+str(i)+'END',html.escape(math))
    toc=[]
    def heading(m):
        ident='section-'+str(len(toc)); toc.append('<a href="#'+ident+'">'+re.sub('<[^>]+>','',m[2])+'</a><br>');return '<h'+m[1]+' id="'+ident+'">'+m[2]+'</h'+m[1]+'>'
    rendered=re.sub(r'<h([123])>(.*?)</h\1>',heading,rendered)
    (preview/(note['slug']+'.html')).write_text(page(note['title'],'<h1>'+html.escape(note['title'])+'</h1><details class="note-toc"><summary>本篇目录</summary>'+''.join(toc)+'</details><article class="post-content">'+rendered+'</article>'),encoding='utf-8')
entries=''.join('<div class="note-entry"><h2><a href="'+n['slug']+'.html">'+html.escape(n['title'])+'</a></h2><p>学习笔记 · 阅读全文 →</p></div>' for n in notes)
(preview/'index.html').write_text(page('Lea 的学习笔记','<div class="intro"><p class="eyebrow">LEARNING IN PUBLIC</p><h1>把学过的知识，<br>变成自己的理解。</h1><p>学习记录、阅读心得与实践过程。</p></div><h2 id="notes">学习笔记</h2>'+entries),encoding='utf-8')
(preview/'about.html').write_text(page('关于','<h1>关于</h1><p>你好，我是 Lea。这里记录我的学习笔记、实践过程和阅读心得。</p><a href="https://github.com/Lea-32">在 GitHub 找到我 →</a>'),encoding='utf-8')
for f in (root/'_notes').glob('*.md'):
    text=f.read_text(encoding='utf-8')
    assert not re.search(r'!?\[\[',text), f
    for asset in re.findall(r'src="/([^"]+)"',text): assert (root/asset).is_file(), asset
    assert text.count('```')%2 == 0, f
files=[]
for f in root.rglob('*'):
    if not f.is_file() or 'preview' in f.relative_to(root).parts: continue
    if f.suffix == '.webp': continue
    files.append({'path': f.relative_to(root).as_posix(), 'mode':'100644','type':'blob','content':f.read_text(encoding='utf-8')})
(root.parent/'blog-upload-text.json').write_text(json.dumps(files,ensure_ascii=False),encoding='utf-8')
(root.parent/'blog-upload-images.json').write_text(json.dumps([str(f) for f in (root/'assets/notes').glob('*.webp')]),encoding='utf-8')
print(json.dumps({'notes':len(notes),'images':len(list((root/'assets/notes').glob('*.webp'))),'text_files':len(files),'max_image_bytes':max(f.stat().st_size for f in (root/'assets/notes').glob('*.webp')),'checks':'image references and code fences passed'},ensure_ascii=False))
