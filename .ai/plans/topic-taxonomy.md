# Plan: Categories, Body Systems, and a Topic Index for Health Papers

Status: **Phase 1 in progress** (Phase 0 dedup deferred, decided separately)
Written: 2026-09-20
Scope: `health-papers/` (182 files today, expected to keep growing past 200)

## The problem

`health-papers/index.md` renders one flat alphabetical list of every paper, plus
a lazy-loaded Lunr full-text search. That was fine at 40 papers. At 182 it fails
in three specific ways:

1. **No browsing.** A reader who doesn't already know what they want has no path
   in. Alphabetical order puts "Acid Reflux" next to "Acne" next to "Actinic
   Keratosis" — adjacency carries no meaning.
2. **Search requires the right word.** Lunr matches text, so someone searching
   "GERD", "heartburn", or "thyroid" finds only papers that happen to use that
   exact term. There is no synonym or see-also layer.
3. **No sense of coverage.** Neither the reader nor the author can see what the
   collection actually covers, which is how we ended up with the duplicates
   catalogued below.

## Design principles

- **Data, not pages.** Every grouping is derived from front matter plus a
  controlled vocabulary in `_data/`. Adding paper #250 means adding front
  matter, not hand-editing an index.
- **No plugins.** GitHub Pages runs a fixed plugin set. Everything here is
  Liquid plus client-side JS — no `jekyll-archives`, no custom generators.
- **Two axes, not seven.** Faceted browse dies when there are too many facets.
  One primary axis (body system) and one secondary (kind of paper), plus
  optional flags.
- **Fail loudly on typos.** A misspelled category silently creates a ghost
  category. A validation script prevents that.

---

## Axis 1 (primary): Body system

This is the main browse grouping — the shelf a reader walks up to. Multi-valued,
because "Metabolic Syndrome" legitimately belongs to both cardiovascular and
endocrine.

Proposed vocabulary (16 values), drawn from what the 182 papers actually cover:

| slug | label | sample papers |
|---|---|---|
| `digestive` | Digestive & Gut | SIBO, IBS, leaky gut, acid reflux, parasites, probiotics |
| `cardiovascular` | Heart & Circulation | high blood pressure, hypotension, DVT, cardiovascular health |
| `respiratory` | Lungs & Breathing | asthma, acute bronchitis, lung health, sleep apnea, sinus |
| `neurological` | Brain & Nerves | Parkinson's, MS, neuropathy, migraines, essential tremor, carpal tunnel |
| `mental-health` | Mental & Emotional | depression, bipolar, schizophrenia, agoraphobia, autism |
| `endocrine` | Hormones & Metabolism | thyroid (x4), diabetes (x2), hypoglycemia, metabolic syndrome, HPA axis |
| `immune` | Immune & Autoimmune | lupus, Hashimoto's, allergies, MCAS, vaccines, HIV |
| `musculoskeletal` | Bones, Joints & Muscles | arthritis, osteoporosis, sciatica, frozen shoulder, disc herniation, muscular dystrophy |
| `skin` | Skin, Hair & Nails | acne, rosacea, vitiligo, melasma, hives, ringworm, hair loss (x2), melanoma |
| `urinary` | Kidneys & Urinary | UTIs, frequent urination, oxalates/stones |
| `reproductive` | Reproductive & Sexual | menstrual health (x2), ovarian cysts, prostate, ED, low libido, prenatal |
| `sensory` | Eyes & Ears | myopia, hearing loss, tinnitus, ear aches |
| `blood-lymph` | Blood & Lymphatic | leukemia, lymphoma, sickle cell, lymphatic health, electrolytes |
| `liver-detox` | Liver & Detoxification | fatty liver, hepatitis, the liver, natural detox systems, binders |
| `sleep` | Sleep | insomnia, narcolepsy, sleep paralysis, sleep apnea |
| `whole-body` | Whole-Body & Foundations | fatigue, 10 foundations, weight loss, chronic Lyme/CIRS, MCS |

`whole-body` is the escape hatch for papers that genuinely span everything. It
must stay small — if it grows past ~15 papers the vocabulary needs another value,
not a bigger junk drawer.

## Axis 2 (secondary): Kind of paper

Single-valued. Answers "what sort of thing am I reading?" — this is what makes
the collection legible, because roughly a third of these papers aren't about a
condition at all.

