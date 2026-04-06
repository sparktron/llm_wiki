# Conventions

## Folder layout
- `raw/`: immutable source material (PDFs, notes, exports).
- `wiki/sources/`: source summary pages (1 page per raw source).
- `wiki/pages/`: synthesized topic pages.
- `wiki/index.md`: canonical index.
- `wiki/log.md`: chronological operation log.
- `tools/`: local helper scripts.

## Frontmatter
All `wiki/sources/*.md` pages require:
- `title`
- `source_id`
- `source_path`
- `source_type` (optional but recommended)
- `created`
- `updated`

All `wiki/pages/*.md` pages require:
- `title`
- `slug`
- `created`
- `updated`
- `citations` (list of source IDs)

Dates must use ISO format (`YYYY-MM-DD`).

## Section conventions
Source pages should include:
1. `## Source metadata`
2. `## Key facts`
3. `## Open questions`

Topic pages should include:
1. `## Summary`
2. `## Evidence`
3. `## Related pages`
4. `## Open questions`

## Citation format
Use source IDs inline, e.g. `(source: SRC-2026-0001)`.

## Link style
Use relative markdown links:
- `../sources/<id>.md`
- `./<slug>.md`
