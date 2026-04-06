# LLM Wiki Starter

A local, markdown-first starter repository for building a persistent, LLM-maintained knowledge base.

This repo implements a pattern where **raw sources remain immutable**, while an LLM agent incrementally builds and maintains a persistent wiki of curated summaries, entity pages, concepts, syntheses, and timelines. Instead of re-analyzing the same sources on every query, the wiki becomes a maintained codebase of knowledge.

## Why use this?

- **Knowledge accumulation**: Build a single source of truth instead of re-deriving answers from raw sources
- **Auditability**: Every wiki claim traces back to source pages and raw files
- **Portability**: Pure markdown—no database, no proprietary formats, easy to version control
- **Agent-operable**: Explicit rules and templates let LLM agents maintain the wiki autonomously
- **Human-readable**: Easy to browse, edit, and reason about the knowledge structure

## Quick start

### 1. Clone and initialize

```bash
git clone <repository> llm-wiki
cd llm-wiki
git init  # if not already a repo
```

### 2. Add a source document

Drop a document into `raw/inbox/`:

```bash
cp ~/Downloads/research-paper.pdf raw/inbox/
# or:
cp ~/Documents/article.md raw/inbox/
```

### 3. Register the source

Register the file to create a metadata manifest and a stub source page:

```bash
python3 tools/ingest.py --file raw/inbox/research-paper.pdf
```

This creates:
- `raw/manifests/src-YYYY-MM-DD-<slug>.json` — metadata (checksum, date, original path)
- `wiki/sources/src-YYYY-MM-DD-<slug>.md` — a template source page

### 4. Ask an LLM agent to ingest it

Provide the agent with:
1. The contents of `schema/AGENTS.md` (operating instructions)
2. A request like:

> Please ingest the source registered at `raw/inbox/research-paper.pdf`. Read the raw file, complete the source page, identify any affected entities or concepts, update relevant wiki pages, update `wiki/index.md`, and append an entry to `wiki/log.md`.

The agent will:
- Read the raw source
- Complete the source page with key findings, claims, and contradictions
- Create or update entity, concept, topic, and synthesis pages as needed
- Maintain backlinks and cross-references
- Keep the wiki index and log current

### 5. Review and commit

```bash
git diff wiki/
# review changes carefully
git add wiki/ raw/manifests/
git commit -m "ingest: research-paper.pdf — key findings on topic X"
```

### 6. Archive the raw source

Once reviewed, move the raw file to processed:

```bash
mv raw/inbox/research-paper.pdf raw/processed/
```

## Directory structure

```
llm-wiki/
├── raw/
│   ├── inbox/              # new sources waiting to be ingested
│   ├── processed/          # sources that have been ingested and reviewed
│   ├── assets/             # downloaded images, PDFs, attachments
│   └── manifests/          # auto-generated metadata for each source
│
├── wiki/
│   ├── index.md            # content-oriented map of all wiki pages
│   ├── log.md              # chronological record of all operations
│   ├── overview.md         # top-level summary / framing of the wiki
│   ├── entities/           # proper nouns (people, organizations, events)
│   ├── concepts/           # abstract concepts and frameworks
│   ├── topics/             # subject areas and domains
│   ├── sources/            # one page per ingested source
│   ├── syntheses/          # durable answers, analyses, comparisons
│   ├── timelines/          # chronological summaries
│   └── decisions/          # decisions and their rationales
│
├── schema/
│   ├── AGENTS.md           # operating rules for LLM agents
│   ├── conventions.md      # frontmatter, naming, link conventions
│   ├── workflows.md        # detailed workflows (ingest, query, lint)
│   └── page_templates/     # markdown templates for each page type
│       ├── entity.md
│       ├── concept.md
│       ├── topic.md
│       ├── source.md
│       ├── synthesis.md
│       ├── timeline.md
│       └── decision.md
│
├── tools/
│   ├── ingest.py           # register sources and generate stubs
│   ├── lint.py             # validate wiki structure and links
│   ├── search.py           # simple markdown-based search
│   └── utils.py            # shared helpers
│
└── prompts/
    ├── codex_implementation_prompt.md
    └── claude_code_implementation_prompt.md
```

