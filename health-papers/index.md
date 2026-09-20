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

<div id="hp-filters" hidden style="margin-bottom:1.2em;">
  <div style="margin-bottom:0.4em;">
    <strong style="font-size:0.85em;color:#666;">Body system:</strong>
    <span data-facet="systems">
      <button type="button" class="hp-chip is-active" data-value="" aria-pressed="true">All</button>
      {% for s in site.data.taxonomy.systems %}<button type="button" class="hp-chip" data-value="{{ s.slug }}" aria-pressed="false">{{ s.label }}</button>
      {% endfor %}
    </span>
  </div>
  <div style="margin-bottom:0.4em;">
    <strong style="font-size:0.85em;color:#666;">Kind:</strong>
    <span data-facet="kind">
      <button type="button" class="hp-chip is-active" data-value="" aria-pressed="true">All</button>
      {% for k in site.data.taxonomy.kind %}<button type="button" class="hp-chip" data-value="{{ k.slug }}" aria-pressed="false">{{ k.label }}</button>
      {% endfor %}
    </span>
  </div>
  <button type="button" id="hp-view-toggle" style="font-size:0.85em;color:#666;background:none;border:none;text-decoration:underline;cursor:pointer;padding:0;">Show plain alphabetical list</button>
</div>

<div id="hp-groups" hidden></div>

<div id="hp-list" markdown="1">
### Available Papers

{% assign papers = site.pages | where_exp: "p", "p.path contains 'health-papers/'" | where_exp: "p", "p.name != 'index.md'" | where_exp: "p", "p.exclude_from_papers != true" | where_exp: "p", "p.title" | sort: "title" %}
{% for paper in papers %}
{{ forloop.index }}. [{{ paper.title }}]({{ paper.url | relative_url }}){% if paper.subtitle %} — *{{ paper.subtitle }}*{% endif %}
{% endfor %}
</div>

---

More papers coming soon.

