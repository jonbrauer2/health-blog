# .ai/

Working material for AI-assisted development of this site: plans, design notes,
scratch analysis. **Nothing here is published.**

Jekyll ignores dot-directories by default, and `.ai/` is also listed explicitly
under `exclude:` in `_config.yml` so the exclusion survives any future change to
Jekyll's default behavior.

- `plans/` — design and implementation plans, one file per initiative.

Content that the *site* consumes (category vocabularies, paper metadata) does
not belong here. That belongs in `_data/`.
