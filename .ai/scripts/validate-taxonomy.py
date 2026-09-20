#!/usr/bin/env python3
"""Validate health-papers front matter against _data/taxonomy.yml.

Always errors (exit 1) on any systems/kind/lens value not present in the
controlled vocabulary — that's the actual goal of this script: a misspelled
category should never silently create a ghost category.

Missing `systems`/`kind` on a paper is only a warning by default, since
tagging is an in-progress migration (see .ai/plans/topic-taxonomy.md).
Pass --strict once migration is complete to promote that to an error too.
"""
import argparse
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
TAXONOMY_PATH = REPO_ROOT / "_data" / "taxonomy.yml"
PAPERS_DIR = REPO_ROOT / "health-papers"

FRONT_MATTER_RE = re.compile(r"\A---\s*\n(.*?\n)---\s*\n", re.DOTALL)


def load_vocab():
    taxonomy = yaml.safe_load(TAXONOMY_PATH.read_text())
    return {
        axis: {entry["slug"] for entry in taxonomy.get(axis, [])}
        for axis in ("systems", "kind", "lens")
    }


def parse_front_matter(path):
    match = FRONT_MATTER_RE.match(path.read_text())
    if not match:
        return None
    return yaml.safe_load(match.group(1)) or {}


def validate_paper(path, front_matter, vocab):
    errors = []
    warnings = []

    if front_matter is None:
        warnings.append("no front matter block found")
        return errors, warnings

    if "systems" not in front_matter:
        warnings.append("missing `systems`")
    else:
        systems = front_matter["systems"]
        if not isinstance(systems, list):
            errors.append(f"`systems` must be a list, got {systems!r}")
        else:
            for value in systems:
                if value not in vocab["systems"]:
                    errors.append(f"unknown `systems` value: {value!r}")

    if "kind" not in front_matter:
        warnings.append("missing `kind`")
    else:
        kind = front_matter["kind"]
        if kind not in vocab["kind"]:
            errors.append(f"unknown `kind` value: {kind!r}")

    lens = front_matter.get("lens") or []
    if not isinstance(lens, list):
        errors.append(f"`lens` must be a list, got {lens!r}")
    else:
        for value in lens:
            if value not in vocab["lens"]:
                errors.append(f"unknown `lens` value: {value!r}")

    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="treat missing systems/kind as errors, not warnings",
    )
    args = parser.parse_args()

    vocab = load_vocab()
    paper_paths = sorted(
        p for p in PAPERS_DIR.glob("*.md") if p.name != "index.md"
    )

    total_errors = 0
    total_warnings = 0

    for path in paper_paths:
        front_matter = parse_front_matter(path)
        errors, warnings = validate_paper(path, front_matter, vocab)

        if args.strict:
            errors.extend(warnings)
            warnings = []

        for message in errors:
            print(f"ERROR  {path.relative_to(REPO_ROOT)}: {message}")
        for message in warnings:
            print(f"warn   {path.relative_to(REPO_ROOT)}: {message}")

        total_errors += len(errors)
        total_warnings += len(warnings)

    print(
        f"\n{len(paper_paths)} papers checked, "
        f"{total_errors} error(s), {total_warnings} warning(s)"
        + (" (strict mode)" if args.strict else "")
    )
    return 1 if total_errors else 0


if __name__ == "__main__":
    sys.exit(main())
