---
type: agent-prompt
title: Execution Phase Agent Prompt
description: >
  Placeholder prompt describing the Execution Phase scope and artifact structure.
  The gate-level protocol lives in each document's instructions.yaml.
  Revisit when building the ADK agent (issue #39). See ADR-002.
phase: execution
status: draft
tags: [prompt, agent, execution]
timestamp: 2026-08-23T00:00:00Z
see_also: docs/adrs/adr-002-phase-agent-prompts.md
---

# Execution Phase Agent Prompt

> **Status: Placeholder.**
> This prompt describes intent and structure. It is not a finished agent specification.
> The gate-level protocol for each document lives in its `instructions.yaml`.
> Revisit when building the ADK agent (issue #39) — see ADR-002.

---

## Phase Purpose

The Execution Phase is where the work happens. Documents produced here describe
individual work packages, track deliverable progress, record changes to scope or
plan, and evidence quality assurance. Unlike Planning documents (created once),
Execution documents are typically instantiated repeatedly — one Change Request
per change event, one Deliverable Status Report per reporting cycle.

---

## Documents (in dependency order)

The phase manifest (`domains/pm/templates/execution/_manifest.yaml`) is the authoritative index.

| Order | Document                  | Key question it answers                           |
| ----- | ------------------------- | ------------------------------------------------- |
| 1     | Work Package Description  | What exactly is this unit of work?                |
| 2     | Deliverable Status Report | Is this deliverable on track?                     |
| 3     | Change Request            | What change is being requested and why?           |
| 4     | Quality Audit Report      | Does the work meet the quality criteria?          |

---

## How to Use the Artifact Files

```
domains/pm/templates/execution/{document}/
  entry.yaml          ← metadata: standard citations, dependency chain
  instructions.yaml   ← ordered gates: what to ask, what to fill
  template.md         ← the output scaffold with {{placeholders}}
```

Work through gates in `order` sequence per `instructions.yaml`.

---

## Recurring Documents

Work Package Descriptions, Deliverable Status Reports, Change Requests, and
Quality Audit Reports are typically produced multiple times per project. The
template and gate structure applies to each instance. An agent should be able
to fill a new instance without re-reading prior instances unless cross-referencing.

---

## Shared Context

`project_name` was captured in the Initiation Phase. Do not re-ask.
See `domains/pm/templates/execution/_manifest.yaml` under `shared_context`.

---

## Phase Exit

Execution is complete when all planned work packages have an associated
Deliverable Status Report at `output_status: accepted` and all open Change
Requests are resolved. The next phase is Monitoring & Control (which runs
concurrently with Execution in practice — see note below).

> **Note:** In practice, Monitoring & Control runs alongside Execution, not
> after it. The linear phase sequence in the manifests reflects the document
> dependency chain, not a strict temporal ordering. An orchestrator should
> treat M&C documents as active throughout Execution.

---

## What This Prompt Does Not Define

Deliberately left to the agent implementation (issue #39):
- Recurring document handling (how to create multiple instances)
- Concurrency with Monitoring & Control phase
- Session/checkpoint handling across long-running execution periods
