---
type: template
document_class: pm:ProjectProposal
phase: initiation
standard: ISO 21502:2020
prince2_equivalent: Project Brief
ontology_uri: https://stephen-mcelhose.github.io/project-management-ontology/ProjectProposal
status: draft
---

# Project Proposal: {{project_name}}

> **Purpose:** Outlines the initial project idea, high-level objectives, and justification
> to seek formal authorization to proceed to a Business Case.
>
> **Produced in:** Initiation phase (DIN 69901)
> **Must be completed before:** Business Case

---

## Project Name
<!-- maps to: dct:title -->

{{project_name}}

---

## Problem / Opportunity
<!-- maps to: dct:description -->
<!-- Describe the current situation. Why does this problem exist? Why act now? -->

{{problem_statement}}

---

## Objectives
<!-- maps to: proj:purpose -->
<!-- 2–5 specific, measurable objectives. Start each with a verb. -->

{{#each objectives}}
- {{this}}
{{/each}}

---

## Expected Benefits
<!-- These become the Business Case. Be concrete: cost, time, risk, revenue. -->

{{expected_benefits}}

---

## Scope

### In Scope
<!-- List the work, deliverables, or capabilities this project will produce. -->

{{scope_in}}

### Out of Scope
<!-- Name things a stakeholder might assume are included but are not. -->

{{scope_out}}

---

## Proposed Sponsor
<!-- maps to: pm:hasSponsor -->
<!-- A named individual with authority to approve resources. -->

**Name:** {{sponsor_name}}
**Role / Title:** {{sponsor_role}}

---

## Key Stakeholders
<!-- maps to: pm:RoleAssignment -->

| Name / Team | Role | Interest |
| ----------- | ---- | -------- |
| {{stakeholder_1_name}} | {{stakeholder_1_role}} | {{stakeholder_1_interest}} |

---

## Rough Budget Estimate
<!-- maps to: pm:budget -->
<!-- Order of magnitude is fine here. TBD is acceptable. -->

{{rough_budget}}

---

## Rough Timeline
<!-- maps to: pm:plannedEndDate -->
<!-- Target end date or duration. TBD is acceptable. -->

{{rough_timeline}}

---

## Key Risks and Assumptions
<!-- maps to: pm:Risk -->
<!-- Top 2–3 risks or assumptions. Each: "If [X], then [consequence]." -->

| # | Risk / Assumption | Consequence |
| - | ----------------- | ----------- |
| 1 | {{risk_1}} | {{risk_1_consequence}} |
| 2 | {{risk_2}} | {{risk_2_consequence}} |

---

## Authorization Request

<!-- What decision are you requesting? -->

{{authorization_request}}

---

*This document was produced in the Initiation phase per ISO 21502:2020 §6
and corresponds to the PRINCE2® Project Brief management product
([prince2.wiki — Project Brief](https://prince2.wiki/management-products/baselines/project-brief/)).*
