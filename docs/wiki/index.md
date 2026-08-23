---
type: concept
title: Wiki Index
description: Catalog of all pages in the process-assistant wiki
timestamp: 2026-08-23T23:07:33Z
tags: [meta, index]
---

# Wiki Index

Links are relative to this file (`docs/wiki/`).

## Reference

| Page                          | Title    | Description                                                                              |
| ----------------------------- | -------- | ---------------------------------------------------------------------------------------- |
| [Glossary](glossary.md)       | Glossary | Canonical definitions for phase, package, agent, orchestrator, gate, manifest, and more |

## Research

| Page                                                          | Title                          | Description                                                                     |
| ------------------------------------------------------------- | ------------------------------ | ------------------------------------------------------------------------------- |
| [PROV-O](research/prov-o.md)                                  | PROV-O                         | W3C provenance ontology — Entity, Activity, Agent model                         |
| [DOAP](research/doap.md)                                      | DOAP                           | Description of a Project vocabulary for software projects                       |
| [Dublin Core Terms](research/dublin-core.md)                  | Dublin Core Terms              | DCTERMS metadata vocabulary for document/artifact annotation                    |
| [FOAF](research/foaf.md)                                      | FOAF                           | Friend of a Friend vocabulary for agents, persons, and organizations            |
| [schema.org Project](research/schema-org-project.md)          | schema.org Project             | schema.org Project class — general-purpose web vocabulary                       |
| [PROJ Ontology](research/proj-ontology.md)                    | PROJ Ontology                  | PROV-O profile for publishing structured project information (candidate base)   |
| [PROMONT Ontology](research/promont-ontology.md)              | PROMONT Ontology               | DIN 69901-grounded PM ontology from AGH University (candidate base)             |
| [SEON / SPMO](research/seon-spmo.md)                          | SEON / SPMO                    | Software Engineering Ontology Network PM module — document mapping focus        |
| [ProjectCO v2.0](research/projectco-ontology.md)              | ProjectCO v2.0                 | Multi-tier core PM ontology by Olsina, Becker, Papa (candidate base)            |
| [PMBOK & OWL — IP Landscape](research/pmbok-owl-ip.md)        | PMBOK & OWL — IP Landscape     | Why there's no open PMBOK OWL and what safe alternatives exist                 |
| [OKF Frontmatter](research/okf-frontmatter.md)                | OKF Frontmatter                | Frontmatter convention used in wiki pages and document templates                |
| [OKF Specification](research/okf-spec.md)                     | OKF Specification              | OKF v0.1 formal spec by Google Cloud — structure, fields, and reference tools  |

## Specs

| Page | Title | Description |
| ---- | ----- | ----------- |
| [Process Agent Spec](../specs/process-agent.md) | Process Agent | RFC 2119 normative spec for the PM process agent (issue #39) |

## Decisions

| Page                                                                   | Title                           | Description                                                                              |
| ---------------------------------------------------------------------- | ------------------------------- | ---------------------------------------------------------------------------------------- |
| [ADR-001: Base Ontology Selection](../adrs/adr-001-base-ontology.md)   | ADR-001: Base Ontology          | Selects PROJ + bespoke `pm:` namespace + DIN 69901 phase taxonomy                       |
| [ADR-002: Phase Agent Prompts](../adrs/adr-002-phase-agent-prompts.md) | ADR-002: Phase Agent Prompts    | Phase prompts are scaffolds; defer mechanics to ADK agent build (issue #39)              |
| [ADR-003: Phase Manifest Pattern](../adrs/adr-003-phase-manifest.md)   | ADR-003: Phase Manifest Pattern | `_manifest.yaml` required per phase; single-read index for agents and orchestrators     |
| [ADR-004: Gate Output Type System](../adrs/adr-004-gate-output-type-system.md) | ADR-004: Gate Output Type System | Seven gate output types (scalar/block/section); named individuals in `pm:GateOutputType`; amendment process |
| [ADR-005: Gate Validation Rules Schema](../adrs/adr-005-gate-validation-rules.md) | ADR-005: Gate Validation Rules | Six `validation_rules:` keys for programmatic gate constraint checking; inventory of ~25 qualifying gates; amendment process |
| [ADR-006: Process Agent Architecture](../adrs/adr-006-process-agent-architecture.md) | ADR-006: Process Agent Architecture | Python + google-adk LlmAgent + env-file auth + JSON session state; LangGraph deferred to spike #65 |
| [ADR-007: Agent Instruction Injection](../adrs/adr-007-instruction-injection.md) | ADR-007: Agent Instruction Injection | Three-layer instruction composition: base mechanics (code) + domain persona (_project-manifest.yaml) + gate context (tool returns) |
| [ADR-008: Project Manifest and Three-Tier Hierarchy](../adrs/adr-008-project-manifest.md) | ADR-008: Project Manifest | `_project-manifest.yaml` as project-level entry point; formalises three-tier hierarchy above ADR-003 phase manifests |
| [ADR-009: Repository rename to process-assistant](../adrs/adr-009-repository-rename.md) | ADR-009: Repository rename | GitHub repo is `process-assistant`; OWL IRIs stay on the historical github.io path |