## Core workflows

### Ingest workflow

**Goal**: Add a new source and integrate its knowledge into the wiki.

1. **Place file**: Drop a document into `raw/inbox/`
2. **Register**: Run `python3 tools/ingest.py --file raw/inbox/<filename>`
3. **Ingest**: Ask an LLM agent to read the source, complete the source page, and update affected wiki pages
4. **Review**: Use `git diff` to inspect all changes
5. **Commit**: Commit the wiki updates and manifest
6. **Archive**: Move the raw file to `raw/processed/`

**Example**:
```bash
cp research_paper.pdf raw/inbox/
python3 tools/ingest.py --file raw/inbox/research_paper.pdf
# Give agent the ingest task...
git diff wiki/
git add wiki/ raw/manifests/
git commit -m "ingest: research_paper.pdf"
mv raw/inbox/research_paper.pdf raw/processed/
```

### Query workflow

**Goal**: Answer a question by consulting the wiki, not the raw sources.

1. **Start at the index**: Read `wiki/index.md` to understand what pages exist
2. **Find relevant pages**: Identify pages that relate to the question
3. **Read wiki pages**: Consult the relevant pages (entity, concept, topic, synthesis)
4. **Check sources if needed**: Only read source pages or raw files if verification is required
5. **Synthesize**: Answer from the wiki
6. **Save if durable**: If the answer creates a valuable artifact, file it as a new synthesis page

**Example**:
```
Q: What are the key differences between approach A and approach B?

1. Check wiki/index.md → find "approach-a" and "approach-b" concept pages
2. Read wiki/concepts/approach-a.md and wiki/concepts/approach-b.md
3. Consult source pages if contradictions or unclear claims exist
4. Synthesize an answer
5. If the answer is worth keeping, create wiki/syntheses/comparison-a-vs-b.md
```

### Lint workflow

**Goal**: Maintain wiki health by catching broken links, orphan pages, and missing metadata.

```bash
python3 tools/lint.py
```

This reports:
- Missing frontmatter
- Broken wiki links (`[[...]]`)
- Orphan pages (pages not linked from anywhere)
- Duplicate page titles
- Stale pages (not updated recently)

Review and fix issues. If a pattern appears repeatedly, consider updating `schema/AGENTS.md` or templates.

### Schema update workflow

**Goal**: Fix systematic issues in the wiki structure.

When repeated problems emerge:
1. Update `schema/AGENTS.md` or page templates in `schema/page_templates/`
2. Increment `schema_version` in new pages if necessary
3. Document the change in `wiki/log.md`

Example: If source pages keep missing a "follow-up actions" section, add it to the template.

## Tools

### `tools/ingest.py`

Registers a new source and generates a metadata manifest and stub source page.

```bash
python3 tools/ingest.py --file raw/inbox/<filename>
```

**Output**:
- `raw/manifests/src-YYYY-MM-DD-<slug>.json` — metadata (checksum, ingest date)
- `wiki/sources/src-YYYY-MM-DD-<slug>.md` — source page template

**Options**:
```bash
python3 tools/ingest.py --file <path>          # register a file
python3 tools/ingest.py --help                  # show all options
```

### `tools/lint.py`

Validates wiki structure and identifies common issues.

```bash
python3 tools/lint.py
```

**Reports**:
- Pages with missing frontmatter fields
- Broken wiki links (`[[...]]` pointing to non-existent pages)
- Orphan pages (not linked from index or elsewhere)
- Duplicate titles
- Pages not updated in 90+ days

**Usage**:
```bash
python3 tools/lint.py                           # check entire wiki
python3 tools/lint.py --path wiki/concepts/     # check specific directory
```

