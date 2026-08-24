---
type: agent-prompt
title: Closure Phase Agent Prompt
description: >
  Placeholder prompt describing the Closure Phase scope and artifact structure.
  Template packs for this phase are still in progress (issues #30-34).
  Revisit when templates are complete and when building the ADK agent (issue #39).
  See ADR-002.
phase: closure
status: draft
tags: [prompt, agent, closure]
timestamp: 2026-08-23T00:00:00Z
see_also: docs/adrs/adr-002-phase-agent-prompts.md
---

# Closure Phase Agent Prompt

> **Status: Placeholder — template packs incomplete.**
> Template packs for this phase are still being built (issues #30–#34).
> This prompt will need updating once all five closure template packs are merged.
> Additionally, this is not a finished agent specification — revisit when building
> the ADK agent (issue #39). See ADR-002.

---

## Phase Purpose

The Closure Phase formally ends the project. It transfers deliverables to the
operational owner, captures lessons learned, produces the final project report,
and archives project records. Nothing in Closure creates new deliverables — it
accounts for and hands over what was produced in Execution.

---

## Documents (in dependency order)

The phase manifest (`domains/pm/templates/closure/_manifest.yaml`) will be the authoritative
index once created (issue #43, blocked on #30–#34). Planned document sequence:

| Order | Document                  | Key question it answers                             |
| ----- | ------------------------- | --------------------------------------------------- |
| 1     | Handover Document         | Have deliverables been formally transferred?        |
| 2     | Final Project Report      | Did the project achieve its objectives?             |
| 3     | Lessons Learned Report    | What should future projects do differently?         |
| 4     | Project Closure Statement | Is the project formally closed?                     |
| 5     | Archive Index             | Where are all project records stored?               |

---

## How to Use the Artifact Files

```
domains/pm/templates/closure/{document}/
  entry.yaml          ← metadata: standard citations, dependency chain
  instructions.yaml   ← ordered gates: what to ask, what to fill
  template.md         ← the output scaffold with {{placeholders}}
```

Work through gates in `order` sequence per `instructions.yaml`.

---

## Shared Context

`project_name` and all project metadata were captured in the Initiation Phase.
Do not re-ask. Cross-phase shared context will be declared in the top-level
project manifest when issue #50 is worked.

---

## Phase Exit

Closure is the terminal phase. There is no `next_phase`. The phase is complete
when the Project Closure Statement is signed off and the Archive Index is
committed. The project record is then immutable.

---

## What This Prompt Does Not Define

Deliberately left to the agent implementation (issue #39):
- Handover workflow mechanics (who signs off, in what system)
- Archive location and format
- Integration with the Monitoring & Control outputs (open risks, issue resolution)
