---
type: template
document_class: pm:ProjectManagementPlan
phase: planning
standard: ISO 21502:2020
prince2_equivalent: Project Initiation Documentation (PID)
ontology_uri: https://stephen-mcelhose.github.io/project-management-ontology/ProjectManagementPlan
status: draft
---

# Project Management Plan: {{project_name}}

> **Purpose:** Consolidates all subsidiary plans into a single governing document defining
> how the project will be executed, monitored, and controlled.
>
> **Produced in:** Planning phase (DIN 69901)
> **Depends on:** Project Charter
> **Must be completed before:** Change Requests, Status Reports, Issue Log, Decision Log

---

## Project Purpose, Scope, and Direction
<!-- maps to: dct:description -->
<!-- State the project purpose, what it will deliver, and what is explicitly out of scope. -->

{{project_purpose_and_scope}}

---

## Project Objectives
<!-- maps to: proj:purpose -->
<!-- Define objectives across all six PRINCE2 performance variables. -->

| Variable  | Target / Commitment |
| --------- | ------------------- |
| Time      | {{objective_time}} |
| Cost      | {{objective_cost}} |
| Quality   | {{objective_quality}} |
| Scope     | {{objective_scope}} |
| Benefits  | {{objective_benefits}} |
| Risk      | {{objective_risk}} |

---

## Project Approach
<!-- maps to: pm:projectApproach -->
<!-- Describe the chosen solution path (build, buy, outsource, phased, agile, etc.). -->

{{project_approach}}

---

## Project Management Team Structure
<!-- maps to: pm:RoleAssignment -->

| Name | Role | Key Responsibilities |
| ---- | ---- | -------------------- |
| {{sponsor_name}} | Project Sponsor | {{sponsor_responsibilities}} |
| {{pm_name}} | Project Manager | {{pm_responsibilities}} |
| {{team_lead_1_name}} | {{team_lead_1_role}} | {{team_lead_1_responsibilities}} |

---

## Tolerances
<!-- maps to: pm:hasTolerance -->
<!-- State the permitted deviation before escalation is required. -->

| Dimension | Tolerance |
| --------- | --------- |
| Time      | {{tolerance_time}} |
| Cost      | {{tolerance_cost}} |
| Quality   | {{tolerance_quality}} |
| Scope     | {{tolerance_scope}} |
| Benefits  | {{tolerance_benefits}} |
| Risk      | {{tolerance_risk}} |

---

## Planning Assumptions
<!-- maps to: pm:hasAssumption -->
<!-- List key assumptions. For each: state the assumption and consequence if false. -->

{{#each planning_assumptions}}
- **Assumption:** {{this.assumption}}
  **If false:** {{this.consequence}}
{{/each}}

---

## Constraints
<!-- maps to: pm:hasConstraint -->
<!-- List constraints limiting the project's options (deadline, budget cap, regulatory, etc.). -->

{{#each constraints}}
- {{this}}
{{/each}}

---

## Risk Management Approach
<!-- Summarize how risks are managed. Full detail in the Risk Management Plan document. -->

{{risk_management_approach}}

---

## Quality Management Approach
<!-- Summarize how quality is managed. Full detail in the Quality Management Plan document. -->

{{quality_management_approach}}

---

## Change Control Approach
<!-- Describe how changes to scope, schedule, or budget are requested, assessed, and approved. -->

{{change_control_approach}}

---

## Communication Approach
<!-- Summarize key recurring communications. Full schedule in the Communication Plan document. -->

{{communication_approach}}

---

## Reporting and Controls
<!-- Specify: reporting frequency, stage boundaries or review gates, and escalation paths. -->

{{reporting_and_controls}}

---

*This document was produced in the Planning phase per ISO 21502:2020
and corresponds to the PRINCE2® Project Initiation Documentation management product
([prince2.wiki — Project Initiation Documentation](https://prince2.wiki/management-products/baselines/project-initiation-documentation/)).*
