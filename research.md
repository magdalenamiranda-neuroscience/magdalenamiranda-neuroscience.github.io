---
layout: default
title: Research
permalink: /research/
description: Five connected lines of work on memory discrimination, from molecules to human cognition.
---
<section class="hero-research">
  <div class="hero-research__mesh" aria-hidden="true">{% include hero-mesh.svg %}</div>
  <div class="container">
    <p class="kicker">Research</p>
    <h1>From single molecules to whole-brain dynamics.</h1>
    <p>Five connected lines of work on how memory keeps similar experiences distinct, in rodents and humans, in health and ageing.</p>
    <a class="btn btn--white" href="{{ '/publications/' | relative_url }}">See publications</a>
  </div>
</section>

<div class="themes">
{% for t in site.data.research %}{% assign fig = site.data.figures[t.id] %}
  <section class="theme" id="{{ t.id }}">
    <div class="container theme__in">
      <div class="theme__text">
        <p class="kicker">{{ t.number }} · {{ t.species }}</p>
        <h2>{{ t.title }}</h2>
        <p>{{ t.text }}</p>
        <ul class="chips">{% for tag in t.tags %}<li>{{ tag }}</li>{% endfor %}</ul>
        <p class="keypapers"><strong>Key papers:</strong>
          {% for d in t.papers %}{% assign pub = site.data.publications | where: "doi", d | first %}<a href="https://doi.org/{{ d }}">{{ pub.journal }} {{ pub.year }}</a>{% unless forloop.last %} · {% endunless %}{% endfor %}
        </p>
      </div>
      <figure class="fig theme__fig">
        <img src="{{ fig.src | relative_url }}" alt="{{ fig.alt }}" loading="lazy">
        {% if fig.credit %}<figcaption>{{ fig.credit }}</figcaption>{% endif %}
      </figure>
    </div>
  </section>
{% endfor %}
</div>
