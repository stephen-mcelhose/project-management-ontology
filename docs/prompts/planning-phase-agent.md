---
type: agent-prompt
title: Planning Phase Agent Prompt
description: >
  Placeholder prompt describing the Planning Phase scope and artifact structure.
  The gate-level protocol lives in each document's instructions.yaml.
  Revisit when building the ADK agent (issue #39). See ADR-002.
phase: planning
status: draft
tags: [prompt, agent, planning]
timestamp: 2026-08-23T00:00:00Z
see_also: docs/adrs/adr-002-phase-agent-prompts.md
---

# Planning Phase Agent Prompt

> **Status: Placeholder.**
> This prompt describes intent and structure. It is not a finished agent specification.
> The gate-level protocol for each document lives in its `instructions.yaml`.
> Revisit when building the ADK agent (issue #39) — see ADR-002.

---

## Phase Purpose

The Planning Phase translates the authorised project (Initiation outputs) into a
concrete, executable plan. It produces the schedule, resource allocation, cost
estimate, and management approach documents that govern Execution. No work should
begin until the core planning documents are in place.

---

## Documents (in dependency order)

The phase manifest (`domains/pm/templates/planning/_manifest.yaml`) is the authoritative index.

| Order | Document                 | Key question it answers                              |
| ----- | ------------------------ | ---------------------------------------------------- |
| 1     | Project Management Plan  | How will this project be governed end-to-end?        |
| 2     | Work Breakdown Structure | What is the full scope, broken into deliverables?    |
| 3     | Project Schedule         | When does each deliverable get done?                 |
| 4     | Resource Plan            | Who does what, and when are they needed?             |
| 5     | Cost Estimate            | What will it cost?                                   |
| 6     | Risk Management Plan     | How will risks be identified and handled?            |
| 7     | Quality Management Plan  | What quality standards apply, and how are they met? |
| 8     | Communication Plan       | How and when do we communicate with stakeholders?    |

Documents 1–5 form a linear chain. Documents 6–8 run off the Project Management
Plan in parallel once it is complete.

---

## How to Use the Artifact Files

```
domains/pm/templates/planning/{document}/
  entry.yaml          ← metadata: standard citations, dependency chain
  instructions.yaml   ← ordered gates: what to ask, what to fill
  template.md         ← the output scaffold with {{placeholders}}
```

Work through gates in `order` sequence per `instructions.yaml`. A document is
complete when all `required: true` gates in `completion.required_gates` are filled.

---

## Shared Context

`project_name` was captured in the Initiation Phase (Project Proposal). Do not
re-ask. See `domains/pm/templates/planning/_manifest.yaml` under `shared_context`.

---

## Phase Entry Condition

The Planning Phase begins after the Initiation Package is complete:
- Project Charter signed off (authorises the project and names the PM)
- Requirement Specification approved (defines the product scope)

---

## Phase Exit

All eight documents at `output_status: draft`, reviewed by the project sponsor
and project manager. The next phase is Execution; entry point is the
Work Package Description.

---

## What This Prompt Does Not Define

Deliberately left to the agent implementation (issue #39):
- Conversation mechanics and gate sequencing across documents
- Parallel vs. sequential document handling (docs 6–8 can run in parallel)
- Session/checkpoint handling
- Output format (Markdown, RDF triples, or both)
