---
type: template
document_class: pm:ProjectSchedule
phase: planning
standard: ISO 21502:2020
prince2_equivalent: Plan (schedule component)
ontology_uri: https://stephen-mcelhose.github.io/process-assistant/pm/ProjectSchedule
status: draft
---

# Project Schedule: {{project_name}}

> **Purpose:** Defines the planned sequence of project activities, their durations,
> and key milestones, forming the project time baseline.
>
> **Produced in:** Planning phase (DIN 69901)
> **Depends on:** Work Breakdown Structure
> **Must be completed before:** Resource Plan, Work Package Descriptions, Deliverable Status Reports

---

## Schedule Overview
<!-- maps to: dct:description -->
<!-- Describe what this schedule covers and what scheduling method is used. -->

{{schedule_description}}

---

## Timeline
<!-- maps to: pm:plannedStartDate, pm:plannedEndDate -->

| | Date |
| --- | --- |
| **Planned Start** | {{project_start_date}} |
| **Planned End**   | {{project_end_date}} |
| **Total Duration** | {{total_duration}} |

---

## Key Milestones
<!-- maps to: pm:hasMilestone -->

| # | Milestone | Target Date | Gating Event |
| - | --------- | ----------- | ------------ |
| 1 | {{milestone_1_name}} | {{milestone_1_date}} | {{milestone_1_trigger}} |
| 2 | {{milestone_2_name}} | {{milestone_2_date}} | {{milestone_2_trigger}} |
| 3 | {{milestone_3_name}} | {{milestone_3_date}} | {{milestone_3_trigger}} |

---

## Activity Schedule
<!-- maps to: pm:hasTask -->
<!-- List all scheduled activities, linked to WBS work packages. -->

| ID | Activity | Start | End | Predecessor | Responsible |
| -- | -------- | ----- | --- | ----------- | ----------- |
| {{act_1_id}} | {{act_1_name}} | {{act_1_start}} | {{act_1_end}} | — | {{act_1_owner}} |
| {{act_2_id}} | {{act_2_name}} | {{act_2_start}} | {{act_2_end}} | {{act_2_predecessor}} | {{act_2_owner}} |

---

## Critical Path
<!-- Identify the critical path and top schedule risks. -->

{{critical_path}}

---

## Schedule Assumptions
<!-- maps to: pm:hasAssumption -->

{{#each schedule_assumptions}}
- {{this}}
{{/each}}

---

## Schedule Tolerances
<!-- maps to: pm:hasTolerance -->
<!-- State the permitted time deviation before escalation is required. -->

{{schedule_tolerances}}

---

*This document was produced in the Planning phase per ISO 21502:2020.
The schedule component corresponds to the PRINCE2® Plan management product
([prince2.wiki — Plan](https://prince2.wiki/management-products/baselines/plan/)).*
