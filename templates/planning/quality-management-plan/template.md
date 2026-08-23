---
type: template
document_class: pm:QualityManagementPlan
phase: planning
standard: ISO 21502:2020
prince2_equivalent: Quality Management Approach
ontology_uri: https://stephen-mcelhose.github.io/project-management-ontology/QualityManagementPlan
status: draft
---

# Quality Management Plan: {{project_name}}

> **Purpose:** Establishes the quality standards, criteria, and assurance activities
> that project deliverables must satisfy.
>
> **Produced in:** Planning phase (DIN 69901)
> **Depends on:** Requirement Specification
> **Must be completed before:** Quality Audit Reports

---

## Scope
<!-- maps to: dct:description -->
<!-- Define which products and activities are subject to quality management. State any exclusions. -->

{{quality_scope}}

---

## Applicable Standards
<!-- maps to: pm:qualityExpectations -->
<!-- List all organizational, industry, legal, or regulatory standards that apply. -->

| Standard | Description | Applies To |
| -------- | ----------- | ---------- |
| {{standard_1_name}} | {{standard_1_description}} | {{standard_1_applies_to}} |
| {{standard_2_name}} | {{standard_2_description}} | {{standard_2_applies_to}} |

---

## Quality Management Procedures

### Quality Planning
<!-- How quality requirements are defined per deliverable. -->

{{quality_planning_procedures}}

### Quality Control
<!-- How deliverables are inspected, reviewed, or tested before acceptance. -->

{{quality_control_procedures}}

### Quality Assurance
<!-- How the quality management process itself is audited. -->

{{quality_assurance_procedures}}

---

## Acceptance Criteria
<!-- maps to: pm:acceptanceCriteria -->
<!-- Define measurable criteria that key deliverables must meet to be accepted. -->

| Deliverable | Acceptance Criteria |
| ----------- | ------------------- |
| {{deliverable_1_name}} | {{deliverable_1_criteria}} |
| {{deliverable_2_name}} | {{deliverable_2_criteria}} |
| Final project product | {{final_product_criteria}} |

---

## Responsibilities
<!-- maps to: pm:RoleAssignment -->

| Role | Responsibility | Assigned To |
| ---- | -------------- | ----------- |
| QA Lead / Quality Manager | Assures the quality management process | {{qa_lead_name}} |
| Reviewer | Performs quality checks on deliverables | {{reviewer_role}} |
| Approver | Signs off acceptance of deliverables | {{approver_name}} |

---

## Supporting Tools and Techniques
<!-- List the tools and techniques used for quality control and assurance. -->

{{quality_tools}}

---

## Quality Records
<!-- Describe how quality evidence will be stored, maintained, and retained. -->

{{quality_records}}

---

*This document was produced in the Planning phase per ISO 21502:2020
and corresponds to the PRINCE2® Quality Management Approach management product
([prince2.wiki — Quality Management Approach](https://prince2.wiki/management-products/baselines/management-approaches/quality/)).*
