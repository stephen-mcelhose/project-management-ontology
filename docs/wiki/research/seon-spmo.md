---
type: concept
title: SEON / SPMO
description: The Software Engineering Ontology Network (SEON) and its Software Project Management Ontology (SPMO) sub-module, developed at UFES Brazil, which formally maps project management documents and processes in software engineering contexts.
timestamp: 2024-08-22T00:00:00Z
resource: http://nemo.inf.ufes.br/seon/
tags: [ontology, software-engineering, project-management, candidate-base]
---

# SEON / SPMO

**SEON** (Software Engineering Ontology Network) is a networked family of ontologies developed by the NEMO research group at the Federal University of Espírito Santo (UFES), Brazil. It provides formal ontological models for software engineering concepts at multiple levels of abstraction.

The **SPMO** (Software Project Management Ontology) is the sub-ontology within SEON dedicated to project management.

## Network Structure

SEON is organized as a layered network rather than a single monolithic ontology:

```
Foundation Ontology (UFO — Unified Foundational Ontology)
    └─ Core Ontologies (reusable cross-domain)
         └─ Domain Ontologies
              └─ SPMO (Software Project Management Ontology)
                   └─ Reference Ontologies (method-specific)
```

This layered design means SPMO concepts are grounded in **UFO** (a well-regarded
foundational ontology from the same UFES group), giving it rigorous philosophical
underpinnings. SEON is originally modeled using **OntoUML** — a UML profile for
conceptual modeling grounded in UFO — before being published as OWL. Practitioners
wishing to extend SPMO directly will need OntoUML-aware tooling (e.g., Menthor
Editor); standard OWL editors work with the published OWL export.

## Key Facts

| Property       | Value                                                      |
| -------------- | ---------------------------------------------------------- |
| Developer      | NEMO Lab, UFES, Brazil                                     |
| Network URL    | http://nemo.inf.ufes.br/seon/                              |
| Namespace      | `http://nemo.inf.ufes.br/seon/domain/spmo`                 |
| Foundation     | UFO (Unified Foundational Ontology)                        |
| Format         | OWL                                                        |
| Domain         | Software engineering project management                    |

## SPMO Coverage

SPMO was explicitly designed to solve the **"semantic documentation" problem** — mapping real-world artifacts (spreadsheets, text files, wiki entries) to formal project management concepts. Key concepts covered:

- **Project** and **Project Phase**
- **Process** — software development processes (Agile, Waterfall, etc.)
- **Activity** and **Task** — with effort estimation
- **Corrective Action Register** — tracking deviations
- **Cost Estimated Process** — budget planning
- **Resource** — human and material
- **Role** — project manager, team member, stakeholder
- **Work Product / Artifact** — deliverables with defined acceptance criteria
- **Schedule** — planned vs actual timeline tracking

## Unique Strength: Document Mapping

SPMO's distinguishing feature is its explicit mapping between formal ontology classes and real-world PM documents:

| Document type             | SPMO concept                        |
| ------------------------- | ----------------------------------- |
| Project plan              | `Project`, `Phase`, `Schedule`      |
| Sprint backlog            | `Task`, `Activity`, `WorkProduct`   |
| Risk register             | `RiskItem`, `CorrectiveAction`      |
| Resource plan             | `Resource`, `Allocation`            |
| Cost estimate             | `CostEstimatedProcess`              |

This makes SEON/SPMO highly relevant to our goal of creating [OKF-annotated document templates](okf-frontmatter.md) that map to ontology terms.

## Suitability as a Base

| Criterion                | Assessment                                                              |
| ------------------------ | ----------------------------------------------------------------------- |
| Open / freely available  | ✅ Open, academic                                                       |
| Foundational grounding   | ✅ UFO — rigorous philosophical basis                                   |
| Document mapping focus   | ✅ Explicitly solves the semantic documentation problem                 |
| Software engineering bias| ⚠️ Heavily SW-focused; less suited to non-technical PM                 |
| Linked data / PROV-O fit | ⚠️ Uses UFO, not PROV-O; bridging needed                               |
| Downloadable TTL/OWL     | ⚠️ Available via UFES but requires registration/access                 |

**Verdict**: The most directly relevant to our *document template* goal among all candidates. The document-to-ontology mapping work already done in SPMO is directly reusable. However, its software engineering bias means we'd need to generalize for non-software PM contexts.

> **Adopted pattern**: The document-to-phase mapping pattern from SEON/SPMO was adopted directly — each [template pack](../glossary.md#template-pack) carries a `pm:producedInPhase` annotation linking it to a [phase](../glossary.md#phase) individual. SEON/SPMO was not imported as a dependency. See [ADR-001](../../adrs/adr-001-base-ontology.md).

## Relationship to Other Candidates

- More document-oriented than [PROMONT Ontology](promont-ontology.md) or [PROJ Ontology](proj-ontology.md)
- Stronger foundational grounding (UFO) than [ProjectCO v2.0](projectco-ontology.md)
- SW-specific scope narrows general applicability vs [PROJ Ontology](proj-ontology.md)
- Bridging to [PROV-O](prov-o.md) needed for provenance tracking

## Sources

- [raw source](../raw/from-url-seon-spmo.md) — http://nemo.inf.ufes.br/seon/
- [initial research](../raw/initial-research-user.md)
