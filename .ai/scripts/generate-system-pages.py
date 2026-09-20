#!/usr/bin/env python3
"""Generate health-papers/systems/<slug>.md stub pages from _data/taxonomy.yml.

Phase 3 of .ai/plans/topic-taxonomy.md. Idempotent: re-running overwrites the
generated files with the current vocabulary. Safe to re-run whenever
_data/taxonomy.yml changes.
"""
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
TAXONOMY_PATH = REPO_ROOT / "_data" / "taxonomy.yml"
OUT_DIR = REPO_ROOT / "health-papers" / "systems"

TEMPLATE = """---
layout: page
title: "{label}"
description: "{description}"
permalink: /health-papers/systems/{slug}/
comments: false
exclude_from_papers: true
---

{description}

[← All health papers](/health-papers/)

{{% assign papers = site.pages | where_exp: "p", "p.path contains 'health-papers/'" | where_exp: "p", "p.exclude_from_papers != true" | where_exp: "p", "p.systems contains '{slug}'" | sort: "title" %}}
{{% if papers.size == 0 %}}
No papers tagged with this system yet.
{{% else %}}
{{% for k in site.data.taxonomy.kind %}}
{{% assign group = papers | where: "kind", k.slug %}}
{{% if group.size > 0 %}}
### {{{{ k.label }}}}

{{% for paper in group %}}
- [{{{{ paper.title }}}}]({{{{ paper.url | relative_url }}}}){{% if paper.lens contains 'adventist-heritage' %}} <span title="Adventist heritage">📜</span>{{% endif %}}{{% if paper.lens contains 'contested' %}} <span title="Contested / disputed evidence">⚠️</span>{{% endif %}}
{{% endfor %}}

{{% endif %}}
{{% endfor %}}
{{% endif %}}
"""


def main():
    taxonomy = yaml.safe_load(TAXONOMY_PATH.read_text())
    OUT_DIR.mkdir(exist_ok=True)
    written = 0
    for entry in taxonomy["systems"]:
        content = TEMPLATE.format(
            label=entry["label"],
            description=entry["description"],
            slug=entry["slug"],
        )
        out_path = OUT_DIR / f"{entry['slug']}.md"
        out_path.write_text(content)
        written += 1
    print(f"wrote {written} system pages to {OUT_DIR.relative_to(REPO_ROOT)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
