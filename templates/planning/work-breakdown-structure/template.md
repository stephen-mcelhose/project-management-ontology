---
type: template
document_class: pm:WorkBreakdownStructure
phase: planning
standard: ISO 21502:2020
prince2_equivalent: Plan (product breakdown structure component)
ontology_uri: https://stephen-mcelhose.github.io/project-management-ontology/WorkBreakdownStructure
status: draft
---

# Work Breakdown Structure: {{project_name}}

> **Purpose:** Hierarchically decomposes the total project scope into manageable
> work packages and deliverables.
>
> **Produced in:** Planning phase (DIN 69901 / DIN 69901-3 Projektstrukturplan)
> **Depends on:** Project Charter
> **Must be completed before:** Project Schedule, Work Package Descriptions

---

## Overview
<!-- maps to: dct:description -->
<!-- Describe what scope this WBS covers and what decomposition levels are used. -->

{{wbs_description}}

---

## Decomposition Approach
<!-- Describe the WBS levels and whether this is product-based or activity-based. -->

{{decomposition_approach}}

---

## WBS Hierarchy
<!-- maps to: pm:hasDeliverable -->
<!-- List the top-level project deliverables (Level 1 / Level 2 of the WBS). -->

### Level 1 Deliverables

| ID | Deliverable | Description |
| -- | ----------- | ----------- |
| {{deliverable_1_id}} | {{deliverable_1_name}} | {{deliverable_1_description}} |
| {{deliverable_2_id}} | {{deliverable_2_name}} | {{deliverable_2_description}} |

---

## Work Packages
<!-- maps to: pm:hasTask -->
<!-- For each top-level deliverable, list the work packages required. -->

### {{deliverable_1_name}}

| WP ID | Work Package Name | Description | Responsible | Estimated Effort |
| ----- | ----------------- | ----------- | ----------- | ---------------- |
| {{wp_1_id}} | {{wp_1_name}} | {{wp_1_description}} | {{wp_1_owner}} | {{wp_1_effort}} |
| {{wp_2_id}} | {{wp_2_name}} | {{wp_2_description}} | {{wp_2_owner}} | {{wp_2_effort}} |

---

## Product Acceptance Criteria
<!-- maps to: pm:acceptanceCriteria -->
<!-- Define what 'done' looks like for the final project product. -->

{{#each acceptance_criteria}}
- {{this}}
{{/each}}

---

## External Dependencies
<!-- List any deliverables or activities outside the project team's control. -->

{{external_dependencies}}

---

## Lessons Incorporated
<!-- Describe any lessons from prior projects incorporated into the WBS design or estimates. -->

{{lessons_incorporated}}

---

*This document was produced in the Planning phase per ISO 21502:2020.
The product breakdown structure component corresponds to the PRINCE2® Plan management product
([prince2.wiki — Plan](https://prince2.wiki/management-products/baselines/plan/)).
DIN 69901-3:2009 references this as the Projektstrukturplan (PSP)
([DIN 69901-3](https://www.beuth.de/en/standard/din-69901-2/119948897)).*
