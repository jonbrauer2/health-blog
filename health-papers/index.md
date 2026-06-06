---
layout: page
title: Health Papers
permalink: /health-papers/
comments: false
---

Comprehensive health guides and resources with scientific references.

---

<input type="search" id="hp-search" placeholder="Search health papers…" autocomplete="off" aria-label="Search health papers" style="width:100%;padding:0.6em 0.8em;font-size:1em;border:1px solid #ccc;border-radius:4px;box-sizing:border-box;margin-bottom:0.5em;">
<p id="hp-search-status" style="margin:0 0 1em;font-size:0.9em;color:#666;" hidden></p>
<div id="hp-search-results" hidden></div>

<div id="hp-list" markdown="1">
### Available Papers

{% assign papers = site.pages | where_exp: "p", "p.path contains 'health-papers/'" | where_exp: "p", "p.name != 'index.md'" | where_exp: "p", "p.title" | sort: "title" %}
{% for paper in papers %}
{{ forloop.index }}. [{{ paper.title }}]({{ paper.url | relative_url }}){% if paper.subtitle %} — *{{ paper.subtitle }}*{% endif %}
{% endfor %}
</div>

---

More papers coming soon.

<script>
(function () {
  var input = document.getElementById('hp-search');
  var status = document.getElementById('hp-search-status');
  var results = document.getElementById('hp-search-results');
  var list = document.getElementById('hp-list');
  var state = 'idle'; // idle | loading | ready | error
  var lunrIndex = null;
  var docsById = null;

  function setStatus(msg) {
    if (msg) { status.textContent = msg; status.hidden = false; }
    else { status.hidden = true; }
  }

  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var s = document.createElement('script');
      s.src = src;
      s.onload = resolve;
      s.onerror = function () { reject(new Error('Failed to load ' + src)); };
      document.head.appendChild(s);
    });
  }

  function ensureLoaded() {
    if (state === 'ready' || state === 'loading') return;
    state = 'loading';
    setStatus('Loading search index…');

    Promise.all([
      loadScript('https://unpkg.com/lunr@2.3.9/lunr.min.js'),
      fetch({{ "/health-papers/search-index.json" | relative_url | jsonify }}).then(function (r) {
        if (!r.ok) throw new Error('index fetch failed: ' + r.status);
        return r.json();
      })
    ]).then(function (parts) {
      var docs = parts[1];
      docsById = {};
      lunrIndex = lunr(function () {
        this.ref('i');
        this.field('t', { boost: 10 });
        this.field('c');
        docs.forEach(function (d) {
          docsById[d.i] = d;
          this.add(d);
        }, this);
      });
      state = 'ready';
      setStatus('');
      if (input.value) runSearch();
    }).catch(function (err) {
      state = 'error';
      setStatus('Search unavailable — using the list below.');
      console.error(err);
    });
  }

  function escapeHtml(s) {
    return s.replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function runSearch() {
    var q = input.value.trim();
    if (!q) {
      results.hidden = true;
      results.innerHTML = '';
      list.hidden = false;
      return;
    }
    if (state !== 'ready') return;

    var hits = [];
    try {
      hits = lunrIndex.search(q);
    } catch (e) {
      try {
        var soft = q.split(/\s+/).map(function (t) {
          return t.replace(/[^\wÀ-￿]/g, '') + '*';
        }).filter(Boolean).join(' ');
        if (soft) hits = lunrIndex.search(soft);
      } catch (e2) { hits = []; }
    }

    list.hidden = true;
    results.hidden = false;

    if (!hits.length) {
      results.innerHTML = '<p><em>No matches for &ldquo;' + escapeHtml(q) + '&rdquo;.</em></p>';
      return;
    }

    var html = '<ol>';
    hits.forEach(function (h) {
      var d = docsById[h.ref];
      if (d) html += '<li><a href="' + escapeHtml(d.u) + '">' + escapeHtml(d.t) + '</a></li>';
    });
    html += '</ol>';
    results.innerHTML = html;
  }

  input.addEventListener('focus', ensureLoaded);
  input.addEventListener('input', function () {
    if (state === 'ready') runSearch();
    else if (state === 'idle') ensureLoaded();
  });
})();
</script>
