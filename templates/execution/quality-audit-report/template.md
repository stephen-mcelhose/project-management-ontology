---
type: template
document_class: pm:QualityAuditReport
phase: execution
standard: ISO 21502:2020
prince2_equivalent: Quality Register
ontology_uri: https://stephen-mcelhose.github.io/project-management-ontology/QualityAuditReport
status: draft
---

# Quality Audit Report: {{audit_id}}

> **Purpose:** Documents the results of a structured quality review confirming whether a
> specific deliverable meets the defined quality standards and acceptance criteria, and
> records any corrective actions required.
>
> **Produced in:** Execution phase (DIN 69901)
> **Depends on:** Quality Management Plan
> **One report per quality review activity**
> **PRINCE2 basis:** Quality Register entry (one per quality activity)

---

## Product Reviewed
<!-- maps to: pm:hasDeliverable -->
<!-- The product or deliverable subject to this quality review. -->

**Product ID:** {{product_id}}
**Product Name:** {{product_name}}

---

## Quality Method
<!-- maps to: pm:projectApproach -->
<!-- The quality control method applied in this review, as defined in the Quality Management Plan. -->

{{quality_method}}

---

## Roles

### Producer
<!-- maps to: pm:RoleAssignment -->
<!-- The person or team who created the product being reviewed. -->

**Name:** {{producer_name}}
**Role:** {{producer_role}}

### Reviewer(s)
<!-- maps to: pm:RoleAssignment -->
<!-- The person or team who assessed the product's quality. Must be independent of the producer. -->

| Name | Role |
| ---- | ---- |
| {{reviewer_1_name}} | {{reviewer_1_role}} |

### Approver
<!-- maps to: pm:RoleAssignment -->
<!-- The individual with authority to formally accept this product. -->

**Name:** {{approver_name}}
**Role:** {{approver_role}}

---

## Review Dates

### Target Review Date
<!-- maps to: pm:plannedStartDate -->
<!-- Planned date for the quality review as scheduled in the project plan. -->

{{target_review_date}}

### Actual Review Date
<!-- maps to: dct:created -->
<!-- The date the quality review actually took place. -->

{{actual_review_date}}

---

## Approval Dates

### Target Approval Date
<!-- maps to: pm:plannedEndDate -->
<!-- Planned date for formal product approval. -->

{{target_approval_date}}

### Actual Approval Date
<!-- maps to: pm:plannedEndDate -->
<!-- The actual date formal approval was granted. Leave blank if pending. -->

{{actual_approval_date}}

---

## Quality Criteria Applied
<!-- maps to: pm:acceptanceCriteria -->
<!-- The specific, measurable criteria evaluated in this review. Each must be traceable to a source document. -->

| # | Quality Criterion | Source / Reference | Met? |
| - | ----------------- | ------------------ | ---- |
| 1 | {{criterion_1}} | {{criterion_1_source}} | {{criterion_1_met}} |
| 2 | {{criterion_2}} | {{criterion_2_source}} | {{criterion_2_met}} |

---

## Result
<!-- maps to: pm:deliverableStatus -->
<!-- Overall outcome of the quality review: Pass | Conditional Pass | Fail -->

**Result:** {{result}}

*Summary of findings:*

{{result_summary}}

---

## Corrective Actions
<!-- maps to: dct:description -->
<!-- Required for Conditional Pass or Fail results. Each action must be assigned to a named owner. -->

| # | Action | Owner | Due Date | Status |
| - | ------ | ----- | -------- | ------ |
| 1 | {{action_1}} | {{action_1_owner}} | {{action_1_due}} | {{action_1_status}} |

*If result was Pass: state "No corrective actions required."*

---

## Quality Records Reference
<!-- maps to: dct:description -->
<!-- Link or reference to the quality records supporting this review (signed-off forms, test results, etc.). -->

{{quality_records_link}}

---

*This document was produced in the Execution phase per ISO 21502:2020 §8
and corresponds to an entry in the PRINCE2® Quality Register management product
([prince2.wiki — Quality Register](https://prince2.wiki/management-products/project-log/quality-register/)).*
