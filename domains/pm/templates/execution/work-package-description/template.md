---
type: template
document_class: pm:WorkPackageDescription
phase: execution
standard: ISO 21502:2020
prince2_equivalent: Work Package
ontology_uri: https://stephen-mcelhose.github.io/process-assistant/pm/WorkPackageDescription
status: draft
---

# Work Package Description: {{work_package_title}}

> **Purpose:** Provides the Team Manager with all information needed to deliver a defined body
> of work in a controlled, agreed manner — specifying the deliverables, quality criteria,
> tolerances, and reporting arrangements.
>
> **Produced in:** Execution phase (DIN 69901)
> **Depends on:** Work Breakdown Structure, Project Schedule
> **Must be completed before:** Deliverable Status Report

---

## Work Package Reference
<!-- maps to: dct:identifier -->
<!-- Unique identifier traceable to the Work Breakdown Structure. -->

**Work Package ID:** {{work_package_id}}

---

## Team Manager / Assigned Team
<!-- maps to: pm:RoleAssignment -->
<!-- The named individual or team responsible for delivering this Work Package. -->

**Name:** {{team_manager_name}}
**Role:** {{team_manager_role}}

---

## Date of Agreement
<!-- maps to: dct:created -->
<!-- The date this Work Package was formally agreed between the Project Manager and Team Manager. -->

{{date_of_agreement}}

---

## Description of Work
<!-- maps to: dct:description -->
<!-- Describe all tasks and activities the team must complete. Be specific enough to start without further clarification. -->

{{work_description}}

---

## Deliverables
<!-- maps to: pm:hasDeliverable -->
<!-- List every product or artifact this Work Package must produce. Reference Product Descriptions. -->

| Deliverable Name | Product ID | Description of Done |
| ---------------- | ---------- | ------------------- |
| {{deliverable_1_name}} | {{deliverable_1_id}} | {{deliverable_1_done}} |

---

## Techniques and Methods
<!-- maps to: pm:projectApproach -->
<!-- Mandatory tools, standards, or methods the team must apply during delivery. -->

{{techniques_and_methods}}

---

## Quality Criteria and Acceptance
<!-- maps to: pm:acceptanceCriteria -->
<!-- Specific, testable criteria each deliverable must satisfy before acceptance. -->

| Deliverable | Quality Criterion | Source / Reference |
| ----------- | ----------------- | ------------------ |
| {{deliverable_1_name}} | {{quality_criterion_1}} | {{quality_source_1}} |

---

## Agreed Tolerances
<!-- maps to: pm:hasTolerance -->
<!-- Permitted deviations for this Work Package before escalation is required. -->

| Dimension | Tolerance |
| --------- | --------- |
| Time      | {{tolerance_time}} |
| Cost      | {{tolerance_cost}} |
| Scope     | {{tolerance_scope}} |

---

## Reporting Arrangements
<!-- maps to: dct:description -->
<!-- Frequency, format, and distribution of Deliverable Status Reports for this Work Package. -->

{{reporting_arrangements}}

---

## Escalation Path
<!-- maps to: pm:hasRisk -->
<!-- How to escalate issues or risks that exceed the agreed tolerances. -->

**Escalation contact:** {{escalation_contact}}
**Trigger:** {{escalation_trigger}}
**Response time:** {{escalation_response_time}}

---

## Interfaces
<!-- maps to: pm:RoleAssignment -->
<!-- Other teams, people, or systems this Work Package must coordinate with. -->

| Interface | Why Coordination Is Needed | Communication Channel |
| --------- | -------------------------- | --------------------- |
| {{interface_1}} | {{interface_1_reason}} | {{interface_1_channel}} |

---

*This document was produced in the Execution phase per ISO 21502:2020 §8
and corresponds to the PRINCE2® Work Package management product
([prince2.wiki — Work Package](https://prince2.wiki/management-products/baselines/work-package/)).*
