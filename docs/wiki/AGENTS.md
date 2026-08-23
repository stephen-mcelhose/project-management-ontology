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

## Conventions

- **Page slugs**: kebab-case, flat — all pages live directly in `docs/wiki/`, never in subdirectories
- **Frontmatter**: OKF — `type` (default `concept`), `title`, `description`, `timestamp` (ISO-8601 UTC); optional `resource`, `tags`
- **Cross-references**: `[[slug]]` wikilinks — slug is the filename without `.md`. Never use directory prefixes.
- **Sources section**: every page ends with `## Sources` listing its raw inputs

## Operations

Run these via the `llm-wiki` skill:

- `ingest <source>` — read a new source, write a summary page, propagate to related pages
- `query <question>` — synthesize an answer from wiki pages, optionally write back
- `lint` — audit for orphans, contradictions, stale claims, missing links

## Raw Sources

Raw source files live in `docs/wiki/raw/`. They are immutable — the LLM reads them but never writes to them.

## index.md

Structured catalog of all wiki pages. Updated on every write operation.

## log.md

Append-only chronological log. Format: `## [YYYY-MM-DD] operation | detail`
