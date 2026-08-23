# Wiki Schema

This wiki is maintained by an LLM using the llm-wiki skill
(https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

## Domain

This wiki covers the **Project Management Ontology** project — a formal Turtle/OWL ontology
for project management concepts with document templates and workflow generation tooling.

Topics covered:
- Base ontologies (PROV-O, DOAP, schema.org, Dublin Core, FOAF) and how they are reused
- Ontology design decisions (class hierarchy, property axioms, SHACL shapes)
- Visualization tooling (Widoco, OWLViz, RDFLib, Graphviz)
- OKF frontmatter spec and how it applies to document templates
- Document template patterns (project charter, risk register, RACI matrix, etc.)
- Workflow generation from ontology instances
- Lessons learned / ADRs

## Directory Layout

```
docs/wiki/
  AGENTS.md          ← this file
  index.md           ← catalog of all pages
  log.md             ← append-only operation log
  raw/               ← immutable source files (URLs, notes, paste)
  research/          ← concept pages distilled from research sources
  decisions/         ← ADRs and architectural decisions
  how-to/            ← step-by-step procedural guides
```

New pages go in the subdirectory matching their `type`. Fall back to the wiki root only if no subdirectory fits.

## Conventions

- **Page slugs**: kebab-case filenames placed in the appropriate subdirectory (e.g., `research/prov-o.md`, `decisions/adr-001-base-ontology.md`)
- **Frontmatter**: OKF — `type` (default `concept`), `title`, `description`, `timestamp` (ISO-8601 UTC); optional `resource`, `tags`
- **Cross-references**: standard relative markdown links — `[Title](relative/path/to/page.md)`. Paths are relative to the linking file. Never use `[[wikilinks]]`.
- **Sources section**: every page ends with `## Sources` listing its raw inputs

## Operations

Run these via the `llm-wiki` skill:

- `ingest <source>` — read a new source, write a summary page, propagate to related pages
- `query <question>` — synthesize an answer from wiki pages, optionally write back
- `lint` — audit for orphans, contradictions, stale claims, missing links

## Raw Sources

Raw source files live in `raw/`. They are immutable — the LLM reads them but never writes to them.

## index.md

Structured catalog of all wiki pages. Links use paths relative to the wiki root. Updated on every write operation.

## log.md

Append-only chronological log. Format: `## [YYYY-MM-DD] operation | detail`
