---
type: concept
title: PMBOK & OWL — IP Landscape
description: Why there is no official open W3C-endorsed PMBOK ontology, what the IP situation is, and what open alternatives exist for modeling project management concepts formally.
timestamp: 2024-08-22T00:00:00Z
resource: https://www.pmi.org
tags: [pmbok, pmi, ip, ontology, landscape]
---

# PMBOK & OWL — IP Landscape

## The Core Problem

The **Project Management Institute (PMI)** treats the PMBOK Guide text as highly protected proprietary intellectual property. This means there is no officially sanctioned, PMI-endorsed OWL or Turtle ontology of PMBOK concepts available for open use — unlike comparable domains:

| Domain            | Open Ontology          | Status              |
| ----------------- | ---------------------- | ------------------- |
| Medical           | SNOMED CT, ICD-10      | ✅ Open / licensed  |
| Finance           | FIBO                   | ✅ Open             |
| Project Mgmt      | PMBOK                  | ❌ Proprietary text |

This has been noted explicitly in ontology research circles. Maria-Esther Vidal and others (including commentary on keet.wordpress.com) documented attempts to formalize PMBOK 5th edition in OWL that ran into IP barriers — the *process descriptions* and *knowledge area definitions* are PMI's IP even if the underlying *concepts* (task, risk, milestone) are not.

## What PMI Protects

PMI's IP restrictions apply to:
- The **text** of the PMBOK Guide
- The **named process groups** and **knowledge area names** as a structured system
- The **PMBOK framework** as a compiled body of work

PMI does **not** own the underlying generic concepts of project management (tasks, risks, milestones, resources, phases). These are industry-common concepts predating PMI.

## Safe Modeling Strategy

The safe approach is to model **concepts** rather than **framework names**:

| Avoid (PMI IP risk)             | Safe equivalent                          |
| ------------------------------- | ---------------------------------------- |
| "PMBOK Knowledge Areas"         | Generic PM concepts (scope, cost, risk)  |
| "Initiating Process Group"      | `pm:Phase` with type `Initiation`        |
| "Project Scope Management"      | `pm:ScopeDefinition`, `pm:WBS`           |
| "Risk Response Planning"        | `pm:RiskResponse` with strategy types    |

## Open PM Standards Available

Several open, non-IP-restricted standards provide the same conceptual coverage and can be freely modeled in OWL:

| Standard        | Body    | Key strengths                                    | OWL available |
| --------------- | ------- | ------------------------------------------------ | ------------- |
| **DIN 69901**   | DIN     | Comprehensive German PM standard; basis for [[promont-ontology]] | Via PROMONT |
| **ISO 21500**   | ISO     | International PM standard aligned with PMBOK    | No official OWL |
| **PM²**         | EU      | European Commission open PM methodology          | No official OWL |
| **PRINCE2**     | Axelos  | UK process-based PM; partially open concepts     | No official OWL |
| **Scrum Guide** | Scrum.org | Open source; process framework                | No official OWL |

## Existing Academic Approaches

Researchers have produced PMBOK-inspired ontologies by abstracting concepts rather than transcribing text:

- **[[promont-ontology]]** — grounds concepts in DIN 69901 (IP-safe alternative to PMBOK)
- **[[projectco-ontology]]** — original academic work, not derived from PMBOK text
- **[[seon-spmo]]** — grounded in software engineering literature, not PMBOK
- **[[proj-ontology]]** — PROV-O profile; domain-neutral, no PMBOK reference

## Implication for This Project

We should model **project management concepts** (the universal ideas) and ground them in open standards, not PMBOK text. The concepts we need — tasks, milestones, risks, roles, deliverables, phases — exist in DIN 69901, ISO 21500, and general PM literature and are freely modelable.

Referencing PMBOK as an *informative* source (not normative) in documentation is fine. Building an ontology that *implements* PMBOK is a legal grey area.

## Sources

- [[from-url-pmbok-owl-ip]] — https://keet.wordpress.com (referenced, 404 at time of access)
- [[initial-research-user]]
- [[promont-ontology]] — DIN 69901 as safe alternative
