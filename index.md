---
layout: default
title: Home
body_class: home
description: Magdalena Miranda is a cognitive neuroscientist studying how memory keeps similar experiences distinct.
---
{% assign pubs = site.data.publications %}
{% assign originals = pubs | where: "type", "article" %}
{% assign leads = pubs | where: "lead", true %}
<section class="hero-home">
  <div class="container hero-home__in">
    <div>
      <p class="kicker">Cognitive neuroscience</p>
      <h1>Memory, and how the brain keeps similar things apart.</h1>
      <p class="lead">I'm Magdalena Miranda, a cognitive neuroscientist. Across rodents and humans (molecules, neural circuits, EEG and behaviour) I study memory discrimination and how it changes with age.</p>
      <p class="status">Incoming Assistant Researcher (<i lang="es">Investigadora Asistente</i>), CONICET — Argentina</p>
      <p class="actions">
        <a class="btn btn--solid" href="{{ '/research/' | relative_url }}">Explore the research</a>
        <a class="btn btn--ghost" href="{{ '/about/' | relative_url }}">About me</a>
      </p>
    </div>
    <figure class="portrait"><img src="{{ '/assets/img/portrait.webp' | relative_url }}" alt="Portrait of Magdalena Miranda"></figure>
  </div>
</section>

<div class="facts-band">
  <div class="container">
    <ul class="facts">
      <li><strong>{{ pubs.size }}</strong><span>publications · {{ originals.size }} original articles, {{ leads.size }} as first or co-first author</span></li>
      <li><strong>HFSP</strong><span>and Fyssen Foundation fellowships</span></li>
      <li><strong>CONICET</strong><span>incoming assistant researcher, Argentina</span></li>
      <li><strong>10+ years</strong><span>of research across Argentina and France</span></li>
    </ul>
  </div>
</div>

<section class="section">
  <div class="container">
    <h2 class="section__title">What I work on</h2>
    <div class="cards">
      {% for t in site.data.research limit:3 %}{% assign fig = site.data.figures[t.id] %}
      <article class="card">
        <img class="card__img{% if fig.fit == 'contain' %} card__img--contain{% endif %}" src="{{ fig.src | relative_url }}" alt="{{ fig.alt }}" loading="lazy">
        <div class="card__body">
          <h3><a href="{{ '/research/' | relative_url }}#{{ t.id }}">{{ t.title }}</a></h3>
          <p>{{ t.summary }}</p>
        </div>
        {% if fig.credit %}<small class="card__credit">{{ fig.credit }}</small>{% endif %}
      </article>
      {% endfor %}
    </div>
  </div>
</section>

<section class="band">
  <div class="container">
    <p class="kicker">Research</p>
    <p class="big">From single molecules to whole-brain dynamics: five connected lines of work.</p>
    <a class="btn btn--white" href="{{ '/research/' | relative_url }}">All research</a>
  </div>
</section>

{% assign latest = site.posts | first %}
{% if latest %}
<div class="container">
  <div class="newsblock">
    <div>
      <p class="kicker">Latest news</p>
      <h3>{{ latest.title }}</h3>
      <p>{{ latest.excerpt | strip_html | strip | truncatewords: 28 }}</p>
    </div>
    <a class="btn btn--ghost" href="{{ latest.url | relative_url }}">Read more</a>
  </div>
</div>
{% endif %}
