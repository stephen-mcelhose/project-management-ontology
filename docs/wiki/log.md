# Wiki Log

<!-- Append-only. Never rewrite or delete entries. -->

## [2024-08-22] init | Wiki initialized with AGENTS.md, index.md, and log.md

## [2024-08-22] ingest | 11 pages written from web fetch + user research note

Sources ingested:
- from-url-prov-o.md → prov-o.md
- from-url-doap.md → doap.md
- from-url-dublin-core.md → dublin-core.md
- from-url-foaf.md → foaf.md
- from-url-schema-org-project.md → schema-org-project.md
- from-url-proj-ontology.md → proj-ontology.md
- from-url-promont-ontology.md → promont-ontology.md
- from-url-seon-spmo.md → seon-spmo.md
- from-url-projectco-ontology.md → projectco-ontology.md
- from-url-pmbok-owl-ip.md → pmbok-owl-ip.md
- initial-research-user.md → (cross-referenced in candidate pages)
- okf-frontmatter.md written from llm-wiki skill spec + Dublin Core mapping

## [2026-08-23] lint | 11 pages checked, 3 issues found, 2 fixed

Pages audited: prov-o, doap, dublin-core, foaf, schema-org-project, proj-ontology, promont-ontology, seon-spmo, projectco-ontology, pmbok-owl-ip, okf-frontmatter

Fixed:
1. seon-spmo.md — added missing cross-reference to okf-frontmatter.md on "OKF-annotated document templates" (near-orphan resolved)
2. okf-frontmatter.md — corrected inaccurate claim "All files under docs/wiki/*.md" to exclude structural files (AGENTS.md, log.md)

Advisory (human judgment required):
- schema-org-project.md Sources section lists cross-reference pages alongside raw sources — minor convention deviation
- okf-frontmatter.md resource field (https://okfn.org) is loose; OKF frontmatter as used here is a project-level convention, not an official OKFN standard

## [2026-08-23] ingest | Open Knowledge Format (OKF) Specification — Google Cloud Blog

Source: https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing

New pages:
- raw/from-url-okf-google-blog.md — raw source saved
- research/okf-spec.md — new concept page for OKF v0.1 formal specification

Updated pages:
- research/okf-frontmatter.md — corrected resource field (was https://okfn.org, now Google Cloud URL),
  added spec cross-reference, clarified required-vs-optional fields (spec requires only `type`;
  project policy additionally requires `title`, `description`, `timestamp`), updated sources section
- index.md — added okf-spec.md row
