(() => {
  const toggle = document.getElementById('theme-toggle');
  const updateTheme = () => { const dark = document.documentElement.dataset.theme === 'dark'; toggle?.setAttribute('aria-pressed', String(dark)); toggle?.setAttribute('aria-label', dark ? '切换浅色模式' : '切换深色模式'); };
  updateTheme();
  toggle?.addEventListener('click', () => { document.documentElement.dataset.theme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark'; try { localStorage.setItem('lea-theme', document.documentElement.dataset.theme); } catch {} updateTheme(); });
  document.querySelectorAll('.main-nav a').forEach(link => { if (link.pathname === location.pathname) link.setAttribute('aria-current', 'page'); });
  const filters = [...document.querySelectorAll('[data-filter]')];
  const cards = [...document.querySelectorAll('#note-grid [data-category]')];
  if (!filters.length) return;
  const valid = new Set(filters.map(a => a.dataset.filter));
  function applyFilter(value) {
    const selected = valid.has(value) ? value : 'all';
    let count = 0;
    cards.forEach(card => { card.hidden = selected !== 'all' && card.dataset.category !== selected; if (!card.hidden) count++; });
    filters.forEach(link => { if (link.dataset.filter === selected) link.setAttribute('aria-current', 'true'); else link.removeAttribute('aria-current'); });
    document.getElementById('filter-empty').hidden = count > 0;
    document.getElementById('filter-status').textContent = '共 ' + count + ' 篇笔记';
  }
  function setFilter(value) { const url = new URL(location.href); if (value === 'all') url.searchParams.delete('category'); else url.searchParams.set('category', value); url.hash = 'library'; history.pushState(null, '', url); applyFilter(value); }
  filters.forEach(link => link.addEventListener('click', e => { if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return; e.preventDefault(); setFilter(link.dataset.filter); }));
  document.querySelector('[data-reset-filter]')?.addEventListener('click', e => { e.preventDefault(); setFilter('all'); });
  window.addEventListener('popstate', () => applyFilter(new URLSearchParams(location.search).get('category') || 'all'));
  applyFilter(new URLSearchParams(location.search).get('category') || 'all');
})();
