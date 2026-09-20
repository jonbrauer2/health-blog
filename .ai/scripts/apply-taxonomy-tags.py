#!/usr/bin/env python3
"""Write approved systems/kind/aliases from a reviewed CSV into paper front matter.

Second half of Phase 2 (see .ai/plans/topic-taxonomy.md). Input is
.ai/tagging/phase2-proposed-tags.csv (or --csv) after human review/edits.
Idempotent: skips a paper if it already has `systems` or `kind` set, unless
--force is passed.
"""
import argparse
import csv
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CSV = REPO_ROOT / ".ai" / "tagging" / "phase2-proposed-tags.csv"
PAPERS_DIR = REPO_ROOT / "health-papers"
TAXONOMY_PATH = REPO_ROOT / "_data" / "taxonomy.yml"

FRONT_MATTER_RE = re.compile(r"\A---\s*\n(.*?\n)---\s*\n", re.DOTALL)


def load_vocab():
    taxonomy = yaml.safe_load(TAXONOMY_PATH.read_text())
    return {
        axis: {entry["slug"] for entry in taxonomy.get(axis, [])}
        for axis in ("systems", "kind", "lens")
    }


def flow_list(items):
    return "[" + ", ".join(items) + "]"


def apply_tags(path, systems, kind, aliases, force):
    text = path.read_text()
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return f"skip (no front matter): {path.name}"

    front_matter = yaml.safe_load(match.group(1)) or {}
    if not force and ("systems" in front_matter or "kind" in front_matter):
        return f"skip (already tagged): {path.name}"

    new_lines = [
        f"systems: {flow_list(systems)}",
        f"kind: {kind}",
        "lens: []",
        f"aliases: {flow_list(aliases)}",
    ]
    new_front_matter = match.group(1).rstrip("\n") + "\n" + "\n".join(new_lines) + "\n"
    new_text = f"---\n{new_front_matter}---\n" + text[match.end():]
    path.write_text(new_text)
    return f"tagged: {path.name}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--force", action="store_true", help="overwrite existing systems/kind")
    parser.add_argument("--dry-run", action="store_true", help="validate only, write nothing")
    args = parser.parse_args()

    vocab = load_vocab()
    applied = 0
    skipped = 0
    errors = []

    with args.csv.open() as f:
        for row in csv.DictReader(f):
            systems = [s for s in row["systems"].split("|") if s]
            kind = row["kind"].strip()
            aliases = [a for a in row["aliases"].split("|") if a]

            bad_systems = [s for s in systems if s not in vocab["systems"]]
            if bad_systems:
                errors.append(f"{row['filename']}: unknown systems {bad_systems}")
                continue
            if kind not in vocab["kind"]:
                errors.append(f"{row['filename']}: unknown kind '{kind}'")
                continue

            path = PAPERS_DIR / row["filename"]
            if not path.exists():
                errors.append(f"{row['filename']}: file not found")
                continue

            if args.dry_run:
                applied += 1
                continue

            result = apply_tags(path, systems, kind, aliases, args.force)
            print(result)
            if result.startswith("tagged"):
                applied += 1
            else:
                skipped += 1

    print(f"\n{applied} tagged, {skipped} skipped, {len(errors)} error(s)")
    for e in errors:
        print(f"ERROR  {e}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