| slug | label | what belongs here |
|---|---|---|
| `condition` | Conditions | a disease or diagnosis — the largest group |
| `nutrition` | Food & Nutrition | cheese, butter, soy, oils, carbs, legumes, fermented foods, caffeine, MSG, sweeteners |
| `remedy` | Remedies & Therapies | hydrotherapy, castor oil packs, herbal medicine, essential oils, cold water immersion, fasting |
| `exposure` | Substances & Exposures | microplastics, mercury, fluoride, mold, microwaves, alcohol, smoking |
| `evaluation` | Claims Under Examination | applied kinesiology, live blood analysis, blood type diet, food-sensitivity testing, pyroluria, coffee enemas, ozone therapy, chelation, earthing |
| `foundations` | Foundations | 10 foundations for vitality, the body's detox systems, whole-person frameworks |

`evaluation` is the most valuable category on this site and currently the least
discoverable. A reader who wants "is this thing legitimate?" has no way to find
those ~10 papers today.

## Optional flags

Two multi-valued, entirely optional front-matter lists:

- `lens: [adventist-heritage]` — papers engaging Ellen White or Adventist health
  history (EGW on cheese, butter, Battle Creek soy, biblical response to applied
  kinesiology). A meaningful thread through this collection worth surfacing.
- `lens: [contested]` — papers where the honest answer is "the evidence is weak
  or disputed." Overlaps `evaluation` but is not identical; some conditions
  (pyroluria, chronic Lyme, MCS) are themselves contested.

Deliberately **not** doing: audience tags, difficulty ratings, reading time,
evidence-grade scores. Each is per-paper editorial overhead with thin payoff.

---

## Axis 3: The topic index (distinct from categories)

Categories are broad shelves. The topic index is a book-style A–Z of **terms** —
symptoms, common names, synonyms, and brand-adjacent words — each pointing at
one or more papers. This is what fixes "search requires the right word."

Mechanism: an `aliases:` list in each paper's front matter.

```yaml
aliases: [GERD, heartburn, reflux, acid indigestion, waterbrash]
```

Those feed three things at once:
1. The A–Z topic index page (`/health-papers/topics/`).
2. The Lunr search index — so searching "GERD" hits the acid reflux paper even
   though the paper may never use the word.
3. See-also cross-references between papers sharing aliases.

Target roughly 5–10 aliases per paper — ~1,200 index entries at current size.
This is the highest-effort piece and the highest-value one. It can ship after
the category work without blocking it.

---

## Blocker to handle first: duplicate papers

Tagging should not happen before deduplication, or the browse pages will show
the same topic two or three times. A size/hash comparison surfaced these
clusters — **all need an editorial decision, none should be auto-deleted**:

| topic | files | note |
|---|---|---|
| Fasting | `fasting-benefits-risks-physiology.md`, `fasting-clear-eyed-guide.md` | **identical titles**, different bodies (37KB / 44KB) |
| Oxalates | `complete-guide-to-oxalates.md`, `dietary-oxalates-evidence-guide.md`, `understanding-oxalates.md` | three papers, one topic |
| Asthma | `breathing-room-asthma.md`, `breathing-room-whole-person-asthma.md` | 20KB vs 41KB — looks like a draft and its expansion |
| Leaky gut | `leaky-gut-calibrated-guide.md`, `leaky-gut-what-the-science-says.md` | |
| Alcohol | `alcohol-health-current-research.md`, `alcohol-health-science-guide.md` | |
| Cold water immersion | `cold-water-immersion.md`, `cold-water-immersion-evidence-handout.md` | |
| Clothing | `clothing-choices-and-physical-health.md`, `clothing-health-guide.md` | |
| Weight loss | `weight-loss.md`, `understanding-weight-loss.md` | |
| Air quality | `breathing-better-air-quality.md`, `the-air-you-breathe-air-quality.md` | |
| Baking soda | `baking-soda-baking-powder-handout.md`, `baking-soda-powder-rising-concerns.md` | |
| Depression | `lifting-the-fog-depression.md`, `roots-of-depression.md`, `whole-person-troubled-mind.md` | third covers bipolar + schizophrenia too |
| Type 2 diabetes | `living-well-type-2-diabetes.md`, `rewriting-blood-sugar-story-diabetes.md` | |
| Vaccines | `understanding-vaccinations.md`, `immunizations-informed-choices.md` | |
| Antibiotics | `antibiotics-vs-natural-approaches.md`, `smart-choices-about-antibiotics.md` | |
| Reflux | `acid-reflux-what-your-body-is-trying-to-tell-you.md`, `heartburn-reflux-guide.md` | |
| Gut/digestion | `your-gut-your-health-digestive-wellness.md`, `what-your-gut-is-telling-you.md` | second is diarrhea/constipation-specific |
| Tremor | `living-well-with-essential-tremor.md`, `hand-tremors-and-shaky-hands.md` | |

