---
type: concept
title: OKF Frontmatter
description: The Open Knowledge Format frontmatter convention for annotating Markdown documents with structured metadata fields used by the llm-wiki skill.
timestamp: 2024-08-22T00:00:00Z
resource: https://okfn.org
tags: [okf, frontmatter, metadata, wiki, convention]
---

# OKF Frontmatter

**OKF frontmatter** is a YAML metadata block placed at the top of Markdown files (between `---` delimiters) following the conventions of the Open Knowledge Foundation and the [llm-wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) skill pattern. Every document template and wiki page in this project uses it.

## Required Fields

| Field         | Type            | Description                                              | Example                              |
| ------------- | --------------- | -------------------------------------------------------- | ------------------------------------ |
| `type`        | controlled vocab | The kind of document this page is                       | `concept`                            |
| `title`       | string          | Human-readable name of the page                         | `"Project Charter"`                  |
| `description` | string          | One-sentence summary                                     | `"Authorizes a project..."`          |
| `timestamp`   | ISO-8601 UTC    | Creation or last-updated time                            | `2024-08-22T00:00:00Z`               |

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

| OKF field     | Dublin Core equivalent      |
| ------------- | --------------------------- |
| `title`       | `dcterms:title`             |
| `description` | `dcterms:description`       |
| `timestamp`   | `dcterms:created`           |
| `type`        | `dcterms:type`              |
| `resource`    | `dcterms:relation`          |
| `tags`        | `dcterms:subject`           |

## Usage in This Project

All files under `docs/wiki/*.md` and `docs/templates/*.md` carry OKF frontmatter. The `llm-wiki` skill enforces its presence during lint passes and ingestion.

## Sources

- [raw source](../raw/from-url-pmbok-owl-ip.md) (OKF referenced tangentially)
- llm-wiki skill definition — `~/.config/csgdaa-code/skills/llm-wiki/skill.md`
