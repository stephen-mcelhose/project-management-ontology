---
type: concept
title: ProjectCO v2.0
description: The Project Management Core Ontology (ProjectCO) v2.0 by Olsina, Becker, and Papa — a multi-tier architectural ontology mapping organizational entities to project attributes including tasks, resources, assignments, and temporal constraints.
timestamp: 2024-08-22T00:00:00Z
resource: https://www.researchgate.net
tags: [ontology, project-management, core-ontology, candidate-base]
---

# ProjectCO v2.0

**ProjectCO v2.0** (Project Management Core Ontology) is an academic ontology published by Luis Olsina, Pablo Becker, and María Fernanda Papa (GIDIS_Web research group). It is available on ResearchGate and aims to provide a reusable, multi-tier core vocabulary for project management that organizations can extend.

## Design Philosophy

ProjectCO takes a **core ontology** approach — it defines the minimal, domain-independent concepts that any project management scenario requires, leaving domain-specific concepts to extension ontologies. The "v2.0" designation reflects a second generation with refined class relationships and clearer separation of tiers.

The architecture has three tiers:

1. **Upper tier** — foundational concepts (Entity, Agent, Goal, Process)
2. **Core tier** — PM-specific (Project, Task, Milestone, Resource, Assignment)
3. **Domain tier** — specializations for IT, construction, research, etc.

## Key Facts

| Property       | Value                                              |
| -------------- | -------------------------------------------------- |
| Authors        | Luis Olsina, Pablo Becker, María Fernanda Papa     |
| Group          | GIDIS_Web, Universidad Nacional de La Pampa        |
| Published      | ResearchGate (paper + ontology file)               |
| Version        | 2.0                                                |
| Format         | OWL (Protégé-compatible)                           |

## Core Classes

| Class           | Description                                                  |
| --------------- | ------------------------------------------------------------ |
| `Project`       | A bounded initiative with goals, scope, and timeline         |
| `Goal`          | An objective the project aims to achieve                     |
| `Phase`         | A named temporal stage within the project                    |
| `Task`          | A unit of work; may be decomposed via WBS                    |
| `Milestone`     | A significant checkpoint marking phase/task completion       |
| `Resource`      | Any asset (human, material, financial) used in the project   |
| `Assignment`    | Reification of a resource assigned to a specific task        |
| `WorkProduct`   | An output or deliverable produced by tasks                   |
| `Risk`          | An uncertain event affecting project objectives              |
| `Constraint`    | Temporal, resource, or budget limits on tasks or the project |

## Key Properties

| Property              | Domain        | Range         | Description                         |
| --------------------- | ------------- | ------------- | ----------------------------------- |
| `hasGoal`             | Project       | Goal          | Project objectives                  |
| `hasPhase`            | Project       | Phase         | Lifecycle phases                    |
| `hasTask`             | Phase/Project | Task          | Work decomposition                  |
| `dependsOn`           | Task          | Task          | Predecessor dependency              |
| `assignedTo`          | Assignment    | Task          | Task receiving the resource         |
| `assignedResource`    | Assignment    | Resource      | Resource being allocated            |
| `startDate`/`endDate` | Task/Phase    | xsd:date      | Temporal bounds                     |
| `estimatedEffort`     | Task          | xsd:decimal   | Effort in person-hours              |
| `hasRisk`             | Project/Task  | Risk          | Associated risks                    |
| `produces`            | Task          | WorkProduct   | Output deliverable                  |

## WBS Support

ProjectCO explicitly supports **Work Breakdown Structure** decomposition: a `Task` can contain sub-tasks recursively, and the hierarchy maps to standard WBS numbering schemes. This is more explicit than [PROJ Ontology](proj-ontology.md) and [PROMONT Ontology](promont-ontology.md).

## Suitability as a Base

| Criterion                | Assessment                                                             |
| ------------------------ | ---------------------------------------------------------------------- |
| Open / freely available  | ✅ Academic, ResearchGate                                              |
| IP-clean                 | ✅ Original academic work, not PMBOK-derived                           |
| Core class coverage      | ✅ Strong — Project, Task, Milestone, Resource, Assignment, Risk       |
| WBS support              | ✅ Explicit hierarchical task decomposition                            |
| Linked data / PROV-O fit | ⚠️ Not a PROV-O profile; bridging needed                              |
| Foundational grounding   | ⚠️ Uses generic upper ontology concepts, not UFO or BFO               |
| Active maintenance       | ⚠️ Academic publication; no known active community                    |

**Verdict**: The most operationally complete of the four candidates. Its explicit WBS, Assignment reification, and Risk model align well with standard PM practice. Primary gap is the absence of a [PROV-O](prov-o.md) or foundational ontology anchor, which would need to be bridged for linked-data compatibility.

## Relationship to Other Candidates

- More complete operationally than [PROJ Ontology](proj-ontology.md) (publication-only)
- More domain-neutral than [SEON/SPMO](seon-spmo.md) (SW-specific)
- Similar operational scope to [PROMONT Ontology](promont-ontology.md) but with cleaner published documentation
- Needs explicit [PROV-O](prov-o.md) bridge for provenance/linked-data interop

## Sources

- [raw source](../raw/from-url-projectco-ontology.md) — https://www.researchgate.net
- [initial research](../raw/initial-research-user.md)
