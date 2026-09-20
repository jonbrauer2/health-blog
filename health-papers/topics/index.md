---
layout: page
title: Topic Index
permalink: /health-papers/topics/
comments: false
exclude_from_papers: true
---

An A–Z index of terms, symptoms, and common names covered across the health
papers — useful when you don't know the "official" name for what you're
looking for. Terms shared by more than one paper are listed as see-also.

[← All health papers](/health-papers/)

{% assign topics = site.data.topics %}
{% assign grouped = topics | group_by_exp: "t", "t.term | slice: 0, 1 | upcase" %}

<nav id="hp-topics-jump" style="margin:1em 0;font-size:0.9em;">
{% for group in grouped %}<a href="#letter-{{ group.name | slugify }}" style="margin-right:0.6em;">{{ group.name }}</a>{% endfor %}
</nav>

{% for group in grouped %}
### <span id="letter-{{ group.name | slugify }}">{{ group.name }}</span>

{% for topic in group.items %}
- {{ topic.term }} — {% for p in topic.papers %}[{{ p.title }}]({{ p.url | relative_url }}){% unless forloop.last %}, {% endunless %}{% endfor %}

{% endfor %}
{% endfor %}
