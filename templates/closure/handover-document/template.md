---
type: template
document_class: pm:HandoverDocument
phase: closure
standard: ISO 21502:2020
prince2_equivalent: End Project Report (handover section)
ontology_uri: https://stephen-mcelhose.github.io/project-management-ontology/HandoverDocument
status: draft
---

# Handover Document: {{project_name}}

> **Purpose:** Formally transfers completed project deliverables from the project to the
> receiving organisation (operations, client, or maintenance team), confirming what has
> been handed over, who is responsible for it, and any outstanding conditions.
>
> **Produced in:** Closure phase
> **ISO 21502:2020 basis:** Section 9 — Closing a project

---

## Project Summary
<!-- maps to: dct:description -->

{{project_summary}}

---

## Deliverables Handover
<!-- maps to: pm:hasDeliverable -->
<!-- For each deliverable: name | status (complete / conditionally accepted / deferred) | receiving party -->

{{deliverables_handover}}

---

## Operational Responsibilities
<!-- maps to: dct:contributor -->
<!-- Name the individual or team assuming operational responsibility for each handover item -->

{{operational_responsibilities}}

---

## Outstanding Items
<!-- maps to: dct:description -->
<!-- List known defects, deferred scope, or open actions — with resolution date and owner; state 'None' if nothing is outstanding -->

{{outstanding_items}}

---

## Support Arrangements
<!-- maps to: dct:description -->
<!-- Post-handover support, warranty, or maintenance — duration, scope, contact point -->
<!-- State 'No post-handover support agreed' if no formal arrangement applies -->

{{support_arrangements}}

---

## Handover Acceptance
<!-- maps to: pm:approvedBy -->
<!-- Name, role, and organisation of the accepting party, plus acceptance date -->

{{handover_acceptance}}

---

*This document was produced in the Closure phase per ISO 21502:2020 §9.
It corresponds to the handover section of the PRINCE2® End Project Report
([prince2.wiki — End Project Report](https://prince2.wiki/management-products/reports/end-project-report/)).*
