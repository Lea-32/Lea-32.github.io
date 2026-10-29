---
layout: default
title: 探索
---
<section class="hero"><p class="hero-intro">Lea 的学习笔记</p><h1>保持好奇。<br><span>让理解，持续生长。</span></h1><p class="hero-description">从一篇论文，到一行代码。<br>记录深度阅读、系统学习与动手实践。</p><a class="primary-button rounded-full font-medium transition-all duration-300" href="#library">探索笔记 <span aria-hidden="true">↓</span></a></section>
<section class="library-section" id="library" aria-labelledby="library-title">
<div class="section-heading"><div><h2 id="library-title">每一次学习，都有迹可循。</h2><p>沿着兴趣，找到下一篇值得阅读的笔记。</p></div><a href="{{ '/categories/' | relative_url }}">浏览分类 →</a></div>
<nav class="category-filter" aria-label="按分类筛选笔记">
<a href="{{ '/' | relative_url }}#library" data-filter="all" aria-current="true">全部 <span>{{ site.notes | size }}</span></a>
{% for category in site.data.categories %}{% assign selected = site.notes | where: 'category', category.id %}
<a href="{{ '/categories/' | append: category.id | append: '/' | relative_url }}" data-filter="{{ category.id }}">{{ category.name }} <span>{{ selected | size }}</span></a>{% endfor %}
</nav>
<p class="results-status" id="filter-status" role="status">共 {{ site.notes | size }} 篇笔记</p>
<div class="article-grid" id="note-grid">{% assign notes = site.notes | sort: 'title' %}{% for note in notes %}{% include note-card.html note=note %}{% endfor %}</div>
<div class="empty-state" id="filter-empty" hidden><h3>新的探索，即将从这里开始。</h3><p>这个分类还没有笔记。先看看其他内容吧。</p><a href="{{ '/' | relative_url }}#library" data-reset-filter>查看全部笔记 →</a></div>
</section>

