---
type: template
document_class: pm:StatusReport
phase: monitoring-control
standard: ISO 21502:2020
prince2_equivalent: Highlight Report
ontology_uri: https://stephen-mcelhose.github.io/process-assistant/pm/StatusReport
status: draft
---

# Status Report: {{project_name}} — {{reporting_period}}

> **Purpose:** Provides a regular update on stage progress for the Project Board, confirming
> the stage remains within tolerances and flagging any issues or risks that require attention
> before they escalate.
>
> **Produced in:** Monitoring & Control phase
> **Frequency:** As defined in the Communication Management Approach

---

## Reporting Period
<!-- maps to: dct:temporal -->

{{reporting_period}}

---

## Status Summary

### Time
<!-- maps to: pm:hasTolerance -->
<!-- On track / behind / ahead — state deviation from approved baseline. Avoid completion percentages. -->

{{status_time}}

### Cost
<!-- maps to: pm:hasTolerance -->
<!-- Actual spend vs. budget — state whether cost tolerance is at risk -->

{{status_cost}}

### Quality
<!-- maps to: pm:hasTolerance -->
<!-- Quality events, failed reviews, products awaiting sign-off -->

{{status_quality}}

### Scope
<!-- maps to: pm:hasTolerance -->
<!-- Scope intact or summary of agreed changes since last report -->

{{status_scope}}

### Benefits
<!-- maps to: pm:hasTolerance -->
<!-- Benefits realization on track per Business Case; note if deferred to closure -->

{{status_benefits}}

### Risk
<!-- maps to: pm:hasRisk -->
<!-- Overall risk exposure — net position improving or deteriorating -->

{{status_risk}}

---

## Work Packages

### Current Period
<!-- maps to: dct:description -->
<!-- List product names being delivered this period — not tasks or activities -->

{{work_packages_current}}

### Next Period
<!-- maps to: dct:description -->
<!-- Products planned to start in the next reporting period -->

{{work_packages_next}}

---

## Change Requests
<!-- maps to: dct:references -->
<!-- Pending or newly raised Change Requests — reference the Change Log; state 'None this period' if applicable -->

{{change_requests}}

---

## Key Risks and Issues
<!-- maps to: pm:hasRisk -->
<!-- Escalations only — items within the project manager's tolerance do not appear here -->
<!-- State 'No escalations this period' if nothing requires Project Board attention -->

{{key_risks_issues}}

---

*This document was produced in the Monitoring & Control phase per ISO 21502:2020 §8
and corresponds to the PRINCE2® Highlight Report management product
([prince2.wiki — Highlight Report](https://prince2.wiki/management-products/reports/highlight-report/)).*
