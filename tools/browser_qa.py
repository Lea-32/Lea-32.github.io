from pathlib import Path
import subprocess, time, json, urllib.request, base64
import websocket

workspace=Path('E:/codex/Projects')
profile=workspace/'apple-qa-profile'
profile.mkdir(exist_ok=True)
browser=subprocess.Popen(['C:/Program Files/Google/Chrome/Application/chrome.exe','--headless','--disable-gpu','--no-first-run','--no-default-browser-check','--remote-debugging-port=0','--remote-allow-origins=*','--user-data-dir='+str(profile),'about:blank'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=subprocess.CREATE_NO_WINDOW)
ws=None
try:
    for _ in range(100):
        active=profile/'DevToolsActivePort'
        if active.exists(): break
        time.sleep(.1)
    port=active.read_text().splitlines()[0]
    pages=json.load(urllib.request.urlopen('http://127.0.0.1:'+port+'/json'))
    target=next(p for p in pages if p['type']=='page')
    ws=websocket.create_connection(target['webSocketDebuggerUrl'],timeout=30)
    seq=0
    def call(method,params=None):
        global seq
        seq+=1; ident=seq
        ws.send(json.dumps({'id':ident,'method':method,'params':params or {}}))
        while True:
            result=json.loads(ws.recv())
            if result.get('id')==ident:
                if 'error' in result: raise RuntimeError(result['error'])
                return result.get('result',{})
    def evaluate(js):
        result=call('Runtime.evaluate',{'expression':js,'returnByValue':True,'awaitPromise':True})
        if result.get('exceptionDetails'): raise RuntimeError(result['exceptionDetails'])
        return result['result'].get('value')
    def navigate(path,selector):
        call('Page.navigate',{'url':'https://lea-32.github.io'+path})
        for _ in range(100):
            try:
                if evaluate('document.readyState===\'complete\' && !!document.querySelector('+json.dumps(selector)+')'):return
            except Exception: pass
            time.sleep(.2)
        raise RuntimeError('Page did not load '+path)
    def screenshot(name):
        result=call('Page.captureScreenshot',{'format':'png','captureBeyondViewport':False})
        (workspace/name).write_bytes(base64.b64decode(result['data']))
    call('Page.enable');call('Runtime.enable')
    call('Emulation.setDeviceMetricsOverride',{'width':1440,'height':1200,'deviceScaleFactor':1,'mobile':False})
    navigate('/','.article-card')
    assert evaluate("document.querySelectorAll('.article-card').length") == 3
    assert evaluate('document.documentElement.scrollWidth<=innerWidth')
    screenshot('apple-desktop.png')
    evaluate("document.querySelector('[data-filter=papers]').click()")
    assert evaluate("!document.getElementById('filter-empty').hidden && [...document.querySelectorAll('.article-card')].every(c=>c.hidden)")
    evaluate("document.querySelector('[data-filter=stacks]').click()")
    assert evaluate("document.querySelectorAll('.article-card:not([hidden])').length") == 1
    call('Emulation.setDeviceMetricsOverride',{'width':390,'height':844,'deviceScaleFactor':1,'mobile':True})
    evaluate("document.querySelector('[data-filter=all]').click();window.scrollTo(0,0)")
    assert evaluate('document.documentElement.scrollWidth<=innerWidth')
    screenshot('apple-mobile.png')
    evaluate("document.getElementById('theme-toggle').click()")
    assert evaluate("document.documentElement.dataset.theme==='dark'")
    time.sleep(.6)
    screenshot('apple-mobile-dark.png')
    evaluate("document.getElementById('theme-toggle').click()")
    navigate('/categories/papers/','.empty-state')
    assert evaluate('document.documentElement.scrollWidth<=innerWidth')
    navigate('/search/?q=Transformer','#search-status')
    for _ in range(50):
        if evaluate("document.querySelectorAll('.search-result').length>0"):break
        time.sleep(.2)
    assert evaluate("document.getElementById('search-results').textContent.includes('CS336')")
    navigate('/notes/cs336/','#note-content')
    assert evaluate('document.documentElement.scrollWidth<=innerWidth')
    assert evaluate("document.querySelectorAll('#toc a').length>0")
    index=evaluate("fetch('/search.json').then(r=>r.json()).then(n=>n.map(x=>({title:x.title,category:x.category})))")
    assert len(index)==3 and all(n['category'] for n in index)
    print(json.dumps({'checks':'PASS: desktop/mobile overflow, card count, category filters, empty page, theme, live search, article TOC, search index','index':index},ensure_ascii=False))
finally:
    if ws:
        try: call('Browser.close')
        except Exception: pass
        ws.close()
    try:browser.wait(timeout=5)
    except subprocess.TimeoutExpired:browser.terminate()
