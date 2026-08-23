---
type: reference
title: Glossary
description: >
  Canonical definitions for terms used across the process-assistant
  repo — ontology, templates, tooling, and agent/orchestrator layers.
  Resolves naming inconsistencies across docs, prompts, issues, and ADRs.
timestamp: 2026-08-23T23:07:33Z
tags: [glossary, reference, meta]
---

# Glossary

Terms are listed alphabetically. Where a term has a common near-synonym that
is used inconsistently in the repo, the synonym is called out explicitly.

---

## Agent

A single-purpose AI reasoning loop with tools. In this project, an agent
handles one scoped task domain — e.g. answering wiki questions, filling
template packs for a phase, or querying the ontology. The ADK agent in
issue #39 is the first agent built on top of this artifact layer.

**Not:** an orchestrator. An agent does not coordinate other agents.

**See also:** [Orchestrator](#orchestrator), issue #39

---

## Document Class

An OWL class in the `pm:` namespace representing a type of project management
document (e.g. `pm:BusinessCase`, `pm:StakeholderRegister`). All document
classes are subclasses of `foaf:Document`. Every document class is declared in
`ontology/modules/document.ttl` and carries:
- `pm:producedInPhase` — the phase that produces it
- `pm:hasHardDependency` — what must exist before it
- `rdfs:seeAlso` — the PRINCE2 management product URL

---

## Gate

A single step in an `instructions.yaml` file. Each gate represents one field
or question in a PM document. A gate specifies:
- `id` — matches the `{{placeholder}}` in `template.md`
- `prompt` — the question an agent asks the user
- `fills` — which template section receives the answer
- `maps_to` — the ontology property the answer asserts as an RDF triple
- `required` — whether the document is incomplete without it
- `type` — the rendering shape of the gate's output; one of seven values (`string`, `date`, `identifier`, `prose`, `list`, `table`, `section`) — see [ADR-004](../adrs/adr-004-gate-output-type-system.md)
- `deferred_value` — literal text written when a `required: false` gate is skipped; mandatory on all optional gates
- `validation` / `guidance` — acceptance rules for the answer (prose, LLM-readable)
- `validation_rules` — optional machine-readable constraint block alongside `validation:`; closed key vocabulary — see [ADR-005](../adrs/adr-005-gate-validation-rules.md)

Gates are worked in `order` sequence. A document is complete when all
`required: true` gates in its `completion.required_gates` list are filled.

**Not to be confused with:** a *phase gate* or *stage gate* (Cooper's
Stage-Gate® model, also used in PMI/PMBOK practice) — a formal Go/No-Go
review checkpoint where a project is evaluated before advancing to the next
phase. In this project, `gate` means a single field-filling step within a
document template, not a phase-boundary review event.

---

## Manifest

A `_manifest.yaml` file at the root of a phase's template directory
(`templates/{phase}/_manifest.yaml`). The single-read index for that phase.

A manifest contains:
- All documents in the phase, in `phase_local_order` (1-based within the phase)
- `dependencies` and `required_before` for each document (the dependency DAG)
- `shared_context` — fields captured once and carried forward across documents
- `completion` — the phase exit condition and pointer to the next phase

**Not to be confused with** `entry.yaml`, which is document-scoped.
The manifest is phase-scoped.

**See also:** ADR-003, `templates/initiation/_manifest.yaml`

---

## Orchestrator

A coordinator that routes work between multiple agents and manages phase
transitions across the full project lifecycle. An orchestrator knows which
phase is active, invokes the appropriate agent, detects phase completion,
and carries context (e.g. `project_name`) across phase boundaries.

The orchestrator is planned in issue #49 and depends on the ADK agent (#39)
and the orchestrator interface contract (#50).

**Not:** an agent. An orchestrator does not itself fill documents.

**See also:** [Agent](#agent), issue #49, issue #50

---

## Package

A GitHub Milestone grouping the template packs for all documents produced
within a single lifecycle phase. A package is a **build/delivery concept**,
not an ontology concept.

- `pkgs:InitiationPackage` — milestone covering issues #8–#12 (5 documents)
- `pkgs:PlanningPackage` — milestone covering issues #13–#20 (8 documents)
- etc.

**Synonym used inconsistently:** "phase" (as in "planning phase work") —
prefer "package" when referring to the delivery milestone and "phase" when
referring to the lifecycle stage.

**Not to be confused with:** [Phase](#phase), or a WBS *work package* — the
lowest-level deliverable unit in a Work Breakdown Structure, where work is
assigned, estimated, and tracked.

---

## Output Status

The lifecycle state of a PM document, carried in the manifest and
`instructions.yaml` files as `output_status`. Valid values:

| Value       | Meaning                                                              |
| ----------- | -------------------------------------------------------------------- |
| `pending`   | Document is in progress — one or more required gates are unfilled    |
| `draft`     | All required gates are filled; document meets its completion condition |
| `approved`  | Draft has received explicit sponsor sign-off                         |

A phase's exit condition requires all mandatory documents to reach
`output_status: draft` (see [Phase Transition](#phase-transition)).

**Not to be confused with:** completion of the gate sequence alone. A
document can have all gates answered yet still await sponsor sign-off before
reaching `approved`.

---

## Phase

A named stage in the project management lifecycle, grounded in DIN 69901.
Represented as an OWL individual (e.g. `phases:Initiation`).

The five phases in order:

| Phase                 | Ontology individual             |
| --------------------- | ------------------------------- |
| Initiation            | `phases:Initiation`             |
| Planning              | `phases:Planning`               |
| Execution             | `phases:Execution`              |
| Monitoring & Control  | `phases:MonitoringControl`      |
| Closure               | `phases:Closure`                |

A phase has a start condition, an exit condition (all required documents at
`output_status: draft`, sponsor-approved), and a pointer to the next phase.
The manifest for each phase declares these formally.

**Not to be confused with:** [Package](#package)

---

## Phase Agent Prompt

A lightweight placeholder document at `docs/prompts/{phase}-phase-agent.md`
that describes a phase's purpose, document sequence, and how an agent should
use the artifact files. It is **not** a finished agent specification —
conversation mechanics and session handling are deliberately left to the
agent implementation. See ADR-002.

**Not to be confused with:** [Package Agent Prompt](#package-agent-prompt)

---

## Package Agent Prompt

A build-time runbook at `docs/prompts/{phase}-package-agent-prompt.md` that
instructs an agent (or human) on how to **create** the template packs for a
phase (researching standards, writing `entry.yaml`, `instructions.yaml`,
`template.md`, and the SHACL shape). These are finished and used; the
template packs they produced are complete for all phases except Closure.

**Not to be confused with:** [Phase Agent Prompt](#phase-agent-prompt)

---

## Phase Local Order

The 1-based position of a document within its phase (`phase_local_order` in
`_manifest.yaml`). Independent of `phase_order` in `entry.yaml`, which is a
global lifecycle counter. Always use `phase_local_order` for phase-scoped
sequencing; use `phase_order` only when comparing documents across phases.

---

## Phase Transition

The event of advancing from one phase to the next. Triggered when all
required documents in the current phase reach `output_status: draft` and
receive sponsor approval. Formally declared in the phase manifest's
`completion.transition_condition` (see issue #50).

---

## Process Assistant

The product and git repository (`stephen-mcelhose/process-assistant`). A
generic gate-driven assistant that loads a domain pack (ontology, SHACL,
templates) and walks a user through documents. Project management is the
first pack, not the name of the product.

**Not:** the OWL namespace. `pm:` IRIs still use
`https://stephen-mcelhose.github.io/project-management-ontology/`.

**See also:** [ADR-009](../adrs/adr-009-repository-rename.md)

---

## SHACL Shape

A constraint file at `shapes/{phase}/{document}.shacl.ttl` that validates
a filled document instance against the ontology. The SHACL shape is the
machine-readable acceptance test for a document: it asserts that required
properties are present, that range types are correct, and that the document
is linked to the correct phase individual. Validation is run via
`python tools/validate/validate.py` (or `make validate`).

---

## Shared Context

Fields captured once — typically in the first document that asks for them —
and carried forward to all subsequent documents in the same phase (and
potentially across phases). An agent should never re-ask for a shared context
field once it has been collected.

Declared in each phase's `_manifest.yaml` under `shared_context`. Cross-phase
shared context is to be declared in the top-level project manifest (issue #50).

**Example:** `project_name` is captured in the Project Proposal and used as a
header field in every subsequent document.

---

## Template Pack

The four files that together define one PM document:

```
templates/{phase}/{document}/
  entry.yaml           ← metadata: standard citations, dependency chain
  instructions.yaml    ← ordered gates: what to ask, what to fill
  template.md          ← Markdown scaffold with {{placeholders}}
shapes/{phase}/{document}.shacl.ttl   ← ontology validation shape
```

A template pack is the primary deliverable of each template issue (#8–#34).

---

## Sources

- ADR-002: `docs/adrs/adr-002-phase-agent-prompts.md`
- ADR-003: `docs/adrs/adr-003-phase-manifest.md`
- ADR-004: `docs/adrs/adr-004-gate-output-type-system.md`
- ADR-005: `docs/adrs/adr-005-gate-validation-rules.md`
- ADR-009: `docs/adrs/adr-009-repository-rename.md`
- Process guide: `docs/processes/defining-document-templates.md`
- GAN review session — 2026-08-23
- M3 Artifact Hygiene session — 2026-08-24
