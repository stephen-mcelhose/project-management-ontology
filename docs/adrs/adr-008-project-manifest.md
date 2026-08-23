---
type: decision
title: "ADR-008: Project Manifest and Three-Tier Hierarchy"
description: >
  Establishes templates/_project-manifest.yaml as the project-level entry point
  above the phase manifests introduced in ADR-003. Formalises the three-tier
  manifest hierarchy, the cross-phase shared context contract, and the canonical
  phase sequence. Does not supersede ADR-003 — the phase manifest pattern is
  unchanged.
timestamp: 2026-08-23T00:00:00Z
status: accepted
tags: [adr, agent, orchestrator, manifest, architecture, hierarchy]
---

# ADR-008: Project Manifest and Three-Tier Hierarchy

**Status:** Accepted  
**Date:** 2026-08-23  
**Deciders:** Stephen McElhose

---

## Context

ADR-003 established `_manifest.yaml` at each phase directory as the single-read
index for that phase. This solved the per-phase problem (document sequence,
shared context, completion condition) but left a gap one level up: there was no
single file that told an orchestrator which phases exist, in what order, and what
agent domain knowledge applies across the entire project.

Three concrete problems remained after ADR-003:

1. **No authoritative phase sequence.** The chain existed implicitly — each phase
   manifest's `completion.next_phase` pointed to the successor — but it was
   distributed across five files. An orchestrator had to load and traverse all
   five to reconstruct the sequence.

2. **Cross-phase shared context was implicit.** Fields like `project_name` were
   declared in each phase manifest's `shared_context`, but no single location
   stated which fields span all phases and where they originate.

3. **Domain instructions had nowhere to live.** ADR-007 defined a Layer 2
   injection model (domain expertise prepended to the agent's base instruction),
   and specified that `_project-manifest.yaml` would carry the `agent_instructions`
   field — but the file did not yet exist.

---

## Decision

A single `templates/_project-manifest.yaml` is the project-level entry point.
This formalises the three-tier manifest hierarchy:

```
templates/_project-manifest.yaml          ← project level
templates/{phase}/_manifest.yaml          ← phase level   (ADR-003)
templates/{phase}/{document}/entry.yaml   ← document level
```

Each tier can be read independently. An orchestrator starting a project run
reads the project manifest first and is fully oriented without touching phase or
document files.

### Required content

```yaml
type: project-manifest
standard: ISO 21502:2020

agent_instructions: |
  # Free-text PM domain expertise injected at Layer 2 (ADR-007).
  # Must cover: domain identity, pushback policy, invariants.
  # Must NOT duplicate gate-level guidance from instructions.yaml files.

phases:
  - id: {phase-id}
    phase_local_order: {n}        # 1-based, project-wide
    manifest: templates/{phase-id}/_manifest.yaml
    required_before: [{phase-id}] # immediate successors only

cross_phase_context:
  - field: {gate_id}              # must match a real gate id in the named document
    maps_to: {ontology:property}
    first_captured_in: {phase-id}/{document-id}
```

### Rules

- `phases` is the **single authoritative source** for phase order. If it
  conflicts with the `next_phase` chain in phase manifests, fix the phase
  manifests.
- `required_before` on each phase entry expresses the immediate predecessor
  constraint (not the full transitive closure). Closure, the terminal phase,
  has `required_before: []`.
- `cross_phase_context` declares only fields that span **all five phases**.
  Fields relevant within a single phase belong in that phase's `_manifest.yaml`
  `shared_context` block.
- `agent_instructions` is authored prose, not machine-readable structure. It is
  loaded verbatim and prepended to the agent's base instruction (ADR-007). It
  must not be left empty in production; the loader tolerates an absent field
  only to allow incremental bring-up before this file exists.
- The file is loaded by `agent/lifecycle/manifest.py::load_project_manifest()`.
  Any new top-level fields must be handled there, or left as documentation-only
  and noted as such.

### What this does not change

ADR-003 is still accepted and in full force. The phase manifest pattern, its
required fields, and its process integration rules are unchanged. This ADR adds
a layer above, not a replacement for, what ADR-003 established.

---

## Consequences

### Positive

- An orchestrator can load the entire project context (phase order, domain
  instructions, cross-phase fields) in a single read before touching any phase
  or document file.
- Phase order is no longer implicit in the `next_phase` chain — it is explicit
  and queryable from one location.
- Cross-phase shared context has a single, authoritative declaration. Phase
  manifests continue to carry their own `shared_context` for phase-scoped
  fields; the two levels do not conflict.
- `agent_instructions` makes PM domain expertise auditable and editable without
  touching agent code (ADR-007 consequence, now realised).

### Trade-offs

- One more file to keep in sync with the phase manifests. If a phase is renamed
  or reordered, both the project manifest and the affected phase manifest must
  be updated.
- `cross_phase_context` entries must correspond to real gate ids in the named
  document's `instructions.yaml`. `make validate-schemas` does not currently
  verify this (it only validates `instructions.yaml` files); this is a process
  discipline requirement.
- `agent_instructions` content can drift from the ontology and gate guidance
  (Layer 3) over time. Authors must review it when adding or changing document
  gates that introduce new domain terms or pushback scenarios.

---

## References

- `docs/adrs/adr-003-phase-manifest.md` — phase-level layer; pattern unchanged
- `docs/adrs/adr-007-instruction-injection.md` — specifies the Layer 2 model
  that `agent_instructions` satisfies
- `templates/_project-manifest.yaml` — the file this ADR governs
- `agent/lifecycle/manifest.py` — `load_project_manifest()` implementation
- Issue #50: Author `templates/_project-manifest.yaml`