### `tools/search.py`

Simple markdown-based full-text search across the wiki.

```bash
python3 tools/search.py "query term"
```

**Output**: List of pages and line numbers containing the query.

**Example**:
```bash
python3 tools/search.py "transformer architecture"
# wiki/concepts/transformers.md:4
# wiki/entities/bert.md:12
# wiki/sources/src-2026-04-06-paper.md:18
```

## Page types and templates

Each wiki page has a **type** (entity, concept, topic, etc.) and follows a standard template:

### Source pages

One page per ingested source. Contains a summary, key claims, and metadata.

```yaml
---
title: "Research Paper: Transformers"
type: source
status: active
created: 2026-04-06
updated: 2026-04-06
schema_version: 1
source_count: 1
confidence: medium
tags:
  - source
  - transformers
aliases: []
---

# Research Paper: Transformers

## Summary
Brief overview of what the source says.

## Source metadata
- Source ID: `src-2026-04-06-transformers`
- Raw file: `raw/processed/transformers.pdf`
- Ingest date: `2026-04-06`

## Key points / findings
- Finding 1
- Finding 2

## Entities mentioned
- [[entity-name]]

## Concepts mentioned
- [[concept-name]]

## Contradictions / Tensions
None identified.

## Open questions
- What's the impact on older architectures?
```

### Entity pages

Proper nouns (people, organizations, papers, events).

**Example**: `wiki/entities/bert.md`

### Concept pages

Abstract concepts, frameworks, techniques.

**Example**: `wiki/concepts/attention-mechanism.md`

### Topic pages

Broader subject areas that may contain multiple concepts and entities.

**Example**: `wiki/topics/neural-networks.md`

### Synthesis pages

Durable answers, comparisons, or analyses derived from the wiki.

**Example**: `wiki/syntheses/comparison-transformers-vs-rnns.md`

See `schema/page_templates/` for full templates.

## Conventions

### Frontmatter

Every page includes YAML frontmatter with metadata:

```yaml
---
title: "Page Title"
type: entity | concept | topic | source | synthesis | timeline | decision
status: active | deprecated | draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
schema_version: 1
source_count: 3  # number of sources cited
confidence: low | medium | high  # editorial confidence
tags:
  - tag1
  - tag2
aliases:
  - "Alternative name"
---
```

### Linking

Use wiki links to cross-reference pages:

```markdown
See [[related-page]] for more.
See [[related-page|custom label]] for details.
```

### Sections

Recommended section order:

1. **Summary** — one-paragraph overview
2. **Key points** — bullet list of main findings
3. **Evidence** — source citations
4. **Contradictions / Tensions** — conflicting claims with source attribution
5. **Open questions** — unknowns or gaps
6. **Related pages** — backlinks and cross-references

### Contradictions

When sources disagree, record it explicitly:

```markdown
## Contradictions / Tensions

- Source A claims: X is true
- Source B claims: X is false
- Current interpretation: Further research needed
- Confidence: low
```

Don't smooth over disagreements. The wiki should reflect reality, including uncertainty.

## Operating principles

The wiki maintains several core principles:

1. **Raw sources are immutable** — never edit files in `raw/`; create wiki pages instead
2. **The wiki is cumulative** — each ingest should improve, not replace, prior synthesis
3. **Prefer updating over creating** — update existing pages before creating new ones
4. **Track contradictions** — record disagreements between sources explicitly
5. **Trace everything back** — every major claim should trace to a source page
6. **Keep it machine-operable** — consistent formatting and structure enable automation

See `schema/AGENTS.md` for more details.

## MVP boundaries

This starter intentionally avoids early overengineering:

- ❌ No database or SQL
- ❌ No vector store or embeddings
- ❌ No background workers or scheduled jobs
- ❌ No web UI or HTTP server
- ❌ No team sync, permissions, or multi-user features

