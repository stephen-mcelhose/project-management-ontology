---
type: template
document_class: pm:RequirementSpecification
phase: initiation
standard: ISO 21502:2020
prince2_equivalent: Project Product Description
ontology_uri: https://stephen-mcelhose.github.io/process-assistant/pm/RequirementSpecification
status: draft
---

# Requirement Specification: {{project_name}}

> **Purpose:** Documents the high-level needs, expectations, and constraints
> of stakeholders that the project deliverables must satisfy, including
> scope, quality expectations, and acceptance criteria for the project's
> final output.
>
> **Produced in:** Initiation phase (DIN 69901)
> **Depends on:** Stakeholder Register
> **Must be completed before:** Quality Management Plan (Planning phase)

---

## Title
<!-- maps to: dct:title -->

{{product_title}}

---

## Purpose
<!-- maps to: dct:description -->
<!-- Why is this product being created? Who are the target users? -->

{{purpose}}

---

## Composition
<!-- maps to: pm:productComposition -->
<!-- Major components/parts of the final product. Defines product scope. -->

{{composition}}

---

## Development Skills Required
<!-- maps to: pm:developmentSkillsRequired -->

{{development_skills}}

---

## Customer's Quality Expectations
<!-- maps to: pm:qualityExpectations -->
<!-- High-level, less measurable than acceptance criteria. -->

{{quality_expectations}}

---

## Requirements
<!-- maps to: pm:hasRequirement -->

| # | Requirement | Type (Functional / Non-Functional) |
| - | ----------- | ------------------------------------ |
| 1 | {{requirement_1}} | {{requirement_1_type}} |
| 2 | {{requirement_2}} | {{requirement_2_type}} |
| 3 | {{requirement_3}} | {{requirement_3_type}} |

---

## Acceptance Criteria
<!-- maps to: pm:acceptanceCriteria -->
<!-- Measurable, individually realistic, testable within the timeframe. -->

| # | Criterion | Priority |
| - | --------- | -------- |
| 1 | {{acceptance_criterion_1}} | {{acceptance_criterion_1_priority}} |
| 2 | {{acceptance_criterion_2}} | {{acceptance_criterion_2_priority}} |

---

## Acceptance Method
<!-- maps to: pm:acceptanceMethod -->

{{acceptance_method}}

---

## Acceptance Responsibilities
<!-- maps to: pm:acceptanceResponsibility -->

{{acceptance_responsibility}}

---

*This document was produced in the Initiation phase per ISO 21502:2020 §6
and corresponds to the PRINCE2® Project Product Description management
product
([prince2.wiki — Project product description](https://prince2.wiki/management-products/baselines/project-product-description/)).*
