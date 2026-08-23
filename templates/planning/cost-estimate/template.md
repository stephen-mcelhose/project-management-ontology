---
type: template
document_class: pm:CostEstimate
phase: planning
standard: ISO 21502:2020
prince2_equivalent: Business Case (cost and investment appraisal component)
ontology_uri: https://stephen-mcelhose.github.io/project-management-ontology/CostEstimate
status: draft
---

# Cost Estimate: {{project_name}}

> **Purpose:** Determines the total approved budget by aggregating estimated costs of
> individual activities and resources, and demonstrates project value via investment appraisal.
>
> **Produced in:** Planning phase (DIN 69901)
> **Depends on:** Resource Plan
> **Must be completed before:** (Cost Estimate is a terminal planning document — no Planning-phase documents depend on it)

---

## Overview
<!-- maps to: dct:description -->
<!-- Describe the scope of this Cost Estimate and what cost categories are covered. -->

{{cost_estimate_description}}

---

## Cost Breakdown
<!-- Detail costs by work package or project phase. State the basis of each estimate. -->

| Work Package / Phase | Cost Type | Estimated Cost | Basis of Estimate |
| -------------------- | --------- | -------------- | ----------------- |
| {{cost_1_item}} | {{cost_1_type}} | {{cost_1_amount}} | {{cost_1_basis}} |
| {{cost_2_item}} | {{cost_2_type}} | {{cost_2_amount}} | {{cost_2_basis}} |

---

## Labour Costs
<!-- maps to: pm:costRate -->
<!-- Calculate from Resource Plan: cost rate × estimated hours per role. -->

| Role | Cost Rate (per hour) | Estimated Hours | Total |
| ---- | -------------------- | --------------- | ----- |
| {{labour_1_role}} | {{labour_1_rate}} | {{labour_1_hours}} | {{labour_1_total}} |
| {{labour_2_role}} | {{labour_2_rate}} | {{labour_2_hours}} | {{labour_2_total}} |

**Total Labour Cost:** {{total_labour_cost}}

---

## Total Project Budget
<!-- maps to: pm:budget -->

| Category | Amount |
| -------- | ------ |
| Labour   | {{total_labour_cost}} |
| Materials / Equipment | {{total_material_cost}} |
| External services | {{total_external_cost}} |
| Other | {{total_other_cost}} |
| **Sub-total (base estimate)** | **{{base_estimate_total}}** |
| Contingency ({{contingency_percent}}%) | {{contingency_amount}} |
| **Total Approved Budget** | **{{total_budget}}** |

**Currency:** {{budget_currency}}

---

## Contingency and Cost Tolerance
<!-- maps to: pm:hasTolerance -->
<!-- State the contingency reserve and the permitted cost deviation before escalation. -->

{{contingency_budget}}

---

## Post-Delivery Operational Costs
<!-- State ongoing costs the project will create after delivery. This must not be omitted. -->

{{operational_costs}}

---

## Investment Appraisal
<!-- maps to: pm:investmentAppraisal -->
<!-- Compare total costs against expected benefits. State the preferred metric and result. -->

{{investment_appraisal}}

---

## Cost Assumptions
<!-- maps to: pm:hasAssumption -->

{{#each cost_assumptions}}
- {{this}}
{{/each}}

---

*This document was produced in the Planning phase per ISO 21502:2020.
The cost and investment appraisal component corresponds to the PRINCE2® Business Case management product
([prince2.wiki — Business Case](https://prince2.wiki/management-products/baselines/business-case/)).*
