---
layout: default
title: 首页
---

<header class="feed-heading">
<p class="eyebrow">LEARNING IN PUBLIC</p>
<h1>学习与记录</h1>
<p>这里是 Lea 的学习笔记本，收集学习记录、阅读心得与实践过程。</p>
<a href="{{ '/archive/' | relative_url }}">浏览全部笔记 →</a>
</header>

<section class="note-feed" aria-label="学习笔记">

{% assign notes = site.notes | sort: 'title' %}
{% for note in notes %}
<article class="article-card"><a class="category-pill" href="{{ '/archive/' | relative_url }}">学习笔记</a><h2><a href="{{ note.url | relative_url }}">{{ note.title | escape }}</a></h2><p>{{ note.description | default: '用自己的语言梳理概念，记录问题与实践。' | escape }}</p><div class="card-meta"><span>Lea · 学习记录</span><a href="{{ note.url | relative_url }}">阅读全文 →</a></div></article>
{% endfor %}
</section>

