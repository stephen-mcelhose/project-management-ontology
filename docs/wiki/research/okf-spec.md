---
type: concept
title: Open Knowledge Format (OKF) Specification
description: The OKF v0.1 open specification by Google Cloud that formalizes the LLM-wiki pattern into a vendor-neutral, agent-readable directory of Markdown files with YAML frontmatter.
resource: https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing
tags: [okf, specification, metadata, llm, knowledge-management]
timestamp: 2026-08-23T05:58:04Z
---

# Open Knowledge Format (OKF) Specification

The **Open Knowledge Format (OKF)** v0.1 is an open specification published by Google Cloud's Data Cloud engineering team in June 2026. It formalizes the ["LLM-wiki" pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) into a portable, vendor-neutral standard for representing metadata, context, and curated knowledge that AI agents and foundation models need to produce accurate, actionable results.

This project's [OKF frontmatter convention](okf-frontmatter.md) predated the formal spec and aligns closely with it — the spec validates the approach already in use here, with one important clarification on field requirements (see below).

## Core Problem: Context Assembly

AI agents require institutional context (schemas, metric definitions, runbooks, join paths, API changes) to do complex work. In most organizations this context is fragmented across metadata catalogs, wikis, code comments, and engineers' heads. OKF solves the **context-assembly problem** by giving agents a shared, unified, evolving library. It is a **format, not a service** — no proprietary SDK, no cloud platform lock-in.

## Structure

An OKF bundle is a directory where each concept (a database table, a metric, a playbook, an API endpoint) gets its own Markdown file with YAML frontmatter. Relationships between concepts are expressed as standard Markdown hyperlinks, turning the directory into a rich relationship graph rather than a flat hierarchy.

```
sales/
├── index.md          ← progressive disclosure for agents navigating the folder
├── tables/
│   ├── orders.md
│   └── customers.md
└── metrics/
    └── weekly_active_users.md
```

Two files are **reserved by the spec**:
- `index.md` — catalog / progressive disclosure entry point for each directory level
- `log.md` — append-only chronological history of changes

This wiki already follows both conventions exactly.

## Field Specification (v0.1)

| Field         | Required?    | Description                                              |
| ------------- | ------------ | -------------------------------------------------------- |
| `type`        | **REQUIRED** | Kind of concept (e.g. `concept`, `BigQuery Table`, `API`) |
| `title`       | optional     | Human-readable name of the concept                       |
| `description` | optional     | One-sentence summary                                     |
| `resource`    | optional     | URI linking to the canonical platform resource           |
| `tags`        | optional     | Array of keyword strings                                 |
| `timestamp`   | optional     | ISO 8601 UTC datetime of creation or last update         |

> **Note for this project**: Our [OKF frontmatter](okf-frontmatter.md) convention treats `title`, `description`, and `timestamp` as required for wiki pages. This is a **stricter local policy** on top of the v0.1 spec minimum, which only mandates `type`. Both are valid — the spec is intentionally "minimally opinionated" to maximize adoption; our policy adds rigor for knowledge quality.

## Why Markdown + YAML?

- **Human-writable**: No schema tools or code generation required
- **Agent-readable**: LLMs parse Markdown natively without structured query engines
- **Version-control friendly**: Lives in Git alongside code; changes tracked via PR/review
- **Producer/consumer independent**: Human-written bundles are readable by AI agents and vice versa

## Relation to Existing Vocabularies

OKF does not replace semantic vocabularies like [PROV-O](prov-o.md), [Dublin Core](dublin-core.md), or [DOAP](doap.md). Instead, it provides the **document envelope** (frontmatter + Markdown) that wraps content derived from those vocabularies. The `resource` field can point to a URI minted by any of these vocabularies, and the `type` field can use terms from any controlled vocabulary.

In practice:
- `dcterms:title` maps to OKF `title`
- `dcterms:description` maps to OKF `description`
- `dcterms:created` maps to OKF `timestamp`
- `dcterms:subject` maps to OKF `tags`

(See [OKF frontmatter](okf-frontmatter.md) for the full mapping table.)

## Reference Implementations (v0.1)

1. **Enrichment Agent** — scans a BigQuery dataset, drafts OKF concept docs for every table/view, then enriches with join paths and citations via a second LLM pass
2. **Static HTML Visualizer** — single self-contained file (no backend), renders any OKF folder as an interactive graph in-browser
3. **Sample datasets** — pre-packaged OKF bundles for GA4 e-commerce, Stack Overflow, and Bitcoin datasets (GitHub)
4. **Google Cloud Knowledge Catalog** — updated to natively ingest OKF bundles for internal and external AI agents

## Sources

- [raw source](../raw/from-url-okf-google-blog.md) — https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing
