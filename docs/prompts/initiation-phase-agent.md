---
type: agent-prompt
title: Initiation Phase Agent Prompt
description: >
  Placeholder prompt describing the Initiation Phase scope and artifact structure
  for an agent or LLM helping a project team complete Initiation Phase documents.
  This is a scaffold — the gate-level protocol lives in each document's
  instructions.yaml. Revisit when building the ADK agent (issue #39).
phase: initiation
status: draft
tags: [prompt, agent, initiation]
timestamp: 2026-08-23T00:00:00Z
see_also: docs/adrs/adr-002-phase-agent-prompts.md
---

# Initiation Phase Agent Prompt

> **Status: Placeholder.**  
> This prompt describes intent and structure. It is not a finished agent specification.
> The gate-level protocol for each document lives in its `instructions.yaml`.
> Revisit and extend this prompt when building the ADK agent (issue #39) or an
> orchestrator — see ADR-002 for rationale.

---

## Phase Purpose

The Initiation Phase establishes that the project is worth doing, secures formal
authorization, and produces the foundational documents that all subsequent phases
depend on. No Planning or Execution work should begin until the Initiation Package
is complete.

---

## Documents (in dependency order)

The phase manifest (`templates/initiation/_manifest.yaml`) is the authoritative
index. The sequence is:

| Order | Document                 | Key question it answers                        |
| ----- | ------------------------ | ---------------------------------------------- |
| 1     | Project Proposal         | Is this project idea worth investigating?       |
| 2     | Business Case            | Does the investment make sense?                |
| 3     | Project Charter          | Is the project formally authorized?            |
| 4     | Stakeholder Register     | Who is affected, and how do we communicate?    |
| 5     | Requirement Specification | What must the final product be and do?         |

Each document must be substantially complete before the next one begins
(`pm:hasHardDependency`). The gate sequence for each document is defined in its
`instructions.yaml`.

---

## How to Use the Artifact Files

For each document, three files define the agent's job:

```
templates/initiation/{document}/
  entry.yaml          ← metadata: standard citations, dependency chain, phase order
  instructions.yaml   ← ordered gates: what to ask, what to fill, ontology mappings
  template.md         ← the output scaffold with {{placeholders}}
```

The `instructions.yaml` is the primary protocol. Each gate specifies:
- `prompt` — the question to put to the user
- `fills` — which template section the answer populates
- `maps_to` — the ontology property the answer asserts
- `required` — whether the document is incomplete without it
- `validation` / `guidance` — rules for accepting or challenging an answer

Work through gates in `order` sequence. A document is complete when all
`required: true` gates in its `completion.required_gates` list are filled with
non-placeholder content.

---

## Shared Context

Certain fields are captured once and apply to every document in the phase.
Do not ask for them again once collected. See `templates/initiation/_manifest.yaml`
under `shared_context` for the authoritative list.

---

## Phase Exit

The Initiation Phase is complete when all five documents are at `output_status: draft`
and have been reviewed by the project sponsor. The next document in the chain is
the Project Management Plan (Planning Phase).

---

## What This Prompt Does Not Define

Deliberately left to the agent implementation (issue #39):

- Conversation mechanics (one question at a time vs. batched)
- Session/checkpoint handling (how to resume mid-document)
- Narrative extraction (how to pull structured answers from prose)
- Validation retry logic (how many times to push back before deferring)
- Output format (rendered Markdown, RDF triples, or both)

These are agent concerns, not artifact concerns.
