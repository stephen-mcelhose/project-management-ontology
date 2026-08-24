---
type: template
document_class: pm:ProjectClosureStatement
phase: closure
standard: ISO 21502:2020
prince2_equivalent: End Project Report (Project Board acceptance)
ontology_uri: https://stephen-mcelhose.github.io/process-assistant/pm/ProjectClosureStatement
status: draft
---

# Project Closure Statement: {{project_name}}

> **Purpose:** Formally declares the project closed. Confirms whether objectives were
> met, records any outstanding commitments, and captures Project Board acceptance.
> This is the authoritative record that the project has ended.
>
> **Produced in:** Closure phase
> **ISO 21502:2020 basis:** Section 9 — Closing a project

---

## Closure Declaration
<!-- maps to: dct:description -->
<!-- Project name, closure date, and one-sentence outcome statement -->
<!-- "The project delivered X and is hereby closed on [date]" -->

{{closure_declaration}}

---

## Objectives Met
<!-- maps to: pm:hasObjective -->
<!-- One line per objective: fully met / partially met / not met — reference the Final Project Report for detail -->

{{objectives_met}}

---

## Outstanding Commitments
<!-- maps to: dct:description -->
<!-- Open actions, deferred items, or known defects at closure — named owner and resolution date -->
<!-- State 'None' if nothing is outstanding -->

{{outstanding_commitments}}

---

## Benefits Realisation
<!-- maps to: dct:description -->
<!-- Current benefits status; post-project benefits review date and owner if not yet measurable -->

{{benefits_realisation}}

---

## Formal Approval
<!-- maps to: pm:approvedBy -->
<!-- Name, role, and organisation of each approver; approval date -->
<!-- Minimum: Project Board Chair or executive sponsor -->

{{formal_approval}}

---

*This document was produced in the Closure phase per ISO 21502:2020 §9.
It provides the standalone closure record corresponding to the PRINCE2® Project Board
authorisation to close, as described in the End Project Report
([prince2.wiki — End Project Report](https://prince2.wiki/management-products/reports/end-project-report/)).*
