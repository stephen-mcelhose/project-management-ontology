---
type: template
document_class: pm:RiskManagementPlan
phase: planning
standard: ISO 21502:2020
prince2_equivalent: Risk Management Approach
ontology_uri: https://stephen-mcelhose.github.io/project-management-ontology/RiskManagementPlan
status: draft
---

# Risk Management Plan: {{project_name}}

> **Purpose:** Defines how risks will be identified, analyzed, prioritized, and managed
> throughout the project lifecycle.
>
> **Produced in:** Planning phase (DIN 69901)
> **Depends on:** Project Charter
> **Must be completed before:** Risk Register

---

## Scope
<!-- maps to: dct:description -->
<!-- Define which types of risks are in scope. State any explicit exclusions. -->

{{risk_scope}}

---

## Risk Management Procedures
<!-- Describe the process for identifying, assessing, planning, implementing, and communicating risks. -->

{{risk_procedures}}

---

## Risk Assessment Scales

### Probability Scale
<!-- maps to: pm:likelihood -->
<!-- Define the scale used to score the likelihood of a risk occurring. -->

| Level | Label | Probability Range |
| ----- | ----- | ----------------- |
| {{prob_1_level}} | {{prob_1_label}} | {{prob_1_range}} |
| {{prob_2_level}} | {{prob_2_label}} | {{prob_2_range}} |
| {{prob_3_level}} | {{prob_3_label}} | {{prob_3_range}} |

### Impact Scale
<!-- maps to: pm:impact -->
<!-- Define the scale used to score the impact if a risk materializes. -->

| Level | Label | Description |
| ----- | ----- | ----------- |
| {{impact_1_level}} | {{impact_1_label}} | {{impact_1_description}} |
| {{impact_2_level}} | {{impact_2_label}} | {{impact_2_description}} |
| {{impact_3_level}} | {{impact_3_label}} | {{impact_3_description}} |

---

## Risk Tolerance and Escalation Threshold
<!-- maps to: pm:hasTolerance -->
<!-- Define the maximum risk exposure acceptable without escalation to the Project Board. -->

{{risk_tolerance}}

---

## Timing of Risk Management Activities
<!-- Specify when formal risk reviews and assessments will take place. -->

{{risk_timing}}

---

## Responsibilities
<!-- maps to: pm:RoleAssignment -->

| Role | Responsibility | Assigned To |
| ---- | -------------- | ----------- |
| Risk Manager | Overall risk management process | {{risk_manager_name}} |
| Risk Owner | Owns a specific risk and its response | {{risk_owner_role}} |
| Risk Action Owner | Implements the risk response action | {{risk_action_owner_role}} |

---

## Supporting Tools and Techniques
<!-- List the tools, techniques, and methods used for risk identification and assessment. -->

{{risk_tools}}

---

## Initial Risk Register (Seed)
<!-- maps to: pm:hasRisk -->
<!-- List the top 3–5 risks already identified. Full tracking moves to the Risk Register. -->

| # | Risk Description | Probability | Impact | Score | Response | Owner |
| - | ---------------- | ----------- | ------ | ----- | -------- | ----- |
| 1 | {{risk_1_description}} | {{risk_1_probability}} | {{risk_1_impact}} | {{risk_1_score}} | {{risk_1_response}} | {{risk_1_owner}} |
| 2 | {{risk_2_description}} | {{risk_2_probability}} | {{risk_2_impact}} | {{risk_2_score}} | {{risk_2_response}} | {{risk_2_owner}} |
| 3 | {{risk_3_description}} | {{risk_3_probability}} | {{risk_3_impact}} | {{risk_3_score}} | {{risk_3_response}} | {{risk_3_owner}} |

---

*This document was produced in the Planning phase per ISO 21502:2020
and corresponds to the PRINCE2® Risk Management Approach management product
([prince2.wiki — Risk Management Approach](https://prince2.wiki/management-products/baselines/management-approaches/risk/)).*
