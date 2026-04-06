# Claude Code Implementation Prompt

You are working inside a local repository that implements a persistent markdown knowledge system called an LLM Wiki.

The objective is to make this repo operational, reliable, and pleasant to use for repeated source ingestion and knowledge maintenance.

## First read
Before making changes, read:
- `README.md`
- `schema/AGENTS.md`
- `schema/conventions.md`
- `schema/workflows.md`

## Conceptual model
This is not a “retrieve chunks at question time” system. It is a persistent, cumulative wiki that the LLM maintains over time.

- `raw/` = immutable source of truth
- `wiki/` = maintained knowledge layer
- `schema/` = behavior contract for the agent
- `tools/` = local helper tooling

## Your mission
Improve this repo into a robust starter kit for real use.

## Work to perform

### 1. Review the repository critically
Identify:
- structural weaknesses
- friction in the current workflows
- unclear conventions
- missing automation
- potential duplication / entropy risks

### 2. Upgrade the tooling
Improve or extend the scripts to support:
- source registration
- manifest generation
- source page creation
- index updates
- log appends
- duplicate detection
- lint reporting
- simple search across markdown pages

### 3. Tighten conventions
Refine the schema and templates so the system is less likely to drift into:
- duplicate pages
- vague summaries
- uncited claims
- inconsistent frontmatter
- broken links

### 4. Keep the implementation grounded
Preferred characteristics:
- local-first
- markdown-first
- git-friendly
- minimal dependencies
- readable Python
- practical rather than flashy

## Constraints
- Do not modify raw sources.
- Do not add cloud infrastructure.
- Do not add a vector database in the initial implementation.
- Do not overbuild a search stack before it is needed.

## Output expectations
After making changes, summarize:
- what changed
- why it changed
- remaining risks
- recommended next steps

## Standard of judgment
The result should be a serious working scaffold for a persistent knowledge base, not a thin proof of concept with buzzword perfume.
