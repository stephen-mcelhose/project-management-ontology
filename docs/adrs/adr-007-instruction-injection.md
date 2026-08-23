---
type: decision
title: "ADR-007: Agent Instruction Injection"
description: >
  Defines a three-layer composition model for the process agent's system
  instruction. Domain expertise flows in from the artifact layer at construction
  time; gate-level guidance flows in through tool return values at runtime.
  Keeps the agent's base mechanics generic so the same code can serve any
  domain whose knowledge is encoded in ontology + templates + shapes.
timestamp: 2026-08-23T00:00:00Z
status: accepted
tags: [adr, agent, process-agent, instruction, domain]
---

# ADR-007: Agent Instruction Injection

## Status

Accepted

## Context

The process agent (ADR-006, issue #39) ships with a static system instruction
hardcoded in `agent/agent.py`. That instruction describes the loop mechanics
correctly but has no domain knowledge: it says nothing about PM standards, what
constitutes a vague answer in this domain, or what the user is trying to
accomplish. When gate `guidance` fields are sparse, the model falls back on
generic LLM behaviour rather than PM-informed judgment.

Two separate concerns were conflated in the original design:

1. **Loop mechanics** — how to call tools, in what order, one gate at a time.
   These never change regardless of domain.

2. **Domain expertise** — what PM practice looks like, which standards apply
   (ISO 21502, DIN 69901), what "sponsor" or "tolerance" mean, how to
   challenge a vague scope statement. These are specific to the PM domain and
   should come from the artifact layer, not from code.

A related but distinct future goal is a fully domain-agnostic agent — one that
can serve any workflow domain (software delivery, HR onboarding, etc.) by
swapping only the artifact layer. That is tracked in a separate issue and is
not decided here. The two are not in conflict; this ADR is a step in that
direction.

## Decision

The system instruction is composed from three layers at agent construction time
and at runtime. The layers are ordered by specificity: generic mechanics first,
domain context second, gate context third.

### Layer 1 — Base mechanics (static, in code)

A constant `_BASE_INSTRUCTION` in `agent/agent.py` that describes only the
tool loop:

- Call `get_progress()` to orient.
- Call `get_next_gate()` to find the next question.
- Ask the user the gate's prompt. Wait for their answer.
- Record it. Repeat until done. Write. Validate. Advance.

This layer never changes. It is the same regardless of domain.

### Layer 2 — Domain instructions (from artifact layer, injected at construction)

`_project-manifest.yaml` gains an optional `agent_instructions` field. When
present, it contains free-text instruction prose specific to the domain:

- Who the agent is and what domain it operates in.
- Which standards and methodology are in scope.
- What domain-specific terms mean.
- How to push back on vague or evasive answers (examples, tone, thresholds).
- Any invariants the agent must enforce (e.g. "never invent data not supplied
  by the user").

`load_project_manifest()` reads this field and populates
`ProjectManifest.agent_instructions`. `build_agent()` accepts
`domain_instructions: str` and prepends it to the base instruction:

```
{domain_instructions}

{_BASE_INSTRUCTION}
```

If the field is absent or the manifest does not yet exist, `domain_instructions`
defaults to `""` and the agent falls back to base mechanics only. This keeps
the agent functional before `_project-manifest.yaml` is created (issue #50).

### Layer 3 — Phase and gate context (via tool return values, at runtime)

The model already receives gate-level context through `get_next_gate()`'s
return value, which includes the gate's `prompt` and `guidance`. No change is
needed here.

Phase-level context (`shared_context` from `_manifest.yaml`) is included in
the `get_progress()` response when a phase is active. The model sees this as
a tool result and incorporates it into its next response.

This layer does **not** mutate the agent's `instruction` field at runtime.
ADK's `LlmAgent.instruction` is fixed at construction. Tool return values are
the correct channel for runtime context: they are visible in the conversation
history, they do not require agent reconstruction, and they keep context
scoped to the turn where it is relevant.

## Rationale

### Why not dynamic instruction mutation?

ADK supports `instruction_provider` (a callable invoked per turn), which could
theoretically inject phase context into the instruction string dynamically.
This was rejected because:

- It couples agent construction to runtime state in a way that is hard to test.
- Tool return values achieve the same result through a mechanism the model
  already understands — they appear in the conversation as structured context.
- Per-turn instruction mutation makes the agent's behaviour harder to reason
  about and audit.

### Why `_project-manifest.yaml`, not a separate file?

Domain instructions belong next to the phase list and project-level metadata.
`_project-manifest.yaml` is already the single-read entry point for the
project. Adding `agent_instructions` there keeps the manifest the authoritative
source of "everything the agent needs to know about this project and domain
before it speaks to the user."

### Why not put domain instructions in `_manifest.yaml` per phase?

Phase-level instructions would require reconstructing the agent on each phase
transition — or injecting them via tool results, which is Layer 3. The domain
identity (what standards apply, what PM means, what vague looks like) does not
change between phases. It is a project-level, not phase-level, concern.

## Consequences

**Positive:**
- The agent's PM expertise is auditable and editable without touching code.
- Adding a new domain is a YAML change, not a code change (once the
  domain-agnostic agent goal is realised — separate issue).
- `_BASE_INSTRUCTION` is clearly separated from domain knowledge; reviewers
  can see what is mechanics and what is PM expertise.
- The fallback (empty `agent_instructions`) keeps the agent functional before
  `_project-manifest.yaml` is authored (issue #50).

**Negative / trade-offs:**
- `_project-manifest.yaml` takes on instruction authoring responsibility.
  It must be kept in sync with the ontology and templates — drift is possible.
  Mitigated by the same `make validate-schemas` discipline applied to
  `maps_to` CURIEs (ADR: CURIE drift detection).
- Gate-level `guidance` (Layer 3) and domain instructions (Layer 2) may
  overlap. Authors must be careful not to duplicate domain rules across both.

## What this does not decide

- The form or content of the PM domain instructions themselves — that is an
  authoring task for issue #50.
- Whether phase-level `shared_context` is surfaced via `get_progress()` or a
  dedicated tool — the current decision is `get_progress()`, but this can be
  revised without touching the ADR.
- The domain-agnostic agent (swappable domains at runtime) — tracked
  separately; this ADR is compatible with that goal.
