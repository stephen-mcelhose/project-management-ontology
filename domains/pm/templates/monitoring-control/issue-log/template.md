---
type: template
document_class: pm:IssueLog
phase: monitoring-control
standard: ISO 21502:2020
prince2_equivalent: Issue Register
ontology_uri: https://stephen-mcelhose.github.io/process-assistant/pm/IssueLog
status: draft
---

# Issue Log Entry: {{entry_id}}

> **Purpose:** Records a single formal issue — Request for Change, Off-Specification, or
> Problem/Concern — and tracks it from identification through to resolution and closure.
>
> **Produced in:** Monitoring & Control phase
> **Living document:** Opened at project initiation; one entry per formal issue raised.
>
> **Note:** Informal issues (minor admin problems, meeting room bookings, etc.) belong in
> the Daily Log, not here. Issues that materialise from risks should reference the Risk Register.

---

## Issue Entry
<!-- maps to: dct:identifier -->

**Issue ID:** {{entry_id}}

---

## Issue Type
<!-- maps to: dct:description -->
<!-- Request for Change (RFC) / Off-Specification / Problem or Concern -->

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

## Issue Description
<!-- maps to: dct:description -->
<!-- For RFCs and Off-Specifications: reference the specific baseline or Product Description affected -->

{{issue_description}}

---

## Priority and Severity

### Priority
<!-- maps to: pm:priority -->
<!-- Scale from Issue Management Approach (e.g. High / Medium / Low) -->
<!-- Priority = urgency of decision -->

{{priority}}

### Severity
<!-- maps to: dct:description -->
<!-- Scale from Issue Management Approach (e.g. Critical / Major / Minor) -->
<!-- Severity = impact if left unresolved -->

{{severity}}

---

## Assigned To
<!-- maps to: pm:assignedRole -->

{{assigned_to}}

---

## Status
<!-- maps to: pm:documentStatus -->
<!-- Open / In Progress / Resolved / Closed -->

{{issue_status}}

---

## Resolution
<!-- maps to: dct:description -->
<!-- Outcome and actions taken. TBD if still open. Capture lessons for future delivery. -->

{{resolution}}

---

## Closure Date
<!-- maps to: dct:description -->

{{closure_date}}

---

*This document was produced in the Monitoring & Control phase per ISO 21502:2020 §8
and corresponds to the PRINCE2® Issue Register management product
([prince2.wiki — Issue Register](https://prince2.wiki/management-products/project-log/issue-register/)).*
