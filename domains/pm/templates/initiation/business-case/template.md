---
type: template
document_class: pm:BusinessCase
phase: initiation
standard: ISO 21502:2020
prince2_equivalent: Business Case
ontology_uri: https://stephen-mcelhose.github.io/process-assistant/pm/BusinessCase
status: draft
---

# Business Case: {{project_name}}

> **Purpose:** Provides the financial and strategic justification for the
> project, comparing expected costs against anticipated benefits, so
> organizational management can judge if the project is desirable, viable,
> and achievable.
>
> **Produced in:** Initiation phase (DIN 69901)
> **Depends on:** Project Proposal
> **Must be completed before:** Project Charter

---

## Executive Summary
<!-- maps to: dct:description -->
<!-- Concise overview: key reasons, benefits, expected ROI. -->

{{executive_summary}}

---

## Reasons
<!-- maps to: dct:description -->

{{reasons}}

---

## Business Options
<!-- maps to: pm:hasBusinessOption -->
<!-- At minimum: "do nothing" baseline, plus "do minimum" and/or "do more". -->

| Option | Description | Cost | Benefit | Feasible? | Recommended? |
| ------ | ----------- | ---- | ------- | --------- | ------------ |
| Do nothing | {{option_do_nothing}} | — | — | Baseline | No |
| {{option_2_name}} | {{option_2_description}} | {{option_2_cost}} | {{option_2_benefit}} | {{option_2_feasible}} | {{option_2_recommended}} |

---

## Expected Benefits
<!-- maps to: pm:hasBenefit -->

| # | Benefit | Measure (metric / target / timing) | Owner |
| - | ------- | ------------------------------------ | ----- |
| 1 | {{benefit_1}} | {{benefit_1_measure}} | {{benefit_1_owner}} |
| 2 | {{benefit_2}} | {{benefit_2_measure}} | {{benefit_2_owner}} |

---

## Expected Dis-benefits
<!-- maps to: pm:hasDisbenefit -->

{{expected_disbenefits}}

---

## Timescale
<!-- maps to: pm:plannedEndDate, pm:plannedStartDate -->

**Start:** {{planned_start_date}}
**End:** {{planned_end_date}}
**Payback period / benefits realization begins:** {{payback_period}}

---

## Costs
<!-- maps to: pm:budget -->

**Total project cost:** {{total_project_cost}}
**Ongoing operational / maintenance costs (post-project):** {{ongoing_costs}}

---

## Investment Appraisal
<!-- maps to: pm:investmentAppraisal -->
<!-- Use a technique appropriate to your organization: ROI, payback period, NPV, etc. -->

{{investment_appraisal}}

---

## Major Risks
<!-- maps to: pm:Risk -->
<!-- Summary only — full detail lives in the Risk Register. -->

| # | Risk | Response |
| - | ---- | -------- |
| 1 | {{risk_1}} | {{risk_1_response}} |
| 2 | {{risk_2}} | {{risk_2_response}} |

---

*This document was produced in the Initiation phase per ISO 21502:2020 §6
and corresponds to the PRINCE2® Business Case management product
([prince2.wiki — Business case](https://prince2.wiki/management-products/baselines/business-case/)).*
