---
layout: page
title: Topic Index
permalink: /health-papers/topics/
comments: false
exclude_from_papers: true
---

An A–Z index of terms, symptoms, and common names covered across the health
papers — useful when you don't know the "official" name for what you're
looking for. Click a term to see its paper(s).

[← All health papers]({{ "/health-papers/" | relative_url }})

{% assign topics = site.data.topics %}
{% assign grouped = topics | group_by_exp: "t", "t.term | slice: 0, 1 | upcase" %}

<nav id="hp-topics-jump" style="margin:1em 0;font-size:0.9em;">
{% for group in grouped %}<a href="#letter-{{ group.name | slugify }}" style="margin-right:0.6em;">{{ group.name }}</a>{% endfor %}
</nav>

<div id="hp-topics-list">
{% for group in grouped %}
<h3 id="letter-{{ group.name | slugify }}">{{ group.name }}</h3>
{% for topic in group.items %}<details class="hp-topic"><summary>{{ topic.term }} ({{ topic.papers.size }})</summary><ul>{% for p in topic.papers %}<li><a href="{{ p.url | relative_url }}">{{ p.title }}</a></li>{% endfor %}</ul></details>
{% endfor %}
{% endfor %}
</div>

<style>
  #hp-topics-list h3 { margin: 1em 0 0.2em; }
  .hp-topic { margin: 0; padding: 0.15em 0; border-bottom: 1px solid #eee; }
  .hp-topic summary { cursor: pointer; font-size: 0.9em; }
  .hp-topic summary:hover { color: #000; }
  .hp-topic ul { margin: 0.2em 0 0.4em 1.4em; padding: 0; }
  .hp-topic li { margin: 0; }
</style>
