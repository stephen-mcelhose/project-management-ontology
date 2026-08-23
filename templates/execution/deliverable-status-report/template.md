---
type: template
document_class: pm:DeliverableStatusReport
phase: execution
standard: ISO 21502:2020
prince2_equivalent: Checkpoint Report
ontology_uri: https://stephen-mcelhose.github.io/project-management-ontology/DeliverableStatusReport
status: draft
---

# Deliverable Status Report: {{work_package_reference}}

> **Purpose:** Enables the Team Manager to report progress on a Work Package to the Project
> Manager — comparing actual deliverable completion against the Team Plan and flagging any
> issues or risks requiring attention.
>
> **Produced in:** Execution phase (DIN 69901)
> **Depends on:** Project Schedule
> **Must be completed before:** Handover Document
> **Frequency:** As agreed in the Work Package Description

---

## Report Date
<!-- maps to: dct:created -->

{{report_date}}

---

## Reporting Period
<!-- maps to: dct:description -->
<!-- The start and end dates of the period this report covers. -->

**From:** {{reporting_period_start}}
**To:**   {{reporting_period_end}}

---

## Deliverables Completed This Period
<!-- maps to: pm:hasDeliverable -->
<!-- Products formally accepted during this reporting period. -->

| Deliverable | Product ID | Completion Date | Accepted By |
| ----------- | ---------- | --------------- | ----------- |
| {{completed_deliverable_1}} | {{completed_id_1}} | {{completed_date_1}} | {{accepted_by_1}} |

*If no deliverables were completed: state reason below.*

{{no_completions_reason}}

---

## Deliverables In Progress
<!-- maps to: pm:hasDeliverable -->
<!-- Current work-in-progress deliverables and their status. -->

| Deliverable | Product ID | Status      | % Complete | Notes |
| ----------- | ---------- | ----------- | ---------- | ----- |
| {{wip_deliverable_1}} | {{wip_id_1}} | {{wip_status_1}} | {{wip_pct_1}} | {{wip_notes_1}} |

---

## Planned Next Period
<!-- maps to: pm:hasDeliverable -->
<!-- Deliverables and activities expected to be completed in the next reporting period. -->

{{deliverables_planned_next_period}}

---

## Comparison to Plan
<!-- maps to: dct:description -->
<!-- How actual progress compares to the Team Plan. Note any deviations and their causes. -->

{{comparison_to_plan}}

---

## Issues and Risks
<!-- maps to: pm:hasRisk -->
<!-- Items requiring the Project Manager's attention. Include anything that could breach tolerances. -->

| # | Description | Potential Impact | Proposed Response |
| - | ----------- | ---------------- | ----------------- |
| 1 | {{issue_1}} | {{issue_1_impact}} | {{issue_1_response}} |

*If no issues or risks: state "No issues or risks to escalate this period."*

---

## Open Actions from Previous Reports
<!-- maps to: dct:description -->
<!-- Outstanding actions carried forward from prior Deliverable Status Reports. -->

| Action | Owner | Due Date | Status |
| ------ | ----- | -------- | ------ |
| {{action_1}} | {{action_1_owner}} | {{action_1_due}} | {{action_1_status}} |

*If this is the first report for this Work Package, state "No prior actions — first report."*

---

*This document was produced in the Execution phase per ISO 21502:2020 §8
and corresponds to the PRINCE2® Checkpoint Report management product
([prince2.wiki — Checkpoint Report](https://prince2.wiki/management-products/reports/checkpoint-report/)).*
