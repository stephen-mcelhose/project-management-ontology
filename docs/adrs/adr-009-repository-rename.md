---
type: decision
title: "ADR-009: Rename to process-assistant, rebase the pm: namespace, adopt domains/pm/"
description: >
  Renames the GitHub repository from project-management-ontology to
  process-assistant, rebases every OWL/SHACL IRI onto the process-assistant
  GitHub Pages path, and moves the PM domain under domains/pm/.
timestamp: 2026-08-23T23:07:33Z
status: accepted
tags: [adr, naming, repository, ontology, namespace, layout]
---

# ADR-009: Rename to process-assistant, rebase the pm: namespace, adopt domains/pm/

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

The same reasoning applies to the namespace and the directory layout. OWL IRIs
are identity, so there is a real argument for freezing them — but only where
something external depends on them. Nothing does: there is no published Pages
site anyone dereferences, and no third-party graph imports `pm:`. The only
consumer is this repository. That makes the rebase a mechanical rewrite paid
once, now, while it is cheap. Deferring it means every triple keeps pointing
at a name the project has abandoned, and the argument for deferring only ever
gets stronger.

## Decision

**Repository.** The GitHub repository is `stephen-mcelhose/process-assistant`.

**Namespace.** The `pm:` base is
`https://stephen-mcelhose.github.io/process-assistant/pm/`. The ontology IRI,
`owl:versionIRI`, `vann:preferredNamespaceUri`, and the `phases/`, `packages/`,
and `shapes/` sub-namespaces all rebase onto it. The prefix label stays `pm:` —
it is a local abbreviation, not identity.

The `/pm/` segment is deliberate. A second domain gets its own base
(`…/process-assistant/{domain}/`) and cannot collide with PM local names. A
flat base would have forced every future domain to either share PM's term
space or break the pattern.

`instructions-schema.json` keeps a domain-neutral `$id` at
`…/process-assistant/schemas/`. It describes the gate file format the engine
reads, which is not PM-specific.

**Layout.** The PM domain lives under `domains/pm/`:

```
domains/pm/
  ontology/
  shapes/
  templates/
```

`tools/`, `agent/`, and `docs/` stay at the root. They are domain-agnostic:
the engine reads a manifest path, and nothing in it knows about project
management.

## Considered options

### Name

| Name | Why not |
| ---- | ------- |
| `process-ontology` | Too vague; drops the assistant |
| `ontology-agent-scaffold` | Awkward; over-weights the scaffold |
| `gate-driven-agent-scaffold` | Drops the ontology |
| `okf-process-agent` | OKF is a convention here, not the product |
| `process-assistant-ontology` | Accurate but longer than we need |
| `pm-ontology` | Still domain-locked |

### Namespace base

| Base | Verdict |
| ---- | ------- |
| `…github.io/project-management-ontology/` (freeze) | Rejected. Preserves identity for a consumer that does not exist, at the cost of naming every triple after an abandoned repo |
| `…github.io/process-assistant/` (flat) | Rejected. One segment shorter, but the second domain either shares PM's term space or breaks the pattern |
| `…github.io/process-assistant/pm/` (domain-scoped) | **Chosen.** Mirrors `domains/pm/`; every future domain gets a sibling base |

## Consequences

- Every Turtle prefix, `entry.yaml` `ontology_class`, `template.md`
  `ontology_uri`, `_manifest.yaml` `ontology_phase`, and namespace constant in
  `tools/` is rewritten.
- `maps_to` CURIEs are unaffected. They are prefix-relative, so `pm:hasSponsor`
  means the new base the moment the prefix is rebound.
- Old IRIs do not resolve and are not aliased. No `owl:sameAs` or
  `owl:deprecated` bridge is published — there is no external graph to bridge
  for. Any document or graph generated before this ADR must be regenerated.
- Paths move: `Makefile` targets, the agent's `TEMPLATES_DIR` default, eval
  fixtures, phase agent prompts, and the template-authoring guides all point
  at `domains/pm/`.
- `github.com` URLs redirect from the old repo name.
- GitHub Pages for the new name is `…github.io/process-assistant/`, so PM
  vocabulary documentation publishes under `…/process-assistant/pm/` —
  published HTML and IRI resolution line up.
- Local checkout path is `~/repos/process-assistant`.
