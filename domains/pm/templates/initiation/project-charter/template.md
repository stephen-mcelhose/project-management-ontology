---
type: template
document_class: pm:ProjectCharter
phase: initiation
standard: ISO 21502:2020
prince2_equivalent: Project Initiation Documentation (PID)
ontology_uri: https://stephen-mcelhose.github.io/process-assistant/pm/ProjectCharter
status: draft
---

# Project Charter: {{project_name}}

> **Purpose:** Formally authorizes the existence of the project and grants
> the project manager authority to apply resources to project activities.
> Sets out the direction and scope of the project and acts as the formal
> agreement between the project manager and the project board.
>
> **Produced in:** Initiation phase (DIN 69901)
> **Depends on:** Business Case
> **Must be completed before:** Stakeholder Register

---

## Project Definition

### Background
<!-- maps to: dct:description -->

{{background}}

### Objectives
<!-- maps to: proj:hadObjective -->

{{#each objectives}}
- {{this}}
{{/each}}

### Desired Outcomes
<!-- maps to: pm:desiredOutcome -->

{{desired_outcomes}}

### Scope

**In Scope:**
{{project_scope_in}}

**Out of Scope:**
{{project_scope_out}}

### Constraints and Assumptions

**Constraints:**
<!-- maps to: pm:hasConstraint -->
{{constraints}}

**Assumptions:**
<!-- maps to: pm:hasAssumption -->
{{assumptions}}

---

## Project Approach
<!-- maps to: pm:projectApproach -->
<!-- How will the project product be delivered? Build, buy, outsource, hybrid. -->

{{project_approach}}

---

## Project Management Team Structure
<!-- maps to: pm:RoleAssignment -->

| Role | Name | Reports To |
| ---- | ---- | ---------- |
| Sponsor / Executive | {{sponsor_name}} | Business layer |
| Project Manager | {{pm_name}} | Sponsor / Executive |
| {{role_3_name}} | {{role_3_person}} | {{role_3_reports_to}} |

---

## Role Descriptions
<!-- maps to: pm:assignedRole -->

{{role_descriptions}}

---

## Project Controls
<!-- maps to: pm:hasTolerance -->
<!-- Management stages, tolerances, and reporting cadence. -->

| Dimension | Tolerance | Notes |
| --------- | --------- | ----- |
| Time | {{tolerance_time}} | |
| Cost | {{tolerance_cost}} | |
| Quality | {{tolerance_quality}} | |
| Scope | {{tolerance_scope}} | |
| Benefit | {{tolerance_benefit}} | |
| Risk | {{tolerance_risk}} | |

**Reporting cadence:** {{project_controls}}

---

## Tailoring
<!-- How has the standard PM approach been tailored for this project? -->

{{tailoring_statement}}

---

## Formal Authorization
<!-- maps to: pm:approvedBy -->

**Authorized by:** {{authorization}}
**Project Manager's authority:** {{pm_authority_limits}}

---

*This document was produced in the Initiation phase per ISO 21502:2020 §6
and corresponds to the PRINCE2® Project Initiation Documentation (PID)
management product
([prince2.wiki — Project initiation documentation](https://prince2.wiki/management-products/baselines/project-initiation-documentation/)).*
