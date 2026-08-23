---
type: template
document_class: pm:ArchiveIndex
phase: closure
standard: ISO 21502:2020
prince2_equivalent: Product Register (broader)
ontology_uri: https://stephen-mcelhose.github.io/project-management-ontology/ArchiveIndex
status: draft
---

# Archive Index: {{project_name}}

> **Purpose:** Identifies, locates, and formally transfers all project records to an
> archive owner for long-term storage and retrieval. Ensures project knowledge is
> preserved for future reference, audit, and benefits realisation review.
>
> **Produced in:** Closure phase
> **ISO 21502:2020 basis:** Section 9 — Closing a project
>
> **Note:** The all-documents dependency is expressed narratively: this index
> can only be compiled once all project documents from all phases are finalized.

---

## Archive Location
<!-- maps to: dct:description -->
<!-- Storage system or location name, URL or path, and named archive owner -->

{{archive_location}}

---

## Document Inventory
<!-- maps to: dct:hasPart -->
<!-- For each document: name | type (plan / report / log / contract / etc.) | version | date finalized -->
<!-- Must cover all phases: Initiation, Planning, Execution, Monitoring & Control, Closure -->

{{document_inventory}}

---

## Access Controls
<!-- maps to: dct:accessRights -->
<!-- Who may read / write / update the archive; any restricted documents -->

{{access_controls}}

---

## Retention Policy
<!-- maps to: dct:description -->
<!-- Retention period, applicable policy or regulation, scheduled review or destruction date -->

{{retention_policy}}

---

## Handover Confirmation
<!-- maps to: pm:approvedBy -->
<!-- Name and role of archive owner who confirmed receipt; transfer date -->

{{handover_confirmation}}

---

*This document was produced in the Closure phase per ISO 21502:2020 §9.
It is related to the PRINCE2® Product Register
([prince2.wiki — Product Register](https://prince2.wiki/management-products/project-log/product-register/)),
but is broader in scope, covering all project management records.*
