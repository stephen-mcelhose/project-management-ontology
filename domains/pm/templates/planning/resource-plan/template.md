---
type: template
document_class: pm:ResourcePlan
phase: planning
standard: ISO 21502:2020
prince2_equivalent: Plan (resource planning component)
ontology_uri: https://stephen-mcelhose.github.io/process-assistant/pm/ResourcePlan
status: draft
---

# Resource Plan: {{project_name}}

> **Purpose:** Identifies the human, material, and financial resources required to
> complete project activities and their planned allocation.
>
> **Produced in:** Planning phase (DIN 69901)
> **Depends on:** Project Schedule
> **Must be completed before:** Cost Estimate

---

## Overview
<!-- maps to: dct:description -->
<!-- Describe the scope of this Resource Plan and what resource types are covered. -->

{{resource_plan_description}}

---

## Human Resources
<!-- maps to: pm:usesResource -->

| Role | Skills Required | # People | Period Required |
| ---- | --------------- | -------- | --------------- |
| {{hr_1_role}} | {{hr_1_skills}} | {{hr_1_count}} | {{hr_1_period}} |
| {{hr_2_role}} | {{hr_2_skills}} | {{hr_2_count}} | {{hr_2_period}} |

---

## Skill Requirements and Gap Analysis
<!-- maps to: pm:developmentSkillsRequired -->
<!-- Identify skill gaps and how they will be resolved. -->

{{skill_requirements}}

---

## Resource Availability
<!-- maps to: pm:capacity -->
<!-- State availability as a fraction of full-time (FTE). Team managers must confirm feasibility. -->

| Resource / Role | Allocation (FTE) | Available From | Available To | Notes |
| --------------- | ---------------- | -------------- | ------------ | ----- |
| {{res_1_name}} | {{res_1_fte}} | {{res_1_from}} | {{res_1_to}} | {{res_1_notes}} |
| {{res_2_name}} | {{res_2_fte}} | {{res_2_from}} | {{res_2_to}} | {{res_2_notes}} |

---

## Material and Equipment Resources
<!-- maps to: pm:usesResource -->
<!-- List material, equipment, or infrastructure needs. State 'None required' if not applicable. -->

{{material_resources}}

---

## Resource Calendar and Constraints
<!-- List known periods of unavailability and other resource constraints. -->

{{resource_calendar}}

---

## Resource Assumptions
<!-- maps to: pm:hasAssumption -->

{{#each resource_assumptions}}
- {{this}}
{{/each}}

---

*This document was produced in the Planning phase per ISO 21502:2020.
The resource planning component corresponds to the PRINCE2® Plan management product
([prince2.wiki — Plan](https://prince2.wiki/management-products/baselines/plan/)).*
