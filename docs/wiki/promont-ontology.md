---
type: concept
title: PROMONT Ontology
description: A project management ontology developed at AGH University (Krakow) grounded in the German DIN 69901 project management standard, designed to bridge semantic web services and business process management.
timestamp: 2024-08-22T00:00:00Z
resource: https://ai.ia.agh.edu.pl
tags: [ontology, project-management, din-69901, candidate-base]
---

# PROMONT Ontology

**PROMONT** (Project Management ONTology) is an open-source reference ontology from the Department of Applied Computer Science at AGH University of Science and Technology, Krakow, Poland. It was developed to formally represent project management lifecycle concepts and bridge semantic web services with physical business process management.

## Origin and Standard Grounding

Unlike ontologies that derive from PMBOK (which is IP-restricted — see [[pmbok-owl-ip]]), PROMONT is grounded in **DIN 69901**, the German Institute for Standardization's project management standard. DIN 69901 is itself a comprehensive, openly referenceable standard covering:

- Project definitions and lifecycle
- Process groups (initiation, planning, execution, monitoring, closure)
- Resource and role concepts
- Schedule and milestone management

This makes PROMONT legally unambiguous to build upon.

## Key Characteristics

| Property        | Value                                                      |
| --------------- | ---------------------------------------------------------- |
| Developer       | AGH University, Krakow (Dept. Applied Computer Science)    |
| Standard basis  | DIN 69901 (German PM standard)                             |
| Primary URL     | https://ai.ia.agh.edu.pl                                   |
| License         | Open source                                                |
| Format          | OWL                                                        |

## Design Focus

PROMONT was built for **semantic middleware** scenarios — specifically:

- Validating task dependencies against document submissions in enterprise systems
- Mapping workflows to decision points, execution steps, and deliverables
- Enabling semantic interoperability between PM tools via shared vocabulary

This operational focus distinguishes it from [[proj-ontology]], which is publication-oriented.

## Core Concept Coverage

Based on DIN 69901 alignment, PROMONT covers:

- **Project** — bounded initiative with goals, timeline, and resources
- **Process groups** — Initiation, Planning, Execution, Monitoring & Control, Closure
- **Activity / Task** — units of work with duration, effort, and dependencies
- **Milestone** — zero-duration reference points in the schedule
- **Resource** — human, material, and financial assets
- **Role** — responsibilities mapped to agents
- **Risk** — uncertain events with probability and impact
- **Deliverable** — outputs produced by activities

## Suitability as a Base

| Criterion                | Assessment                                                             |
| ------------------------ | ---------------------------------------------------------------------- |
| Open / freely available  | ✅ Open source                                                         |
| IP-clean standard basis  | ✅ DIN 69901 (not PMBOK)                                               |
| Operational PM coverage  | ✅ Strong — process groups, tasks, resources, risks                    |
| Linked data / PROV-O fit | ⚠️ Not a PROV-O profile — separate design lineage                      |
| Active maintenance       | ⚠️ Academic origin; unclear current maintenance status                 |
| Downloadable TTL/OWL     | ⚠️ Available via AGH but not widely mirrored                          |

**Verdict**: Strong candidate for operational PM concepts (scheduling, resource allocation, process groups). Complements [[proj-ontology]] which focuses on publication/description. May need to import selectively rather than adopt wholesale.

## Relationship to Other Candidates

- More operationally complete than [[proj-ontology]] (which is publication-focused)
- More PM-specific than [[seon-spmo]] (which is software engineering-focused)
- Less rigorously published than [[projectco-ontology]] (which has ResearchGate papers)
- Not a [[prov-o]] profile, so provenance tracking would need to be added separately

## Sources

- [[from-url-promont-ontology]] — https://ai.ia.agh.edu.pl
- [[initial-research-user]]
