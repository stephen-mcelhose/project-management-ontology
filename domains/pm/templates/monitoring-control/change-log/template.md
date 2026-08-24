---
type: template
document_class: pm:ChangeLog
phase: monitoring-control
standard: ISO 21502:2020
prince2_equivalent: Issue Management Approach
ontology_uri: https://stephen-mcelhose.github.io/process-assistant/pm/ChangeLog
status: draft
---

# Change Log Entry: {{entry_id}}

> **Purpose:** Tracks a single change request through its full lifecycle — from initial submission
> through evaluation, authorisation, implementation, and verification — providing an audit trail
> of all changes to the project baseline.
>
> **Produced in:** Monitoring & Control phase
> **Living document:** Opened at project initiation; one entry per Change Request submitted.
>
> **Note:** Corresponds to the change control tracking function of the PRINCE2 Issue Management
> Approach. Each entry links to an originating Change Request document.

---

## Change Log Entry
<!-- maps to: dct:identifier -->

**Change Log ID:** {{entry_id}}

---

## Change Request Reference
<!-- maps to: dct:references -->
<!-- Link to the originating Change Request document -->

{{change_request_ref}}

---

## Issue Type
<!-- maps to: dct:description -->
<!-- Request for Change / Off-Specification / Problem or Concern -->

{{issue_type}}

---

## Date Raised
<!-- maps to: dct:created -->

{{date_raised}}

---

## Raised By
<!-- maps to: dct:creator -->

{{raised_by}}

---

## Change Description
<!-- maps to: dct:description -->
<!-- Brief summary (1–3 sentences) of the proposed change -->

{{change_description}}

---

## Priority and Severity
<!-- maps to: pm:priority -->
<!-- Priority: High / Medium / Low (urgency of decision) -->
<!-- Severity: Critical / Major / Minor (impact if left unresolved) -->

{{priority_severity}}

---

## Decision
<!-- maps to: dct:description -->
<!-- Approved / Rejected / Deferred / Pending -->

{{decision}}

---

## Decision Authority
<!-- maps to: pm:approvedBy -->
<!-- Named individual or governance body who authorised the decision -->

{{decision_authority}}

---

## Decision Date
<!-- maps to: dct:description -->

{{decision_date}}

---

## Implementation Status
<!-- maps to: pm:documentStatus -->
<!-- Not Started / In Progress / Implemented / Verified / Closed -->

{{implementation_status}}

---

## Closure Date
<!-- maps to: dct:description -->

{{closure_date}}

---

*This document was produced in the Monitoring & Control phase per ISO 21502:2020 §8
and corresponds to the change control tracking function of the PRINCE2® Issue Management
Approach management product
([prince2.wiki — Issue Management Approach](https://prince2.wiki/management-products/baselines/management-approaches/issue/)).*
