---
layout: page
title: "Hormones & Metabolism"
description: "Thyroid, diabetes, hypoglycemia, metabolic syndrome, HPA axis"
permalink: /health-papers/systems/endocrine/
comments: false
exclude_from_papers: true
---

Thyroid, diabetes, hypoglycemia, metabolic syndrome, HPA axis

[← All health papers]({{ "/health-papers/" | relative_url }})

{% assign papers = site.pages | where_exp: "p", "p.path contains 'health-papers/'" | where_exp: "p", "p.exclude_from_papers != true" | where_exp: "p", "p.systems contains 'endocrine'" | sort: "title" %}
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
