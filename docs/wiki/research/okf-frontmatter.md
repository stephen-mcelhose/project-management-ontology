---
type: concept
title: OKF Frontmatter
description: The Open Knowledge Format frontmatter convention for annotating Markdown documents with structured metadata fields used by the llm-wiki skill.
timestamp: 2024-08-22T00:00:00Z
resource: https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing
tags: [okf, frontmatter, metadata, wiki, convention]
---

# OKF Frontmatter

**OKF frontmatter** is a YAML metadata block placed at the top of Markdown files (between `---` delimiters) following the [Open Knowledge Format specification](okf-spec.md) and the [llm-wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) skill pattern. Every document template and wiki page in this project uses it.

The OKF v0.1 spec (published June 2026 by Google Cloud) formally defines this convention — see [OKF Specification](okf-spec.md) for full details. The spec designates only `type` as strictly required; this project applies a stricter local policy requiring `title`, `description`, and `timestamp` as well for knowledge quality.

## Required Fields

The [OKF v0.1 spec](okf-spec.md) only mandates `type`. This project requires four fields for knowledge quality:

| Field         | Type             | Description                                              | Example                              |
| ------------- | ---------------- | -------------------------------------------------------- | ------------------------------------ |
| `type`        | controlled vocab | The kind of document this page is (**spec required**)    | `concept`                            |
| `title`       | string           | Human-readable name of the page (**project required**)   | `"Project Charter"`                  |
| `description` | string           | One-sentence summary (**project required**)              | `"Authorizes a project..."`          |
| `timestamp`   | ISO-8601 UTC     | Creation or last-updated time (**project required**)     | `2024-08-22T00:00:00Z`               |

## Optional Fields

| Field      | Type         | Description                                   | Example                                      |
| ---------- | ------------ | --------------------------------------------- | -------------------------------------------- |
| `resource` | URI          | The primary external resource this page maps to | `http://linked.data.gov.au/def/project`    |
| `tags`     | list         | Free-form classification tags                 | `[ontology, prov-o, candidate-base]`         |

## Valid `type` Values

| Value       | When to use                                                             |
| ----------- | ----------------------------------------------------------------------- |
| `concept`   | Explanatory page about an idea, term, or technology (default)          |
| `how-to`    | Step-by-step procedural instructions                                    |
| `decision`  | An architectural decision record (ADR)                                  |
| `runbook`   | Operational guide for running/maintaining something                     |
| `proposal`  | A draft idea not yet decided                                            |
| `spike`     | Time-boxed research into an unknown                                     |
| `template`  | A reusable document skeleton with fill-in-the-blank sections            |

## Example

```yaml
---
type: concept
title: PROV-O
description: The W3C provenance ontology used as the foundational layer for the PROJ profile.
timestamp: 2024-08-22T00:00:00Z
resource: http://www.w3.org/ns/prov#
tags: [vocabulary, rdf, provenance, w3c]
---
```

## Relationship to Dublin Core

OKF frontmatter fields map closely to [Dublin Core](dublin-core.md) properties:

| OKF field     | Closest equivalent                        | Notes                                                   |
| ------------- | ----------------------------------------- | ------------------------------------------------------- |
| `title`       | `dcterms:title`                           | Direct match                                            |
| `description` | `dcterms:description`                     | Direct match                                            |
| `timestamp`   | `dcterms:created`                         | Direct match                                            |
| `type`        | `dcterms:type`                            | Direct match                                            |
| `resource`    | `foaf:primaryTopic`                       | No DCTERMS equivalent; `foaf:primaryTopic` expresses "this document is primarily about this URI" — `dcterms:relation` (generic "related resource") is too broad |
| `tags`        | `dcterms:subject`                         | Direct match                                            |

## Usage in This Project

All concept and research pages in `docs/wiki/` and templates in `docs/templates/` carry OKF frontmatter. Structural files (`AGENTS.md`, `log.md`) are exempt. The `llm-wiki` skill enforces its presence during lint passes and ingestion.

## Sources

- [raw source](../raw/from-url-okf-google-blog.md) — https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing
- llm-wiki skill definition — local skill config (`skills/llm-wiki/skill.md`)
- [OKF Specification](okf-spec.md) — full spec page with field details and reference implementations
