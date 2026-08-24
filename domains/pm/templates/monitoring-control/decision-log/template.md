---
type: template
document_class: pm:DecisionLog
phase: monitoring-control
standard: ISO 21502:2020
prince2_equivalent: Daily Log
ontology_uri: https://stephen-mcelhose.github.io/process-assistant/pm/DecisionLog
status: draft
---

# Decision Log Entry: {{entry_id}}

> **Purpose:** Documents a single key decision made during the project, recording the context,
> alternatives considered, rationale, and current status to ensure transparency and
> accountability across the project lifecycle.
>
> **Produced in:** Monitoring & Control phase
> **Living document:** Opened at project initiation; one entry per significant decision.
>
> **Note:** Extends the PRINCE2 Daily Log with formal decision tracking per ISO 21502:2020 §8.
> Decisions that affect the project baseline should also trigger a Change Request.

---

## Decision Entry
<!-- maps to: dct:identifier -->

**Decision ID:** {{entry_id}}

---

## Decision Date
<!-- maps to: dct:created -->

{{decision_date}}

---

## Decision Maker
<!-- maps to: dct:creator -->
<!-- Named individual or governance body (e.g. Project Board, Change Authority, Project Manager) -->

{{decision_maker}}

---

## Decision Title
<!-- maps to: dct:title -->

{{decision_title}}

---

## Context
<!-- maps to: dct:description -->
<!-- What situation required this decision to be made? -->

{{context}}

---

## Alternatives Considered
<!-- maps to: dct:description -->
<!-- At least two options evaluated, including 'do nothing' where applicable -->

{{alternatives_considered}}

---

## Decision Made
<!-- maps to: dct:description -->

{{decision}}

---

## Rationale
<!-- maps to: dct:description -->
<!-- Why was this option chosen over the alternatives? -->

{{rationale}}

---

## Impact
<!-- maps to: dct:description -->
<!-- Effect on project baseline (time, cost, scope, benefits, risk) -->
<!-- If this decision affects the baseline, a Change Request should also be raised -->

{{impact}}

---

## Status
<!-- maps to: pm:documentStatus -->
<!-- Active / Superseded / Reversed -->

{{decision_status}}

---

## Related Items
<!-- maps to: dct:references -->
<!-- Issue Log IDs, Change Request IDs, or Risk Register IDs. State 'None' if not applicable. -->

{{related_items}}

---

*This document was produced in the Monitoring & Control phase per ISO 21502:2020 §8
and corresponds to the PRINCE2® Daily Log management product
([prince2.wiki — Daily Log](https://prince2.wiki/management-products/project-log/daily-log/)).*
