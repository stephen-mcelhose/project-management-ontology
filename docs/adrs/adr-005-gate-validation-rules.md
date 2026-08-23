---
type: decision
title: "ADR-005: Gate Validation Rules Schema"
description: >
  Defines a controlled vocabulary of six validation_rules: keys for the
  instructions.yaml gate schema. Keys express programmatically checkable
  constraints alongside the existing prose validation: field, enabling
  deterministic validation tooling and JSON Schema enforcement (issue #47).
  Establishes the amendment process for extending the key vocabulary.
timestamp: 2026-08-24T00:00:00Z
status: accepted
tags: [adr, artifact-layer, gate-schema, instructions-yaml, validation]
---

# ADR-005: Gate Validation Rules Schema

**Status:** Accepted  
**Date:** 2026-08-24  
**Deciders:** Stephen McElhose  
**Closes:** Issue #46 (schema decision; gate annotation tracked separately)

---

## Context

Gates in `instructions.yaml` carry a `validation:` prose field describing
constraints that an LLM interprets during a session. These constraints cannot
be unit-tested, linted, or asserted without an LLM in the loop.

A full inventory of all `validation:` fields across the template library
(~85 fields, 14 documents, all phases) reveals that roughly a third express
constraints that are programmatically checkable — minimum item counts, closed
enumerations, identity uniqueness, named-individual requirements, structural
part requirements, format rules, and cross-document consistency checks. The
remaining two-thirds are qualitative guidance ("must be concise", "avoid
vague language", "must be testable") that cannot be expressed as a rule.

The JSON Schema tooling planned in issue #47 (`instructions-schema.json`)
can formally enumerate and enforce a closed key vocabulary, making
`validation_rules:` a first-class schema concern alongside `type:`
(ADR-004) and `deferred_value:` (issue #45).

---

## Decision

Add an optional `validation_rules:` block to the gate schema. The prose
`validation:` field is **always preserved** — `validation_rules:` is
additive, not a replacement.

### Key vocabulary

Six keys in five categories:

#### Identity

| Key | Value type | Meaning |
|-----|------------|---------|
| `unique: true` | boolean | Value must not be reused across entries in the same register. Duplicate IDs break traceability. |

#### Enumeration

| Key | Value type | Meaning |
|-----|------------|---------|
| `allowed_values: [...]` | list of strings | Value must be exactly one of the listed options (closed set). |

#### Structural

| Key | Value type | Meaning |
|-----|------------|---------|
| `min_items: N` | positive integer | Output must contain at least N discrete, enumerable items or options. |
| `named_individual: true` | boolean | Value must be a specific named person; a role, team, or department name alone is insufficient. |
| `required_parts: [...]` | list of strings | Structured output must explicitly address each named part. |

#### Format

| Key | Value type | Meaning |
|-----|------------|---------|
| `format: currency` | string literal | Value must be a numeric amount with an explicit currency symbol (e.g. `€120,000`). Only `currency` is a valid code — date format is covered by `type: date` (ADR-004). |

#### Cross-document

| Key | Value type | Meaning |
|-----|------------|---------|
| `references_document: <doc-name>` | string | Output must reference or be consistent with the named sibling document (kebab-case document ID matching the template pack folder name). |

### Coverage

These keys cover gates where at least one constraint is programmatically
expressible. Gates whose `validation:` text is purely qualitative receive
no `validation_rules:` block — the prose is sufficient there.

Inventory of qualifying gates by key:

| Key | Gates |
|-----|-------|
| `unique: true` | change-request/change\_request\_id, quality-audit-report/audit\_id, risk-register/entry\_id, decision-log/entry\_id, issue-log/entry\_id |
| `allowed_values` | change-request/issue\_type, quality-audit-report/result, risk-register/risk\_type, issue-log/issue\_type |
| `min_items` | stakeholder-register/stakeholders (≥3), change-request/recommended\_options (≥2), risk-management-plan/probability\_scale (≥3), risk-management-plan/impact\_scale (≥3), project-schedule/milestones (≥3) |
| `named_individual` | project-proposal/sponsor, project-charter/approval\_authority, work-package-description/team\_manager, risk-register/risk\_owner, requirement-specification/approver |
| `required_parts` | risk-register/risk\_description ([cause, event, impact]), quality-management-plan/quality\_approach ([planning, control, assurance]), project-management-plan/tolerances ([time, cost, quality, scope, benefits, risk]) |
| `format: currency` | cost-estimate/total\_budget |
| `references_document` | communication-plan/stakeholder\_analysis (stakeholder-register), resource-plan/human\_resources (work-breakdown-structure), quality-audit-report/product\_id\_and\_name (product-register), quality-audit-report/quality\_method (quality-management-plan), change-log/entry\_id (change-request) |

### YAML usage

```yaml
# Enumeration — closed value set
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

# Identity — unique identifier
- id: entry_id
  order: 1
  type: identifier
  prompt: "What is the unique identifier for this risk? (e.g. RISK-001)"
  fills: "## Risk Entry"
  maps_to: dct:identifier
  required: true
  validation: "Must follow a consistent scheme (e.g. RISK-NNN). Never reuse an ID."
  validation_rules:
    unique: true

# Structural — minimum item count
- id: stakeholders
  order: 2
  type: list
  prompt: "List every stakeholder..."
  fills: "## Stakeholder Analysis"
  maps_to: pm:RoleAssignment
  required: true
  validation: "Must list at least 3 distinct stakeholders. Avoid vague entries."
  validation_rules:
    min_items: 3

# Structural — named parts required
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

# Cross-document — consistency with sibling document
- id: stakeholder_analysis
  order: 3
  type: table
  prompt: "For each stakeholder, identify interest, influence, and engagement levels..."
  fills: "## Stakeholder Analysis"
  maps_to: pm:RoleAssignment
  required: true
  validation: "All stakeholders from the Stakeholder Register must appear."
  validation_rules:
    references_document: stakeholder-register
```

### Rules

- `validation_rules:` is optional. Only add it when at least one constraint
  can be expressed using the above keys.
- Multiple keys may appear on one gate (e.g. `unique: true` plus
  `allowed_values:` if the value must be unique AND from a fixed set).
- The prose `validation:` field must always accompany `validation_rules:` —
  the rules supplement human-readable text, not replace it.
- Keys not in the vocabulary are not valid; they will be rejected by the JSON
  Schema (#47). To propose a new key, follow the amendment process below.

---

## Amendment process

The vocabulary is intentionally small. New keys require deliberate
justification.

### Adding a key

A new key is warranted when:
- At least three real gates across different documents need it, **and**
- No existing key adequately expresses the constraint, **and**
- The constraint is programmatically checkable without an LLM.

Steps:
1. Open a GitHub issue: `artifact layer: propose validation_rules key '<name>'`.
   Include the key name, value type, a one-line definition, and the three
   qualifying gates.
2. If an existing key covers the case, close the issue.
3. If the key is warranted: amend this ADR (add to the key table and
   inventory, append to Amendment History), update `instructions-schema.json`
   (#47) to include the new key, and annotate the qualifying gates.

### Retiring a key

1. Confirm no gate uses the key.
2. Amend this ADR to mark it deprecated with a date.
3. Update `instructions-schema.json` (#47) to remove or deprecate the key.

---

## Consequences

- An agent encountering `validation_rules: { min_items: 3 }` can assert the
  constraint without interpreting prose — useful for structured agent pipelines
  and automated checks.
- `instructions-schema.json` (#47) gains a formal enum of valid keys,
  preventing ad-hoc rule keys from accumulating silently.
- Approximately 25 gates across 14 documents receive `validation_rules:`
  blocks. The remaining ~60 `validation:` fields stay prose-only.
- The prose `validation:` field remains the primary contract for LLM agents.
  `validation_rules:` is a machine-readable supplement, not the authoritative
  source.

---

## References

- Issue #46 — Artifact layer: add structured validation rules alongside prose
- Issue #47 — Tooling: add instructions-schema.json
- ADR-004 — Gate Output Type System (sibling schema decision for `type:`)
- `docs/processes/defining-document-templates.md` — Step 3b gate schema

---

## Amendment history

*No amendments yet.*
