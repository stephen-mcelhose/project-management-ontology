---
type: template
document_class: pm:ChangeRequest
phase: execution
standard: ISO 21502:2020
prince2_equivalent: Issue Report
ontology_uri: https://stephen-mcelhose.github.io/project-management-ontology/ChangeRequest
status: draft
---

# Change Request: {{change_request_id}}

> **Purpose:** Documents a formal proposal to modify any aspect of the project baseline
> (scope, schedule, budget, or quality), providing a complete impact assessment and a
> recommendation to support the approving authority's decision.
>
> **Produced in:** Execution phase (DIN 69901)
> **Depends on:** Project Management Plan
> **Must be completed before:** Change Log
> **PRINCE2 issue type:** Request for Change (RFC) / Off-Specification / Problem/Concern

---

## Issue Type
<!-- maps to: dct:description -->
<!-- Classify the issue: Request for Change | Off-Specification | Problem/Concern -->

**Type:** {{issue_type}}

---

## Date Raised and Raised By
<!-- maps to: dct:created -->

**Date raised:** {{date_raised}}
**Raised by:** {{raised_by_name}}, {{raised_by_role}}

---

## Issue Description
<!-- maps to: dct:description -->
<!-- Clear, objective description of the current situation and the change being proposed.
     Describe the problem or opportunity, not the solution. -->

{{issue_description}}

---

## Impact Analysis
<!-- maps to: pm:hasTolerance -->
<!-- Assess the impact across all six PRINCE2 performance variables.
     'No impact' must be stated explicitly — a blank implies the assessment was not done. -->

### Time
<!-- How many days/weeks of schedule change? Which milestones are affected? -->

{{impact_time}}

### Cost
<!-- Additional or reduced cost. Does this breach the budget tolerance? -->

{{impact_cost}}

### Quality
<!-- Which quality criteria or Product Descriptions are affected? -->

{{impact_quality}}

### Scope
<!-- Are deliverables added, removed, or modified? -->

{{impact_scope}}

### Benefits
<!-- Does this change increase, reduce, or defer the benefits in the Business Case? -->

{{impact_benefits}}

### Risk
<!-- maps to: pm:hasRisk -->
<!-- New risks introduced or existing risks mitigated by this change. -->

| Risk Description | Likelihood | Impact |
| ---------------- | ---------- | ------ |
| {{risk_1}} | {{risk_1_likelihood}} | {{risk_1_impact}} |

{{impact_risk_narrative}}

---

## Priority and Severity
<!-- maps to: pm:priority -->
<!-- Priority = urgency of decision (High / Medium / Low)
     Severity = extent of impact if unaddressed (Critical / Major / Minor) -->

**Priority:** {{priority}}
**Severity:** {{severity}}

---

## Recommended Options
<!-- maps to: dct:description -->
<!-- Provide at least two options including 'do nothing'. State advantages and disadvantages of each. -->

### Option 1: {{option_1_title}}

**Description:** {{option_1_description}}
**Advantages:** {{option_1_advantages}}
**Disadvantages:** {{option_1_disadvantages}}

### Option 2: {{option_2_title}}

**Description:** {{option_2_description}}
**Advantages:** {{option_2_advantages}}
**Disadvantages:** {{option_2_disadvantages}}

### Recommendation

{{recommendation}}

---

## Decision
<!-- maps to: dct:description -->
<!-- To be completed by the Project Manager, Change Authority, or Project Board. -->

**Decision:** {{decision}}
**Decided by:** {{decided_by}}

---

## Decision Date and Closure
<!-- maps to: dct:created -->

**Decision date:** {{decision_date}}
**Closure date:** {{closure_date}}

---

*This document was produced in the Execution phase per ISO 21502:2020 §8
and corresponds to the PRINCE2® Issue Report management product (RFC type)
([prince2.wiki — Issue Report](https://prince2.wiki/management-products/reports/issue-report/)).*
