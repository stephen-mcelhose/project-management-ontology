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

## [2026-08-23] ingest | Glossary — canonical term definitions

New pages:
- glossary.md — canonical definitions for phase, package, agent, orchestrator, gate, manifest, shared context, template pack, phase transition, document class, SHACL shape, phase local order, package agent prompt, phase agent prompt

Updated pages:
- index.md — added Reference section with glossary entry; added Decisions section with ADR-001, ADR-002, ADR-003

## [2026-08-23] lint | 14 pages checked, 6 issues found, 5 fixed

Fixed:
1. proj-ontology.md — added Decision callout noting PROJ was selected (ADR-001); stale "verdict" now has follow-through
2. promont-ontology.md — added Decision callout noting DIN 69901 adopted as phase taxonomy (ADR-001); glossary cross-reference added
3. schema-org-project.md — separated comparison vocabulary links into a ## See Also section; Sources now contains only raw sources (convention fix from prior lint advisory)
4. seon-spmo.md — added Decision callout noting document-to-phase mapping pattern adopted; glossary cross-references added
5. index.md — ADR-001, ADR-002, ADR-003 added to Decisions section (were index gaps)

Advisory (no fix needed):
- glossary.md uses `type: reference` which is not in the project's documented type vocabulary (`concept | how-to | decision | runbook | proposal | spike`). `reference` is a reasonable extension and not a spec violation; document as an accepted type in AGENTS.md if the pattern recurs.

## [2026-08-24] ingest | ADR-004: Gate Output Type System

New decision indexed:
- ADR-004 added to index.md Decisions section
- Defines seven gate output types (string, date, identifier, prose, list, table, section) as pm:GateOutputType OWL named individuals

## [2026-08-24] ingest | ADR-005: Gate Validation Rules Schema

New decision indexed:
- ADR-005 added to index.md Decisions section
- Defines six validation_rules: keys for programmatic gate constraint checking
- Inventory of ~25 qualifying gates across all phases documented in ADR

## [2026-08-24] lint | 14 pages checked, 2 issues found, 2 fixed

Pages checked: all 12 research pages, glossary.md, index.md (AGENTS.md, log.md, raw/ excluded as structural/immutable)

Fixed:
1. glossary.md / Gate entry — stale: missing type, deferred_value, validation_rules fields added in M3; updated with all current gate fields and cross-references to ADR-004 and ADR-005
2. glossary.md / Sources — added ADR-004, ADR-005, M3 session citation

Advisory (no fix needed):
- ADR-004 and ADR-005 live in docs/adrs/ (outside wiki root) — correctly indexed via relative links in index.md; no action required

## [2026-08-23] lint | Extensive wiki review — industry accuracy, deep dives, structural drift

Pages reviewed: all 13 research pages, glossary.md, index.md, AGENTS.md, log.md

### Highs fixed (2 of 3 — 1 was a false alarm)

1. **glossary.md / Gate** — added "Not to be confused with" note distinguishing this
   project's use of "gate" (a template field-filling step) from the PM industry's
   "phase gate / stage gate" (Cooper's Stage-Gate® model — a formal Go/No-Go
   review checkpoint between phases).
2. **okf-frontmatter.md + okf-spec.md / resource field mapping** — corrected
   `dcterms:relation` (too broad: "a related resource") to `foaf:primaryTopic`
   (semantically correct: "the document is primarily about this URI"). No DCTERMS
   equivalent exists; FOAF is the right namespace. Notes column added to mapping table.
3. ~~schema-org-project.md / FundingAgency hierarchy~~ — verified correct via
   schema.org: FundingAgency IS a subclass of Project. No fix needed.

### Mediums fixed (9)

4. **glossary.md / Package** — added "Not to be confused with: WBS work package"
   distinction.
5. **glossary.md / Output Status** — new entry added defining `pending`, `draft`,
   and `approved` values with cross-reference to Phase Transition.
6. **AGENTS.md / type vocabulary** — added `reference` as a documented valid type
   for catalog/index pages (resolves 2026-08-23 lint advisory).
7. **AGENTS.md / structural drift** — removed non-existent `decisions/` and
   `how-to/` subdirectories from the directory layout. ADRs correctly documented
   as living in `docs/adrs/` (outside the wiki, indexed via `index.md`). Page slug
   convention updated accordingly.
8. **prov-o.md** — added "Usage in This Project" section clarifying PROV-O is used
   indirectly via the PROJ profile; raw `prov:` terms may not appear in Turtle files.
   Added PROJ Ontology to Related Vocabularies.
9. **promont-ontology.md** — softened "legally unambiguous to build upon" →
   "safe to model against — DIN 69901 concepts are not tied to any proprietary
   framework." Changed "Open source" → "Academically available (no formal
   open-source license)."
10. **seon-spmo.md** — added OntoUML note: SEON is originally modeled in OntoUML
    (a UML profile grounded in UFO) before being published as OWL; practitioners
    extending SPMO need OntoUML-aware tooling.
11. **pmbok-owl-ip.md** — four fixes:
    - SNOMED CT changed from "✅ Open / licensed" to "⚠️ Member-country licensed"
      with explanatory blockquote and snomed.org/licensing reference.
    - ISO 21500 updated to ISO 21502 (successor standard; consistent with project
      templates which already cite ISO 21502:2020).
    - Axelos updated to "PeopleCert (formerly Axelos, acquired 2021)".
    - Dead keet.wordpress.com attribution defused: "Researchers (including
      commentary previously at keet.wordpress.com — now offline)" replaces the
      unverifiable Vidal attribution.
12. **foaf.md** — added spec status blockquote noting `foaf:currentProject` and
    `foaf:pastProject` carry `term_status: testing` in the FOAF 0.1 spec; caution
    advised in production linked data.

### Issues filed for further research

- #51 — wiki: update PROMONT URL to ontology-specific resource
- #52 — wiki: verify SNOMED CT member country count in pmbok-owl-ip.md
- #53 — wiki: audit foaf:currentProject usage in ontology — term_status:testing
