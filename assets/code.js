(() => {
  const content = document.getElementById('note-content');
  if (!content) return;
  let serial = 0;
  const isCode = node => node && (node.matches('pre') || node.matches('.highlighter-rouge, .highlight')) && !!node.querySelector('code');
  // Consecutive blocks only: repeated group names in different questions stay separate.
  content.querySelectorAll('.code-meta[data-group]').forEach(marker => {
    if (!content.contains(marker)) return;
    let current = marker;
    const entries = [];
    while (current?.matches('.code-meta') && current.dataset.group === marker.dataset.group) {
      const block = current.nextElementSibling;
      if (!isCode(block)) break;
      entries.push({marker: current, block, title: current.dataset.tab || '方法 ' + (entries.length + 1)});
      current = block.nextElementSibling;
    }
    if (!entries.length) return;
    const group = document.createElement('section'), list = document.createElement('div');
    group.className = 'code-tabs'; list.className = 'code-tab-list';
    list.setAttribute('role', 'tablist'); list.setAttribute('aria-label', marker.dataset.group + '：代码方法');
    group.append(list); marker.before(group);
    const buttons = [], panels = [];
    const activate = (index, focus = false) => {
      buttons.forEach((button, i) => { button.setAttribute('aria-selected', String(i === index)); button.tabIndex = i === index ? 0 : -1; panels[i].hidden = i !== index; });
      if (focus) buttons[index].focus();
    };
    entries.forEach((entry, i) => {
      const id = 'code-method-' + (++serial), button = document.createElement('button'), panel = document.createElement('div');
      button.type = 'button'; button.textContent = entry.title; button.id = id + '-tab'; button.setAttribute('role', 'tab'); button.setAttribute('aria-controls', id);
      panel.id = id; panel.className = 'code-panel'; panel.setAttribute('role', 'tabpanel'); panel.setAttribute('aria-labelledby', button.id);
      panel.tabIndex = 0; panel.append(entry.block); group.append(panel); entry.marker.remove(); list.append(button); buttons.push(button); panels.push(panel);
      button.addEventListener('click', () => activate(i));
      button.addEventListener('keydown', event => {
        let target;
        if (event.key === 'ArrowRight') target = (i + 1) % entries.length;
        if (event.key === 'ArrowLeft') target = (i - 1 + entries.length) % entries.length;
        if (event.key === 'Home') target = 0;
        if (event.key === 'End') target = entries.length - 1;
        if (target !== undefined) { event.preventDefault(); activate(target, true); }
      });
    });
    activate(0);
  });
  content.querySelectorAll('pre').forEach(pre => {
    const code = pre.querySelector('code'); if (!code) return;
    const wrapper = pre.closest('.highlighter-rouge') || pre.closest('.highlight') || pre;
    const shell = document.createElement('div'), bar = document.createElement('div'), label = document.createElement('span'), copy = document.createElement('button');
    shell.className = 'code-shell'; bar.className = 'code-toolbar';
    const language = (wrapper.className + ' ' + code.className).match(/language-([\w+-]+)/);
    label.textContent = language ? language[1] : '代码'; copy.type = 'button'; copy.textContent = '复制'; copy.setAttribute('aria-label', '复制代码');
    const announcement = document.createElement('span'); announcement.className = 'code-copy-status'; announcement.setAttribute('role', 'status');
    copy.addEventListener('click', async () => { try { await navigator.clipboard.writeText(code.textContent); copy.textContent = '已复制'; announcement.textContent = '代码已复制'; } catch { copy.textContent = '请手动选择复制'; announcement.textContent = '无法访问剪贴板，请选择代码后复制'; } setTimeout(() => { copy.textContent = '复制'; announcement.textContent = ''; }, 2200); });
    pre.tabIndex = 0; pre.setAttribute('aria-label', label.textContent + '代码，可横向滚动');
    wrapper.before(shell); shell.append(bar, wrapper); bar.append(label, copy, announcement);
  });
})();
