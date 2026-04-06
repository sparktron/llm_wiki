# Conventions

## Frontmatter example

```yaml
---
title: Example Page
type: concept
status: active
created: 2026-04-06
updated: 2026-04-06
schema_version: 1
source_count: 3
confidence: medium
tags:
  - example
  - knowledge-management
aliases:
  - Alternate Name
---
```

## Section conventions

Recommended section order:

1. Summary
2. Key points / current understanding
3. Evidence / supporting sources
4. Contradictions / tensions
5. Open questions
6. Related pages

## Link conventions

Use standard wiki links:

- `[[Page Name]]`
- `[[Page Name|Custom Label]]`

Prefer canonical page names instead of creating many aliases in prose.

## Contradiction formatting

Use this structure when sources disagree:

```md
## Contradictions / Tensions
- Source A claims ...
- Source B claims ...
- Current interpretation: ...
- Confidence: low
```

## Source page requirements

Every source page should include:

- source identifier
- raw file path
- ingest date
- concise summary
- key claims or findings
- entities mentioned
- concepts mentioned
- contradictions or tensions surfaced by the source
- follow-up actions or questions

## Confidence labels

Use one of:

- `low`
- `medium`
- `high`

These are editorial confidence levels in the synthesis, not claims of ground truth.
