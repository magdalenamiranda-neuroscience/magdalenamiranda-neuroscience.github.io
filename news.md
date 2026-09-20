---
layout: default
title: News
permalink: /news/
description: News from Magdalena Miranda.
---
<div class="container">
  <header class="page-head">
    <p class="kicker">News</p>
    <h1>News</h1>
  </header>
  {% for post in site.posts %}
  <article class="post-item">
    <p class="kicker">{{ post.date | date: "%-d %B %Y" }}</p>
    <h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
    <p>{{ post.excerpt | strip_html | strip }}</p>
  </article>
  {% endfor %}
</div>
