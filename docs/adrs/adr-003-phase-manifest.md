---
type: decision
title: "ADR-003: Phase Manifest Pattern"
description: >
  Establishes a _manifest.yaml file at the root of each phase's template
  directory as the single authoritative index for that phase: document sequence,
  dependency chain, shared context fields, and phase completion condition.
  Required for agent and orchestrator readiness.
timestamp: 2026-08-23T00:00:00Z
status: accepted
tags: [adr, agent, orchestrator, manifest, architecture]
---

# ADR-003: Phase Manifest Pattern

**Status:** Accepted  
**Date:** 2026-08-23  
**Deciders:** Stephen McElhose

---

## Context

Each document template pack stores its dependency information in `entry.yaml`:
`dependencies`, `required_before`, `phase_order`, and `next_document` in the
`completion` block. This is sufficient for a single-document view but creates
friction for any consumer that needs a phase-level view.

A GAN-style review of the Initiation Phase identified the following concrete
problems:

1. **No single-read phase index.** An agent or orchestrator must open N separate
   `entry.yaml` files and reconstruct the document graph to know a phase's scope
   and sequence.

2. **`phase_order` is a global counter.** The field counts position in the entire
   project lifecycle, not within the phase. A consumer cannot use it directly as
   a phase-local index without also knowing the phase boundaries.

3. **Shared context fields are implicit.** Fields like `project_name` appear as
   `{{placeholders}}` in every template but there is no declaration of which
   fields are captured once and carried forward. An agent must infer this from
   gate inspection.

4. **Phase completion is undefined.** The chain terminates at the last document's
   `next_document` pointing into the next phase, but "the phase is complete" as
   a predicate is never stated explicitly. An orchestrator needs this to manage
   phase transitions.

---

## Decision

Every phase directory gets a `_manifest.yaml`:

```
templates/{phase}/_manifest.yaml
```

### Required content

```yaml
# OKF frontmatter
type: phase-manifest
phase: {phase-id}
phase_label: {Human Label}
ontology_phase: https://stephen-mcelhose.github.io/project-management-ontology/phases/{Phase}
package: pkgs:{Phase}Package
standard: ISO 21502:2020

# Document sequence — in dependency order, phase-local numbering
documents:
  - id: {document-id}          # matches templates/{phase}/{document-id}/
    phase_local_order: 1       # 1-based within this phase only
    title: {Document Title}
    ontology_class: pm:{ClassName}
    dependencies: []           # ids of documents that must exist first
    required_before:
      - {document-id}          # ids of documents that depend on this one

# Shared context — fields captured once and carried across all documents
# An agent MUST NOT re-ask for these after the first capture
shared_context:
  - field: {gate_id}
    maps_to: {ontology:property}
    first_captured_in: {document-id}

# Phase completion
# The phase is done when all documents listed here have output_status: draft
completion:
  required_documents:
    - {document-id}
  output_status: draft
  next_phase: {phase-id}
  first_document_in_next_phase: {document-id}
```

### Rules

- `phase_local_order` is independent of `phase_order` in `entry.yaml` (which
  remains as-is for backward compatibility). Use `phase_local_order` for all
  phase-scoped sequencing.
- `shared_context` entries must match a real gate `id` in the named document's
  `instructions.yaml`. Do not declare shared context for a field that doesn't
  have a gate.
- The manifest is the **single source of truth** for phase-level sequencing.
  If it conflicts with `entry.yaml`, fix `entry.yaml`.
- The manifest does **not** duplicate gate content from `instructions.yaml`.
  It references documents; it does not describe what's inside them.

### Process integration

The process for defining document templates (`docs/processes/defining-document-templates.md`)
is updated to require:

- When adding the **first** document to a new phase: create `_manifest.yaml`
  with that document as the only entry.
- When adding a **subsequent** document to an existing phase: update
  `_manifest.yaml` to include the new document in the correct position.
- The manifest must be committed in the same commit as the template pack.

---

## Consequences

### Positive
- An agent or orchestrator can load the entire phase context in one read
- Phase-local ordering is unambiguous (`phase_local_order: 1` always means
  "first in this phase")
- Shared context fields are formally declared — no agent has to guess
- Phase completion is an explicit, queryable predicate
- Enables a future orchestrator to manage phase transitions without reading
  every `entry.yaml`

### Trade-offs
- Adds one file per phase (5 files total across all phases)
- Shared context declarations must be kept in sync with gate changes — a
  process discipline requirement
- Backfilling manifests for already-complete phases (planning, execution,
  monitoring-control) is needed; tracked in individual GitHub issues

### Not in scope (deferred to agent implementation)
- Progress/checkpoint schema (how an agent persists partial state mid-document)
- Structured validation rules on gates (gate `validation:` fields remain prose)
- Gate output type annotations (`type:` on gates)

These are agent-layer concerns. If they are needed, open issues against the
agent repo (or revisit when issue #39 is worked), not against this artifact layer.

---

## References

- GAN-style review of Initiation Phase (session context, 2026-08-23)
- `templates/initiation/_manifest.yaml` — first manifest following this pattern
- Issue #39: Build Python ADK agent
- `docs/adrs/adr-002-phase-agent-prompts.md`
- `docs/processes/defining-document-templates.md`
