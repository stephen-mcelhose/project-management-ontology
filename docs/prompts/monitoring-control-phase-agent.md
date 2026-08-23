---
type: agent-prompt
title: Monitoring & Control Phase Agent Prompt
description: >
  Placeholder prompt describing the Monitoring & Control Phase scope and artifact
  structure. The gate-level protocol lives in each document's instructions.yaml.
  Revisit when building the ADK agent (issue #39). See ADR-002.
phase: monitoring-control
status: draft
tags: [prompt, agent, monitoring-control]
timestamp: 2026-08-23T00:00:00Z
see_also: docs/adrs/adr-002-phase-agent-prompts.md
---

# Monitoring & Control Phase Agent Prompt

> **Status: Placeholder.**
> This prompt describes intent and structure. It is not a finished agent specification.
> The gate-level protocol for each document lives in its `instructions.yaml`.
> Revisit when building the ADK agent (issue #39) — see ADR-002.

---

## Phase Purpose

Monitoring & Control tracks project performance against the plan, manages risks
and issues as they emerge, logs decisions, and records all approved changes.
These documents are the project's running record — they are updated throughout
Execution, not produced once and closed.

---

## Documents (in dependency order)

The phase manifest (`templates/monitoring-control/_manifest.yaml`) is the
authoritative index.

| Order | Document       | Key question it answers                                    |
| ----- | -------------- | ---------------------------------------------------------- |
| 1     | Status Report  | Is the project on track against the plan?                  |
| 2     | Risk Register  | What risks exist, and what is being done about each?       |
| 3     | Issue Log      | What problems have occurred, and are they resolved?        |
| 4     | Decision Log   | What formal decisions have been made and why?              |
| 5     | Change Log     | What changes have been approved and implemented?           |

---

## How to Use the Artifact Files

```
templates/monitoring-control/{document}/
  entry.yaml          ← metadata: standard citations, dependency chain
  instructions.yaml   ← ordered gates: what to ask, what to fill
  template.md         ← the output scaffold with {{placeholders}}
```

---

## Living Documents

All five documents in this phase are **living registers**, updated on a recurring
cadence rather than completed once. An agent populating these should support:
- Adding new entries to an existing register (not starting from scratch each time)
- Updating the status of existing entries (risk probability changes, issue resolved)

The template and gate structure applies per entry, not per document instance.

---

## Shared Context

`project_name` was captured in the Initiation Phase. Do not re-ask.
See `templates/monitoring-control/_manifest.yaml` under `shared_context`.

---

## Phase Exit

Monitoring & Control is complete when the project moves to Closure — i.e., all
Execution deliverables are accepted, all open issues and risks are resolved or
formally accepted, and the Change Log reflects a closed change set. The next
phase is Closure; entry point is the Handover Document.

---

## What This Prompt Does Not Define

Deliberately left to the agent implementation (issue #39):
- Register update mechanics (append entry vs. edit in place)
- Concurrency with Execution (M&C runs alongside Execution, not after it)
- Cadence and trigger logic for recurring Status Reports
- Session continuity across long-running monitoring periods
