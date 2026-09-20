---
layout: default
title: Publications
permalink: /publications/
description: Peer-reviewed publications of Magdalena Miranda in cognitive neuroscience.
---
{% assign pubs = site.data.publications %}
<div class="container">
  <header class="page-head">
    <p class="kicker">Publications</p>
    <h1>Publications</h1>
    <p class="lead">{{ pubs.size }} publications, most recent first. Also listed on <a href="{{ site.data.links.orcid }}">ORCID</a>{% if site.data.links.scholar %} and <a href="{{ site.data.links.scholar }}">Google Scholar</a>{% endif %}.</p>
  </header>

  {% assign groups = pubs | group_by: "year" | sort: "name" | reverse %}
  {% for g in groups %}
  <section class="pubyear" aria-labelledby="y{{ g.name }}">
    <h2 id="y{{ g.name }}">{{ g.name }}</h2>
    <ol class="pubs">
      {% for p in g.items %}
      <li class="pub">
        <p class="pub__title">{{ p.title }}</p>
        <p class="pub__meta pub__authors">{% for a in p.authors %}{% if a.self %}<strong>{{ a.name }}</strong>{% else %}{{ a.name }}{% endif %}{% unless forloop.last %}, {% endunless %}{% endfor %}</p>
        <p class="pub__meta"><em>{{ p.journal }}</em>{% if p.volume != "" %} {{ p.volume }}{% endif %}{% if p.pages != "" %}, {{ p.pages }}{% endif %} · <a href="https://doi.org/{{ p.doi }}">doi:{{ p.doi }}</a></p>
        <p class="badges">
          {% if p.lead %}<span class="badge badge--lead">First / co-first author</span>{% endif %}
          {% if p.corresponding %}<span class="badge">Corresponding author</span>{% endif %}
          {% if p.type == "review" %}<span class="badge">Review</span>{% elsif p.type == "editorial" %}<span class="badge">Editorial</span>{% endif %}
          {% if p.oa %}<span class="badge">Open access</span>{% endif %}
        </p>
      </li>
      {% endfor %}
    </ol>
  </section>
  {% endfor %}
</div>
