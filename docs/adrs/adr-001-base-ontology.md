---
type: decision
title: "ADR-001: Base Ontology Selection"
description: Selects the PROJ Ontology (PROV-O profile) as our provenance backbone and defines a bespoke pm: operational namespace, with DIN 69901 process groups as the phase taxonomy and ProjectCO v2.0 as the conceptual model reference for operational classes.
timestamp: 2024-08-22T00:00:00Z
status: accepted
tags: [adr, ontology, architecture, prov-o, din-69901]
---

# ADR-001: Base Ontology Selection

**Status:** Accepted  
**Date:** 2024-08-22  
**Deciders:** Stephen McElhose

---

## Context

We are building a project management ontology to serve two phases:

- **Phase 1 (now):** Base primitives — formal OWL classes for PM concepts, document templates annotated to project phases, and visualization tooling.
- **Phase 2 (future):** An agent-driven workflow system that fills out project documents via human interaction and heuristics, can hand off to humans, and resumes work via triggers such as uploaded documents.

The ontology must cover:
- Phases, tasks, milestones, roles, resources, deliverables, risks, decisions
- Document templates that are explicitly linked to the phase in which they are produced
- A provenance model suitable for Phase 2 (tracking who did what, when, and why)

### Rejected outright: PMBOK / PMI

The PMBOK Guide is PMI intellectual property. Its process group names, knowledge area structure, and process descriptions are protected. We model the same *concepts* (which predate PMI) but ground them in open standards. This is non-negotiable.

### Candidates evaluated

| Candidate         | Strengths                                           | Weaknesses                                            |
| ----------------- | --------------------------------------------------- | ----------------------------------------------------- |
| **PROJ Ontology** | PROV-O profile; stable URI; domain-neutral upper layer | Research/funding focus; no tasks, milestones, or risks |
| **PROMONT**       | DIN 69901-grounded; full operational coverage       | Not PROV-O-based; hosted on AGH server (accessibility uncertain) |
| **ProjectCO v2.0**| Best operational completeness (WBS, Assignment, Risk) | No stable import URI; OWL file not at a published namespace |
| **SEON/SPMO**     | Best document-to-phase mapping already done         | Software engineering bias; requires UFES account access |

---

## Decision

**Import PROJ** (`https://linked.data.gov.au/def/project`) as the provenance upper layer, and define a bespoke **`pm:` namespace** for all operational PM concepts.

The `pm:` operational layer is:
- **Structured by DIN 69901 process groups** — the open German PM standard that PROMONT is grounded in. This gives us IP-clean phase taxonomy with clear document-template assignments.
- **Class-modelled after ProjectCO v2.0** — we adopt its conceptual model (Project, Phase, Task, Milestone, Role, Assignment, WorkProduct, Risk, Constraint) without importing its OWL file directly (no stable import URI exists).
- **Document-mapped using the SEON/SPMO pattern** — each document template class carries a `pm:producedInPhase` annotation linking it to a DIN 69901 phase.

### Phase taxonomy (DIN 69901)

| Phase                    | `pm:Phase` instance            | Key document templates                                      |
| ------------------------ | ------------------------------ | ----------------------------------------------------------- |
| Initiation               | `pm:phases/Initiation`         | Project Charter, Stakeholder Register, Project Brief        |
| Planning                 | `pm:phases/Planning`           | Project Plan, WBS, Risk Register, RACI Matrix, Comms Plan   |
| Execution                | `pm:phases/Execution`          | Status Report, Meeting Minutes, Change Request, Issue Log   |
| Monitoring & Control     | `pm:phases/MonitoringControl`  | Progress Report, Risk Update, Variance Report               |
| Closure                  | `pm:phases/Closure`            | Lessons Learned, Closure Report, Benefits Realization       |

### What PROJ gives us

- `proj:Project` (subclass of `prov:Activity`) — our `pm:Project` subclasses this
- `proj:hadSubActivity` — used for sub-projects and phases
- `proj:hadPlan` — links a project to its governing plan document
- `proj:hadLeader`, `proj:hadSponsor` — role associations
- Full PROV-O inheritance (`prov:wasAssociatedWith`, `prov:wasGeneratedBy`, `prov:used`, etc.)

### What `pm:` adds

Everything PROJ does not cover:
- `pm:Phase` — a named lifecycle stage (Initiation → Closure)
- `pm:Task` — unit of work with duration, effort, and predecessor dependencies
- `pm:Milestone` — zero-duration checkpoint
- `pm:Role` — typed agent responsibility (ProjectManager, Sponsor, TeamMember, Stakeholder)
- `pm:Resource` — human, material, or financial
- `pm:Assignment` — reification of resource-to-task allocation
- `pm:WorkProduct` / `pm:Document` — deliverables, with `pm:producedInPhase`
- `pm:Risk` — uncertain event with probability, impact, and response strategy
- `pm:Decision` — a formal choice made during the project, with rationale

---

## Consequences

### Positive
- **IP-clean throughout.** PROJ is CC-BY 4.0 (CSIRO). DIN 69901 concepts are freely referenceable. Our `pm:` classes are our own IP.
- **PROV-O provenance built in.** Phase 2 agent actions (filling in a document, making a decision) can be recorded as `prov:Activity` instances without any bridging work.
- **Phase-annotated templates.** Every document template carries a `pm:producedInPhase` triple, making it trivially queryable: "give me all documents for the Planning phase."
- **Full operational coverage from day one.** We are not constrained by what PROJ chose to model — our `pm:` layer covers all the operational primitives Phase 2 will need.
- **Vendor copy in repo.** `domains/pm/ontology/vendor/proj.ttl` is pinned so builds are reproducible without network dependency.

### Trade-offs
- We maintain the `pm:` namespace ourselves — no upstream community. Acceptable for a project-specific ontology; we document the conceptual sources (DIN 69901, ProjectCO) in the wiki.
- ProjectCO and PROMONT are referenced conceptually, not imported — if their OWL files become stably available, we could align formally later.

---

## References

- [PROJ Ontology](../wiki/research/proj-ontology.md) — wiki page
- [PROMONT](../wiki/research/promont-ontology.md) — wiki page (DIN 69901 grounding)
- [ProjectCO v2.0](../wiki/research/projectco-ontology.md) — wiki page (operational class model)
- [SEON/SPMO](../wiki/research/seon-spmo.md) — wiki page (document-to-phase mapping pattern)
- [PMBOK & OWL — IP Landscape](../wiki/research/pmbok-owl-ip.md) — wiki page (why PMI is excluded)
- `domains/pm/ontology/vendor/proj.ttl` — pinned vendor copy of PROJ ontology