Genuinely distinct despite looking paired — **keep both**: butter (general vs.
EGW), cheese (general vs. EGW), applied kinesiology (general vs. biblical
response), hydrotherapy (general vs. cold-relief protocol).

Resolution per cluster is one of: merge into the stronger paper and delete the
weaker; keep both and differentiate the titles; or keep both with a
`canonical:` pointer so only one appears in browse. Expect this to take ~160
papers down from 182.

---

## Implementation

### Phase 0 — Deduplicate
Review the clusters above, decide merge/keep/differentiate for each, execute.
Redirect any deleted URL with a `redirect_to` stub (papers may be linked from
ezra-blog or shared directly).

### Phase 1 — Vocabulary + validation
- `_data/taxonomy.yml` — the controlled vocabulary: slug, label, description,
  and display order for both axes.
- `.ai/scripts/validate-taxonomy.py` — fails if any paper carries a value not in
  `_data/taxonomy.yml`, or is missing `systems`/`kind` entirely. Wire into a
  GitHub Action on push so a typo can't reach `main` unnoticed.

### Phase 2 — Tag the papers
The bulk of the effort: ~160 papers × (systems + kind + aliases). Do it as a
scripted first pass that writes a reviewable CSV (slug, proposed systems,
proposed kind, proposed aliases), human-review the CSV, then a second script
writes the approved values into front matter. Reviewing a CSV is far faster than
opening 160 files, and the CSV is re-runnable if the vocabulary changes.

### Phase 3 — Browse UI
- Rewrite `health-papers/index.md`: papers grouped under body-system headings,
  with a kind filter and a system filter as chips at the top.
- Filtering is **client-side** over the existing index fetch — one JSON, no
  combinatorial explosion of generated pages, and it composes with the search
  box already on the page.
- Extend `health-papers/search-index.json` (already a Liquid template, so this
  is a small edit) to emit `systems`, `kind`, `lens`, and `aliases` alongside
  the current title/url/content fields. One fetch powers both search and filter.
- Keep a plain alphabetical list reachable as a fallback view.

### Phase 4 — Topic index
- `/health-papers/topics/` — A–Z of all aliases and titles, each linking to its
  paper(s), with see-also for shared terms. Pure Liquid over `site.pages`.

### Phase 5 — Per-paper navigation
- Category chips in the paper layout linking back to the browse view.
- "Related papers" from shared systems + aliases.

Phases 3–5 each stand alone and ship independently once Phase 2 is done.

## Front-matter contract (final shape)

```yaml
---
layout: page
title: "Acid Reflux: What Your Body Is Trying to Tell You"
permalink: /health-papers/acid-reflux-what-your-body-is-trying-to-tell-you/
systems: [digestive]
kind: condition
lens: []
aliases: [GERD, heartburn, reflux, acid indigestion]
---
```

`systems` and `kind` required; `lens` and `aliases` optional. Existing papers
keep working un-tagged during migration — untagged papers fall into an
"Uncategorized" group on the browse page, which doubles as the migration
progress tracker.

## Decisions (resolved 2026-09-20)

1. `theory-papers/` stays **separate** — does not share this taxonomy.
2. Body-system pages **do** get real URLs (`/health-papers/systems/<slug>/`),
   ~16 stub pages generated from `_data/taxonomy.yml` in Phase 3.
3. ezra-blog's redirect needs no change — it points at `/health-papers/`,
   which stays valid regardless of what that page renders.
4. Phase 0 (dedup) is **deferred** — being decided separately, outside this
   plan's automation. Phase 1 scaffolding proceeds without waiting on it;
   the validator (below) is written to not assume dedup or full tagging has
   happened yet.

## Note: validator strictness during migration

Phase 1's original wording ("fails if... missing `systems`/`kind` entirely")
conflicts with the front-matter contract's migration allowance ("existing
papers keep working un-tagged"). Resolved as: the validator always errors on
values not in `_data/taxonomy.yml` (typo protection, the actual goal of this
phase); it only *warns* (non-failing, listed for tracking) on papers missing
`systems`/`kind`, via a `--strict` flag to promote that to an error once
Phase 2 tagging is complete and CI should start enforcing full coverage.
