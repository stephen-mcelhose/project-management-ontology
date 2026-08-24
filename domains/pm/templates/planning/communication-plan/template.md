---
type: template
document_class: pm:CommunicationPlan
phase: planning
standard: ISO 21502:2020
prince2_equivalent: Communication Management Approach
ontology_uri: https://stephen-mcelhose.github.io/process-assistant/pm/CommunicationPlan
status: draft
---

# Communication Plan: {{project_name}}

> **Purpose:** Outlines the information needs of stakeholders and the methods,
> frequency, and responsibilities for distributing project information.
>
> **Produced in:** Planning phase (DIN 69901)
> **Depends on:** Stakeholder Register
> **Must be completed before:** (Communication Plan is a terminal planning document — no Planning-phase documents depend on it)

---

## Scope
<!-- maps to: dct:description -->
<!-- Define which stakeholders and communication types are in scope. State any exclusions. -->

{{communication_scope}}

---

## Stakeholder Analysis
<!-- maps to: pm:RoleAssignment -->
<!-- All stakeholders from the Stakeholder Register must appear here. -->

| Stakeholder / Group | Interest | Influence | Current Engagement | Desired Engagement |
| ------------------- | -------- | --------- | ------------------ | ------------------ |
| {{sh_1_name}} | {{sh_1_interest}} | {{sh_1_influence}} | {{sh_1_current_engagement}} | {{sh_1_desired_engagement}} |
| {{sh_2_name}} | {{sh_2_interest}} | {{sh_2_influence}} | {{sh_2_current_engagement}} | {{sh_2_desired_engagement}} |

---

## Communication Schedule
<!-- maps to: pm:communicationApproach -->
<!-- Every stakeholder group must have at least one scheduled communication with a stated frequency. -->

| Stakeholder / Group | Information | Frequency | Channel | Format | Owner |
| ------------------- | ----------- | --------- | ------- | ------ | ----- |
| {{comm_1_stakeholder}} | {{comm_1_information}} | {{comm_1_frequency}} | {{comm_1_channel}} | {{comm_1_format}} | {{comm_1_owner}} |
| {{comm_2_stakeholder}} | {{comm_2_information}} | {{comm_2_frequency}} | {{comm_2_channel}} | {{comm_2_format}} | {{comm_2_owner}} |

---

## Communication Channels and Tools
<!-- List the platforms and tools used for communication delivery. Note channel suitability for sensitive information. -->

{{communication_channels}}

---

## Responsibilities
<!-- maps to: pm:RoleAssignment -->

| Communication Type | Responsible for Preparing | Responsible for Approving | Responsible for Distributing |
| ------------------ | ------------------------- | ------------------------- | ---------------------------- |
| Status reports | {{status_report_preparer}} | {{status_report_approver}} | {{status_report_distributor}} |
| Stakeholder updates | {{update_preparer}} | {{update_approver}} | {{update_distributor}} |
| Escalations | {{escalation_preparer}} | {{escalation_approver}} | {{escalation_distributor}} |

---

## Feedback Procedures
<!-- Describe how stakeholders can provide feedback and how it will be captured and acted on. -->

{{feedback_procedures}}

---

## Standards and Constraints
<!-- List any organizational, legal, or GDPR constraints on project communications. -->

{{communication_standards}}

---

*This document was produced in the Planning phase per ISO 21502:2020
and corresponds to the PRINCE2® Communication Management Approach management product
([prince2.wiki — Communication Management Approach](https://prince2.wiki/management-products/baselines/management-approaches/communication/)).*
