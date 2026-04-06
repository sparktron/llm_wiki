# Codex Implementation Prompt

You are implementing a local, markdown-first “LLM Wiki” knowledge system inside this repository.

## Goal
Build and refine a persistent wiki that sits between immutable raw sources and downstream user queries. The wiki accumulates synthesis over time. It is not a generic chat RAG system.

## Repository model
- `raw/` contains immutable source files.
- `wiki/` contains agent-maintained markdown pages.
- `schema/AGENTS.md` defines operating rules.
- `tools/` contains helper scripts.

## Your responsibilities
1. Read and follow `schema/AGENTS.md`, `schema/conventions.md`, and `schema/workflows.md`.
2. Preserve the invariant that raw sources are never modified.
3. Improve the repo with pragmatic, local-first tooling.
4. Keep everything markdown-first and git-friendly.
5. Avoid overengineering.

## Immediate tasks

### Task 1 — Audit the scaffold
Inspect the repo and report:
- missing pieces
- design weaknesses
- likely failure modes
- implementation opportunities

### Task 2 — Improve helper tooling
Enhance the starter scripts in `tools/` with:
- better source registration
- safer path handling
- optional source type metadata
- index update helpers
- log append helpers
- duplicate detection support

### Task 3 — Add a higher-quality ingest flow
Implement a workflow that makes it easy for an agent to:
- register a source
- create or update a source page
- identify impacted wiki pages
- update `wiki/index.md`
- append an operation to `wiki/log.md`

### Task 4 — Add stronger linting
Expand lint checks for:
- orphan pages
- dead links
- duplicate titles
- likely duplicate concepts
- missing required sections
- pages with low citation density
- stale pages based on `updated` dates

### Task 5 — Improve search
Keep it local and simple. Add a pragmatic markdown search layer with:
- title boosts
- frontmatter awareness
- snippet output
- optional regex mode if easy

## Constraints
- Do not add a database unless truly necessary.
- Do not add a vector store in the first pass.
- Do not add web frameworks or cloud dependencies.
- Keep dependencies minimal.
- Prefer Python standard library unless a package is clearly justified.
- Keep code readable, typed where useful, and well-commented.

## Deliverables
When finished, provide:
1. a summary of changes made
2. a list of key design decisions
3. a list of remaining weaknesses
4. suggested next implementation steps

## Editing behavior
- Make concrete changes directly in the repo.
- Prefer small coherent commits if git usage is appropriate.
- If a convention is weak, improve the convention file too.
- If you discover a better folder structure, update carefully and explain why.

## Quality bar
This system should feel like a disciplined knowledge-maintenance tool, not a toy demo. Optimize for long-term maintainability, clarity, and operational usefulness.