These can be added later once the wiki structure and workflows stabilize. Start with pure markdown.

## Example session

```bash
# 1. Add a document
cp ~/research/ml-trends.md raw/inbox/

# 2. Register it
python3 tools/ingest.py --file raw/inbox/ml-trends.md

# 3. Ask an agent to ingest
# [Provide AGENTS.md and ask agent to ingest...]

# 4. Review
git diff wiki/

# 5. Commit
git add wiki/ raw/manifests/
git commit -m "ingest: ml-trends.md — 2026 ML landscape overview"

# 6. Archive
mv raw/inbox/ml-trends.md raw/processed/

# 7. Query the wiki later
python3 tools/search.py "transformer"
# [read relevant pages from output...]
```

## Best practices

### During ingestion

- **Be specific**: If updating existing pages, cite the source page in the edit
- **Avoid duplicates**: Check if a concept already exists before creating a new page
- **Mark uncertainty**: Use confidence labels (low/medium/high) liberally
- **Preserve contradictions**: Don't hide disagreements between sources
- **Keep the index current**: `wiki/index.md` should always reflect the current state

### During queries

- **Start at the index**: Always consult `wiki/index.md` first
- **Trust the wiki**: Answer from the wiki, not the raw sources
- **Verify when uncertain**: Pull source pages or raw files only if claims seem unreliable
- **Save useful results**: If a query produces a valuable artifact, file it as a synthesis page

### Long-term maintenance

- **Lint periodically**: Run `python3 tools/lint.py` every few ingests
- **Review the log**: Skim `wiki/log.md` to understand what's changed recently
- **Update the schema**: If a pattern breaks or a new structure helps, update the templates
- **Commit often**: Small, descriptive commits make the knowledge history more useful

## Troubleshooting

### "Broken link in wiki/index.md"

A link like `[[foo]]` points to a page that doesn't exist. Either:
- Create `wiki/<category>/foo.md`
- Update the link to an existing page
- Mark it as a TODO and create the page later

### "Source page not filling in"

If an agent struggles to complete a source page:
- Provide more context about the document (domain, format, key topics)
- Break the task into smaller steps (first just summarize, then list entities)
- Review `schema/page_templates/source.md` to ensure it's clear

### "Too many orphan pages"

If the linter reports many orphaned pages, consider:
- Are they truly unused, or is the index incomplete?
- Should they be moved to a "draft" or "archived" directory?
- Do they need to be merged with related pages?

### "How do I handle contradictions?"

Use the contradiction section of a page:

```markdown
## Contradictions / Tensions

- [[source-a]] claims X happened in 2020
- [[source-b]] claims X happened in 2022
- Current interpretation: Unclear; may reflect different definitions
- Confidence: low
```

Record the disagreement. Don't hide it or smooth it over.

## Suggested next steps

1. **Add 5–10 real documents** to build momentum and test workflows
2. **Refine templates** based on what you learn — update `schema/page_templates/` as needed
3. **Test edge cases** — duplicate detection, contradiction handling, citation discipline
4. **Only add search/database when needed** — the simple approach scales further than expected

## Git hygiene

Initialize a git repo and commit early and often:

```bash
git init
git add .
git commit -m "Initial LLM wiki starter scaffold"

# After each ingest:
git add wiki/ raw/manifests/
git commit -m "ingest: <source-title> — <one-line summary>"
```

**Version history is part of the product.** Your wiki is not just content; it's a maintained codebase of knowledge. The git log tells the story of how the wiki evolved.

## Further reading

- **`schema/AGENTS.md`** — detailed operating rules for LLM agents
- **`schema/conventions.md`** — frontmatter, naming, and citation conventions
- **`schema/workflows.md`** — deep dive into ingest, query, and lint workflows
- **`schema/page_templates/`** — full templates for each page type

---

**Made for knowledge work that compounds over time.**
