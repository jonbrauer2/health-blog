---
layout: page
title: Theory Development Papers
linktitle: Theory Development
permalink: /theory-papers/
comments: false
---

Papers developing a coherent framework for health research methodology, evidence integration, and how to think about claims under uncertainty.

---

### Available Papers

{% assign papers = site.pages | where_exp: "p", "p.path contains 'theory-papers/'" | where_exp: "p", "p.name != 'index.md'" | where_exp: "p", "p.title" | sort: "title" %}
{% for paper in papers %}
{{ forloop.index }}. [{{ paper.title }}]({{ paper.url | relative_url }}){% if paper.subtitle %} — *{{ paper.subtitle }}*{% endif %}
{% endfor %}

---

More papers coming soon.
