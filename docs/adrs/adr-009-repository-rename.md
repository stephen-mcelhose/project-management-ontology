---
type: decision
title: "ADR-009: Repository rename to process-assistant"
description: >
  Renames the GitHub repository from project-management-ontology to
  process-assistant. Keeps OWL namespace IRIs on the historical GitHub Pages
  path so existing RDF identity does not change. Defers a domains/ layout
  until a second domain is committed here.
timestamp: 2026-08-23T23:07:33Z
status: accepted
tags: [adr, naming, repository, ontology]
---

# ADR-009: Repository rename to process-assistant

**Status:** Accepted
**Date:** 2026-08-23
**Deciders:** Stephen McElhose

---

## Context

Issue [#61](https://github.com/stephen-mcelhose/process-assistant/issues/61)
noted that `project-management-ontology` names only the OWL layer and locks
the repo to PM. The README already describes a generic ontology-based process
assistant, with PM as the first domain.

[#61](https://github.com/stephen-mcelhose/process-assistant/issues/61) listed
`process-assistant-ontology` as the leading candidate and suggested deferring
until after M5. The chosen name is shorter: `process-assistant`. Action is
now, not after M5.

## Decision

The GitHub repository is `stephen-mcelhose/process-assistant`.

OWL and SHACL IRIs stay on
`https://stephen-mcelhose.github.io/project-management-ontology/`. Those
strings are identity, not a marketing URL. Changing them would rewrite every
`pm:` triple and every `maps_to` binding.

A `domains/{name}/` tree (PM under `domains/pm/`) is still the intended
layout when a second domain lands in this repo. This rename does not move
`ontology/`, `shapes/`, or `templates/`.

## Considered options

| Name | Why not |
| ---- | ------- |
| `process-ontology` | Too vague; drops the assistant |
| `ontology-agent-scaffold` | Awkward; over-weights the scaffold |
| `gate-driven-agent-scaffold` | Drops the ontology |
| `okf-process-agent` | OKF is a convention here, not the product |
| `process-assistant-ontology` | Accurate but longer than we need |
| `pm-ontology` | Still domain-locked |

## Consequences

- `github.com` URLs redirect from the old repo name.
- GitHub Pages for the new name is `…github.io/process-assistant/`. Published
  HTML may move; Turtle prefixes must not.
- Local checkout path is `~/repos/process-assistant`.
