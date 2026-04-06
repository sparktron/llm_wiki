# AGENTS.md

## Mission
Maintain a persistent markdown wiki that synthesizes raw sources over time. The wiki is the working knowledge layer between the user and the immutable raw source collection.

## Core principles

1. Raw sources are immutable.
2. The wiki is cumulative and persistent.
3. Prefer updating existing pages over creating duplicates.
4. Track contradictions explicitly instead of smoothing them away.
5. Preserve traceability from wiki claims back to source pages and raw files.
6. Keep formatting predictable and machine-operable.

## Directory ownership

- `raw/` is read-only from the agent's perspective.
- `wiki/` is the agent-maintained layer.
- `schema/` defines operational rules and page formats.
- `tools/` contains helper utilities the agent may invoke.

## Source policy

- Never modify files under `raw/`.
- Every ingested source must get:
  - a metadata manifest in `raw/manifests/`
  - a source page in `wiki/sources/`
- Source pages must link to the raw file path or source identifier.

## Required actions for every ingest

For each newly ingested source:

1. Read the source.
2. Complete or revise its source page.
3. Identify affected entities, concepts, topics, timelines, or syntheses.
4. Update existing pages where appropriate.
5. Create new pages only when a concept or entity is significant enough to justify one.
6. Update `wiki/index.md`.
7. Append an entry to `wiki/log.md`.

## Writing policy

### Separate these clearly:
- factual claims from sources
- interpretation / synthesis
- contradictions / tensions
- open questions / unknowns

### Never do these:
- silently overwrite a disputed claim
- create near-duplicate pages for slightly different phrasings
- add vague unsupported assertions
- bury important contradictions

## Canonical page types

- `source`
- `entity`
- `concept`
- `topic`
- `synthesis`
- `timeline`
- `decision`

## Frontmatter requirements

Every wiki page should include YAML frontmatter with, at minimum:

- `title`
- `type`
- `status`
- `created`
- `updated`
- `tags`

When useful, also include:

- `source_count`
- `confidence`
- `aliases`
- `schema_version`

## Citation and traceability policy

- Important claims should be traceable to source pages.
- Source pages should reference the raw file or source identifier.
- If a statement is uncertain, mark it clearly.
- If two sources disagree, record the disagreement under a contradiction / tension section.

## Query workflow

When answering a question:

1. Read `wiki/index.md` first.
2. Identify relevant wiki pages.
3. Read the most relevant pages.
4. Consult source pages or raw sources for verification when needed.
5. Answer from the maintained wiki whenever possible.
6. If the answer creates a valuable durable artifact, file it as a new synthesis page.

## Lint workflow

Periodically audit the wiki for:

- orphan pages
- broken wiki links
- missing frontmatter
- duplicate or overlapping pages
- stale pages
- uncited claims
- contradictions not reflected in topic summaries
- frequently mentioned concepts lacking a dedicated page

## Naming conventions

- Entity pages: canonical proper noun, singular form when applicable
- Concept pages: canonical concept phrase
- Topic pages: broader subject label
- Timeline pages: `<scope> timeline`
- Synthesis pages: concise descriptive title reflecting the actual analysis

## Editing preference hierarchy

When incorporating new information:

1. update an existing page if the concept already exists
2. create a new section if the concept is substantial but page-worthy within the same page
3. create a new page only if it materially improves organization or retrieval

## Index policy

`wiki/index.md` is content-oriented. It should list pages by category with a one-line summary.

## Log policy

`wiki/log.md` is chronological and append-only. Each entry should start with a heading in this format:

`## [YYYY-MM-DD] <operation> | <short title>`

Examples of operations:
- `ingest`
- `query`
- `lint`
- `merge`
- `schema-update`

## Quality bar

The wiki should become more coherent, more connected, and more useful over time. Every change should improve the long-term quality of the knowledge base, not just satisfy the immediate prompt.
