---
layout: page
title: "Liver & Detoxification"
description: "Fatty liver, hepatitis, the liver, natural detox systems, binders"
permalink: /health-papers/systems/liver-detox/
comments: false
exclude_from_papers: true
---

Fatty liver, hepatitis, the liver, natural detox systems, binders

[← All health papers](/health-papers/)

{% assign papers = site.pages | where_exp: "p", "p.path contains 'health-papers/'" | where_exp: "p", "p.exclude_from_papers != true" | where_exp: "p", "p.systems contains 'liver-detox'" | sort: "title" %}
{% if papers.size == 0 %}
No papers tagged with this system yet.
{% else %}
{% for k in site.data.taxonomy.kind %}
{% assign group = papers | where: "kind", k.slug %}
{% if group.size > 0 %}
### {{ k.label }}

{% for paper in group %}
- [{{ paper.title }}]({{ paper.url | relative_url }}){% if paper.lens contains 'adventist-heritage' %} <span title="Adventist heritage">📜</span>{% endif %}{% if paper.lens contains 'contested' %} <span title="Contested / disputed evidence">⚠️</span>{% endif %}
{% endfor %}

{% endif %}
{% endfor %}
{% endif %}
