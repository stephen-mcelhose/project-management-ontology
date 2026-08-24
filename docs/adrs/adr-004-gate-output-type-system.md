---
type: decision
title: "ADR-004: Gate Output Type System"
description: >
  Defines a controlled vocabulary of seven gate output types — scalar, block,
  and section categories — that annotate the type: field in instructions.yaml
  gate definitions. Types are modelled as OWL named individuals in the pm:
  namespace following the existing named individuals pattern. Establishes the
  amendment process for adding or retiring types.
timestamp: 2026-08-24T00:00:00Z
status: accepted
tags: [adr, artifact-layer, gate-schema, instructions-yaml, ontology]
---

# ADR-004: Gate Output Type System

**Status:** Accepted  
**Date:** 2026-08-24  
**Deciders:** Stephen McElhose  
**Closes:** Issue #44

---

## Context

Gates in `instructions.yaml` produce varied output shapes — a short inline
value (`project_name`), a bullet list (`objectives`), a Markdown table
(`pm_team_structure`), a structured multi-section block (`wbs`) — but no
`type:` field declares this. An agent filling a template must infer the
expected rendering format from prompt text and placeholder patterns.

This causes agent ambiguity and makes it impossible for a JSON Schema (#47)
to enumerate valid values for the field.

---

## Decision

### Type vocabulary

Seven types, in three categories:

#### Scalar — single atomic value

Fills a `{{placeholder}}` token inline. The agent produces one value, not a
Markdown block.

| `type:`      | Description                                             |
|--------------|---------------------------------------------------------|
| `string`     | Free-form inline text (project name, role name, etc.)  |
| `date`       | ISO 8601 calendar date — YYYY-MM-DD                    |
| `identifier` | Unique code with a naming convention (e.g. CR-001)     |

#### Block — structured Markdown content

Fills an entire `## Section`. The agent produces a Markdown block.

| `type:`  | Description                                                    |
|----------|----------------------------------------------------------------|
| `prose`  | Narrative paragraph(s), no required internal structure         |
| `list`   | Ordered or unordered enumeration of discrete items             |
| `table`  | Markdown table with defined column headers                     |

#### Section — structured prose with internal organisation

| `type:`   | Description                                                           |
|-----------|-----------------------------------------------------------------------|
| `section` | Prose that has its own internal sub-structure (headings, nested blocks, embedded tables). Free-form prose with no sub-structure is `prose`. |

**Boundary: `prose` vs `section`** — If the agent writes two paragraphs, use
`prose`. If the output requires its own internal headings or a combination of
multiple block types (e.g. a WBS with hierarchy, or an embedded management
approach with sub-sections), use `section`.

**Boundary: `string` vs `prose`** — If `fills:` contains a `{{placeholder}}`
token, the type is scalar (`string`, `date`, or `identifier`). If `fills:`
names a `## Section`, the type is a block or section.

### Ontological grounding

Types are defined as OWL named individuals of the class `:GateOutputType` in
`domains/pm/ontology/modules/document.ttl`, following the named individuals pattern used
for `:ProjectStatus`, `:DocumentStatus`, and `:TaskStatus`.

`:GateOutputType` is a vocabulary class only. Gates are not modelled as OWL
instances; there is no `:gateOutputType` property on any domain class.

### YAML usage

```yaml
- id: project_name
  order: 1
  type: string
  prompt: "What is the project name?"
  fills: "## Project Name"
  maps_to: dct:title
  required: true

- id: objectives
  order: 2
  type: list
  prompt: "List the project objectives…"
  fills: "## Project Objectives"
  maps_to: proj:hadObjective
  required: true

- id: pm_team_structure
  order: 9
  type: table
  prompt: "Describe the project management team structure…"
  fills: "## Project Management Team Structure"
  maps_to: pm:RoleAssignment
  required: true
```

`type:` is optional for now. Gates without it are unclassified; all gates
should be annotated before M5 (ADK agent build).

### Validation rules (`validation_rules:`)

Gates with a `validation:` prose field may also carry a `validation_rules:`
block expressing the same constraint in a machine-readable form. The prose
field is **always preserved** — `validation_rules:` is additive.

#### Key vocabulary

Six keys, in four categories:

**Identity**

| Key | Value type | Meaning |
|-----|------------|---------|
| `unique: true` | boolean | Value must not be reused across entries in the same register. Duplicate IDs break traceability. |

**Enumeration**

| Key | Value type | Meaning |
|-----|------------|---------|
| `allowed_values: [...]` | list of strings | Value must be exactly one of the listed options. |

**Structural**

| Key | Value type | Meaning |
|-----|------------|---------|
| `min_items: N` | integer | Output must contain at least N discrete, enumerable items. |
| `named_individual: true` | boolean | Value must be a specific named person; a role, team, or department name alone is insufficient. |
| `required_parts: [...]` | list of strings | Structured output must explicitly address each named part (e.g. `[cause, event, impact]` for a risk description). |

**Format**

| Key | Value type | Meaning |
|-----|------------|---------|
| `format: currency` | string literal | Value must be a numeric amount with an explicit currency symbol (e.g. `€120,000`). |

**Cross-document**

| Key | Value type | Meaning |
|-----|------------|---------|
| `references_document: <doc-name>` | string | Output must reference or be fully consistent with the named sibling document (kebab-case document ID). |

#### Coverage

These six keys cover gates where at least one constraint is programmatically
expressible. Gates whose `validation:` text is purely qualitative
(conciseness, testability, non-vagueness) receive no `validation_rules:`
block — prose alone is sufficient there.

Inventory of gates that qualify, by key:

| Key | Gates |
|-----|-------|
| `unique: true` | change-request/change\_request\_id, quality-audit-report/audit\_id, risk-register/entry\_id, decision-log/entry\_id, issue-log/entry\_id |
| `allowed_values` | change-request/issue\_type, quality-audit-report/result, risk-register/risk\_type, issue-log/issue\_type |
| `min_items` | stakeholder-register/stakeholders (≥3), change-request/recommended\_options (≥2), risk-management-plan/probability\_scale (≥3), risk-management-plan/impact\_scale (≥3), project-schedule/milestones (≥3) |
| `named_individual` | project-proposal/sponsor, project-charter/approval\_authority, work-package-description/team\_manager, risk-register/risk\_owner, requirement-specification/approver |
| `required_parts` | risk-register/risk\_description ([cause, event, impact]), quality-management-plan/quality\_approach ([planning, control, assurance]), project-management-plan/tolerances ([time, cost, quality, scope, benefits, risk]) |
| `format: currency` | cost-estimate/total\_budget |
| `references_document` | communication-plan/stakeholder\_analysis, resource-plan/human\_resources, quality-audit-report/product\_id\_and\_name, quality-audit-report/quality\_method, change-log/entry\_id |

#### YAML usage

Multiple keys may appear on one gate:

```yaml
- id: stakeholders
  order: 2
  type: list
  prompt: "List every stakeholder..."
  fills: "## Stakeholder Analysis"
  maps_to: pm:RoleAssignment
  required: true
  validation: "Must list at least 3 distinct stakeholders. Avoid vague entries like 'management'."
  validation_rules:
    min_items: 3

- id: risk_type
  order: 2
  type: string
  prompt: "Is this a Threat or an Opportunity?"
  fills: "## Risk Type"
  maps_to: dct:description
  required: true
  validation: "Must be either 'Threat' or 'Opportunity'."
  validation_rules:
    allowed_values: [Threat, Opportunity]

- id: entry_id
  order: 1
  type: identifier
  prompt: "What is the unique identifier for this risk?"
  fills: "## Risk Entry"
  maps_to: dct:identifier
  required: true
  validation: "Must follow a consistent scheme (e.g. RISK-NNN). Never reuse an ID."
  validation_rules:
    unique: true

- id: risk_description
  order: 3
  type: prose
  prompt: "Describe the risk using the PRINCE2 three-part format..."
  fills: "## Risk Description"
  maps_to: dct:description
  required: true
  validation: "All three parts (cause, event, impact) must be present."
  validation_rules:
    required_parts: [cause, event, impact]
```

#### Rules

- `validation_rules:` is optional. Only add it when at least one constraint
  is expressible with the keys above.
- The prose `validation:` field must always be present alongside
  `validation_rules:` — the rules supplement, not replace, the human-readable text.
- Keys not in the vocabulary are not valid. To propose a new key, follow the
  amendment process below.

---

## Amendment process

The vocabularies are intentionally small and closed. Extensions require
deliberate justification.

### Adding a gate output type

A new type is warranted when:
- At least three real gates across different documents need it, **and**
- No existing type adequately describes the output shape, **and**
- The distinction changes agent behaviour (not just a stylistic preference).

Steps:
1. Open a GitHub issue: `artifact layer: propose gate type '<name>'`. Include
   the proposed local name, a one-line definition, and the three gates.
2. If an existing type covers the case, close the issue and annotate the gates.
3. If a new type is warranted: amend this ADR (add to the vocabulary table,
   update boundary notes, append to Amendment History below).
4. Add the named individual to `domains/pm/ontology/modules/document.ttl`.
5. Update `instructions-schema.json` (#47) to include the new valid value.
6. Annotate all existing gates that match the new type.

### Retiring a gate output type

1. Confirm no gate uses the type.
2. Mark the individual `owl:deprecated true` in `document.ttl`. Do not
   delete — IRIs must remain dereferenceable.
3. Amend this ADR to mark the type deprecated with a date.

### Clarifying a type definition

Minor wording changes that do not reclassify any gate: commit to this file
and the ontology `skos:definition` directly. Substantive changes that would
move gates between types require an issue and an entry in Amendment History.

### Adding a `validation_rules:` key

A new key is warranted when:
- At least three real gates across different documents need it, **and**
- No existing key adequately expresses the constraint, **and**
- The constraint is programmatically checkable without an LLM.

Steps:
1. Open a GitHub issue: `artifact layer: propose validation_rules key '<name>'`.
   Include the proposed key, its value type, a one-line definition, and the three gates.
2. If an existing key covers the case, close the issue.
3. If the key is warranted: amend this ADR (add to the key table and inventory),
   update `instructions-schema.json` (#47), and annotate the qualifying gates.

### Retiring a `validation_rules:` key

1. Confirm no gate uses the key.
2. Amend this ADR to mark it deprecated with a date.
3. Update `instructions-schema.json` (#47) to remove or deprecate the key.

---

## Consequences

- An agent receiving `type: table` knows to produce a Markdown table without
  inferring it from the prompt.
- The JSON Schema (#47) can enumerate valid `type:` values from the controlled
  vocabulary.
- Types are formally grounded in the `pm:` namespace, consistent with all
  other controlled vocabularies in this ontology.
- One-time annotation effort across all existing gates (~150 gates, all
  phases). Tracked in issue #44.

---

## References

- Issue #44 — Artifact layer: annotate gate output type
- Issue #47 — Tooling: add instructions-schema.json
- `domains/pm/ontology/modules/document.ttl` — `:GateOutputType` vocabulary
- `docs/processes/defining-document-templates.md` — Step 3b gate schema
- ADR-003 — Phase Manifest Pattern

---

## Amendment history

*No amendments yet.*
