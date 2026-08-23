---
type: decision
title: "ADR-002: Phase Agent Prompts as Scaffolds"
description: >
  Establishes a policy of writing lightweight, non-prescriptive placeholder prompts
  per phase now, while deferring full agent specification to the ADK agent build
  (issue #39). Prompt files describe intent and reference instructions.yaml as
  the gate-level protocol; they do not hardcode conversation mechanics.
timestamp: 2026-08-23T00:00:00Z
status: accepted
tags: [adr, agent, prompt, architecture]
---

# ADR-002: Phase Agent Prompts as Scaffolds

**Status:** Accepted  
**Date:** 2026-08-23  
**Deciders:** Stephen McElhose

---

## Context

The project management ontology has a complete template artifact layer: every
PM document has an `entry.yaml`, `instructions.yaml`, `template.md`, and SHACL
shape. The `instructions.yaml` files encode a full gate-level protocol — what
to ask, in what order, mapped to the ontology, with validation rules.

Issue #39 proposes building a proper ADK agent that will use these artifacts as
tool context to assist with template population and ontology queries. That agent
is not yet built.

In the meantime, there is value in having a human-readable document per phase
that describes:
- The phase's purpose
- The document sequence and dependency chain
- How the artifact files fit together
- What the agent's job is at a high level

The risk is writing these too prescriptively — encoding conversation mechanics,
session management, retry logic, or output format — before the agent architecture
is decided. That would create throw-away work and false expectations.

---

## Decision

Write **one lightweight prompt file per phase**, stored at:

```
docs/prompts/{phase}-phase-agent.md
```

These files:

- Use `type: agent-prompt` and `status: draft` in OKF frontmatter
- Include a prominent **"Status: Placeholder"** notice at the top
- Describe the phase's purpose and document sequence in plain language
- Reference `instructions.yaml` as the authoritative gate protocol — they do
  not repeat or paraphrase gate content
- Reference the phase `_manifest.yaml` for the document index and shared context
- List explicitly what they **do not define** (conversation mechanics, session
  handling, output format) — these are deferred to the agent implementation
- Cross-reference this ADR and issue #39

These prompts are useful immediately as:
- Human onboarding guides for what each phase produces
- LLM context for ad-hoc experiments before the formal agent is built
- A specification input when issue #39 is worked

### What they are not

These prompts are **not** a finished agent specification. They must not be treated
as a contract for agent behavior. When issue #39 is worked, revisit all phase
prompts and either:
- Extend them into proper system prompts if the ADK agent uses them directly
- Replace them with references to the agent's actual implementation
- Deprecate them if the agent reads `instructions.yaml` directly without a wrapper prompt

---

## Consequences

### Positive
- Captures intent now without constraining the agent architecture
- Creates a useful human reference for each phase
- Prevents premature lock-in to a conversation pattern
- Clear "revisit" trigger tied to a concrete issue

### Trade-offs
- Prompts are stubs, not usable as production agent prompts today
- Requires discipline to update all phase prompts when #39 is resolved

---

## References

- Issue #39: Build Python ADK agent for OKF wiki + template Q&A
- `docs/prompts/initiation-phase-agent.md` — first prompt following this pattern
- `docs/adrs/adr-003-phase-manifest.md` — manifest pattern referenced by prompts
