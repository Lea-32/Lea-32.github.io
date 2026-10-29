---
layout: page
title: 首页
---

<div class="intro">
<p class="eyebrow">LEARNING IN PUBLIC</p>
<h1>把学过的知识，变成自己的理解。</h1>
<p>这里是 Lea 的学习笔记本，收集学习记录、阅读心得与实践过程。</p>
<a href="{{ '/archive/' | relative_url }}">浏览全部笔记 →</a>
</div>

## 学习笔记

{% assign notes = site.notes | sort: 'title' %}
{% for note in notes %}
<div class="note-entry"><h3><a href="{{ note.url | relative_url }}">{{ note.title | escape }}</a></h3><p>阅读笔记 →</p></div>
{% endfor %}

