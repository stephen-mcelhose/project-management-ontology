---
type: concept
title: PROJ Ontology
description: A PROV-O profile designed to publish structured information about projects — their goals, milestones, funding, stakeholders, and activities.
timestamp: 2024-08-22T00:00:00Z
resource: http://linked.data.gov.au/def/project
tags: [ontology, project-management, prov-o, candidate-base]
---

# PROJ Ontology

**PROJ** is a profile of [PROV-O](prov-o.md) developed by Simon Cox (CSIRO Australia) and registered on [BioPortal](https://bioportal.bioontology.org/ontologies/PROJ). It is one of the most mature open ontologies expressly designed to describe *project information* — as opposed to managing projects operationally.

## Key Facts

| Property       | Value                                                  |
| -------------- | ------------------------------------------------------ |
| Namespace      | `http://linked.data.gov.au/def/project`                |
| BioPortal      | https://bioportal.bioontology.org/ontologies/PROJ      |
| Version        | 2020 (uploaded BioPortal 2021)                         |
| Extends        | [PROV-O](prov-o.md) (W3C PROV Ontology)                         |
| Classes        | 46                                                     |
| Properties     | 58                                                     |
| Individuals    | 109                                                    |
| Author         | Simon Cox, CSIRO Australia                             |

## Design Philosophy

PROJ is **domain-neutral by intention** — it describes projects in the abstract and expects downstream ontologies to specialize or extend it. It explicitly states it is *not* designed to support project management operations (scheduling, resource allocation), but rather to *publish* structured information about projects for discovery and linking.

This makes it an excellent **upper layer** to build a more operational PM ontology on top of, rather than a complete solution on its own.

## What It Covers

- **Project planning** — goals, phases, timelines
- **Funding** — funding bodies, grant information
- **Project stakeholders and relationships** — sponsors, participants
- **Project activities and timeline** — modeled as `prov:Activity` subclasses
- **Project outcomes** — deliverables as `prov:Entity` subclasses

## Relationship to PROV-O

PROJ is built directly on [PROV-O](prov-o.md)'s tripartite model:

```
prov:Entity      → project deliverables, documents, datasets
prov:Activity    → project phases, tasks, experiments
prov:Agent       → project managers, teams, funding bodies
```

Provenance chains (`wasGeneratedBy`, `used`, `wasDerivedFrom`) naturally express how deliverables emerge from project activities.

## Suitability as a Base for This Project

| Criterion               | Assessment                                                                       |
| ----------------------- | -------------------------------------------------------------------------------- |
| Open / freely available | ✅ Yes — CC licensed, downloadable from BioPortal                                |
| Extends well-known W3C  | ✅ PROV-O                                                                        |
| Covers core PM concepts | ⚠️ Partial — publication-focused, not operational scheduling/tracking            |
| Active maintenance      | ⚠️ Last updated 2020                                                             |
| Machine-readable (TTL)  | ✅ Available as OWL/RDF from BioPortal                                           |
| Community adoption      | ⚠️ Niche — primarily Australian government linked data context                   |

**Verdict**: Strong candidate as an *upper ontology layer* to inherit from. Needs extension with operational PM concepts (task status, risk, RACI, etc.).

> **Decision**: PROJ was selected as the provenance backbone for this project. A bespoke `pm:` operational namespace was added on top, structured by DIN 69901 process groups. See [ADR-001: Base Ontology Selection](../../adrs/adr-001-base-ontology.md).

## Sources

- [raw source](../raw/from-url-proj-ontology.md) — https://bioportal.bioontology.org/ontologies/PROJ
- [initial research](../raw/initial-research-user.md)