<style>
  .hp-chip { font-size: 0.85em; padding: 0.25em 0.6em; margin: 0.15em 0.25em 0.15em 0; border: 1px solid #ccc; border-radius: 999px; background: #fff; cursor: pointer; }
  .hp-chip.is-active { background: #333; color: #fff; border-color: #333; }
  #hp-groups h3 { margin-bottom: 0.3em; }
  #hp-groups .hp-group { margin-bottom: 1.2em; }
  .hp-kind-tag { font-size: 0.75em; color: #888; margin-left: 0.4em; }
</style>

<script>
(function () {
  var input = document.getElementById('hp-search');
  var status = document.getElementById('hp-search-status');
  var results = document.getElementById('hp-search-results');
  var list = document.getElementById('hp-list');
  var filters = document.getElementById('hp-filters');
  var groups = document.getElementById('hp-groups');
  var viewToggle = document.getElementById('hp-view-toggle');

  var state = 'idle';      // idle | loading | ready | error  (docs fetch)
  var lunrState = 'idle';  // idle | loading | ready | error
  var lunrIndex = null;
  var docsById = null;
  var allDocs = null;
  var activeSystem = '';
  var activeKind = '';
  var browseView = 'list'; // 'groups' once JS renders successfully

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

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function chipLabels(facet) {
    var map = {};
    var order = [];
    document.querySelectorAll('#hp-filters [data-facet="' + facet + '"] .hp-chip[data-value]').forEach(function (btn) {
      var v = btn.getAttribute('data-value');
      if (!v) return;
      map[v] = btn.textContent;
      order.push(v);
    });
    return { map: map, order: order };
  }

  function renderSection(slug, label, docs, kindMap) {
    var items = docs.map(function (d) {
      var kindLabel = d.k ? (kindMap[d.k] || d.k) : '';
      var badges = '';
      if (d.l && d.l.indexOf('adventist-heritage') !== -1) badges += ' <span title="Adventist heritage">📜</span>';
      if (d.l && d.l.indexOf('contested') !== -1) badges += ' <span title="Contested / disputed evidence">⚠️</span>';
      return '<li data-kind="' + escapeHtml(d.k || '') + '"><a href="' + escapeHtml(d.u) + '">' + escapeHtml(d.t) + '</a>' +
        (kindLabel ? ' <span class="hp-kind-tag">' + escapeHtml(kindLabel) + '</span>' : '') + badges + '</li>';
    }).join('');
    return '<section class="hp-group" data-system="' + escapeHtml(slug) + '"><h3>' + escapeHtml(label) + '</h3><ul>' + items + '</ul></section>';
  }

  function renderGroups() {
    var systems = chipLabels('systems');
    var kinds = chipLabels('kind');
    var html = '';

    systems.order.forEach(function (slug) {
      var docs = allDocs.filter(function (d) { return d.sy && d.sy.indexOf(slug) !== -1; });
      if (!docs.length) return;
      html += renderSection(slug, systems.map[slug], docs, kinds.map);
    });

    var uncategorized = allDocs.filter(function (d) { return !d.sy || !d.sy.length; });
    if (uncategorized.length) {
      html += renderSection('uncategorized', 'Uncategorized', uncategorized, kinds.map);
    }

    groups.innerHTML = html;
  }

  function applyFilters() {
    document.querySelectorAll('#hp-groups .hp-group').forEach(function (section) {
      var sysMatch = !activeSystem || section.getAttribute('data-system') === activeSystem;
      if (!sysMatch) { section.hidden = true; return; }
      var visible = 0;
      section.querySelectorAll('li').forEach(function (li) {
        var match = !activeKind || li.getAttribute('data-kind') === activeKind;
        li.hidden = !match;
        if (match) visible++;
      });
      section.hidden = visible === 0;
    });
  }

  function setActiveChip(facet, value) {
    document.querySelectorAll('#hp-filters [data-facet="' + facet + '"] .hp-chip').forEach(function (btn) {
      var active = btn.getAttribute('data-value') === value;
      btn.classList.toggle('is-active', active);
      btn.setAttribute('aria-pressed', active ? 'true' : 'false');
    });
  }

  function showBrowse(view) {
    browseView = view;
    groups.hidden = view !== 'groups';
    list.hidden = view !== 'list';
    viewToggle.textContent = view === 'groups' ? 'Show plain alphabetical list' : 'Show grouped view';
  }

  function loadDocs() {
    if (state === 'ready' || state === 'loading') return;
    state = 'loading';
    fetch({{ "/health-papers/search-index.json" | relative_url | jsonify }})
      .then(function (r) {
        if (!r.ok) throw new Error('index fetch failed: ' + r.status);
        return r.json();
      })
      .then(function (docs) {
        allDocs = docs;
        docsById = {};
        docs.forEach(function (d) { docsById[d.i] = d; });
        state = 'ready';
        renderGroups();
        applyFilters();
        filters.hidden = false;
        showBrowse('groups');
      })
      .catch(function (err) {
        state = 'error';
        console.error(err);
      });
  }

  function ensureLunr() {
    if (lunrState === 'ready' || lunrState === 'loading') return;
    if (state !== 'ready') { loadDocs(); return; }
    lunrState = 'loading';
    setStatus('Loading search index…');
    loadScript('https://unpkg.com/lunr@2.3.9/lunr.min.js').then(function () {
      lunrIndex = lunr(function () {
        this.ref('i');
        this.field('t', { boost: 10 });
        this.field('c');
        allDocs.forEach(function (d) { this.add(d); }, this);
      });
      lunrState = 'ready';
      setStatus('');
      if (input.value) runSearch();
    }).catch(function (err) {
      lunrState = 'error';
      setStatus('Search unavailable — using the list below.');
      console.error(err);
    });
  }

  function runSearch() {
    var q = input.value.trim();
    if (!q) {
      results.hidden = true;
      results.innerHTML = '';
      showBrowse(state === 'ready' ? 'groups' : 'list');
      return;
    }
    if (lunrState !== 'ready') return;

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

    groups.hidden = true;
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

  document.addEventListener('click', function (e) {
    var chip = e.target.closest ? e.target.closest('.hp-chip') : null;
    if (!chip || !filters.contains(chip)) return;
    var group = chip.closest('[data-facet]');
    var facet = group.getAttribute('data-facet');
    var value = chip.getAttribute('data-value');
    setActiveChip(facet, value);
    if (facet === 'systems') activeSystem = value;
    if (facet === 'kind') activeKind = value;
    applyFilters();
  });

  viewToggle.addEventListener('click', function () {
    showBrowse(browseView === 'groups' ? 'list' : 'groups');
  });

  input.addEventListener('focus', ensureLunr);
  input.addEventListener('input', function () {
    if (lunrState === 'ready') runSearch();
    else if (lunrState === 'idle') ensureLunr();
  });

  loadDocs();
})();
</script>
