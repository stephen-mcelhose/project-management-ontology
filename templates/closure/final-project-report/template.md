---
type: template
document_class: pm:FinalProjectReport
phase: closure
standard: ISO 21502:2020
prince2_equivalent: End Project Report
ontology_uri: https://stephen-mcelhose.github.io/project-management-ontology/FinalProjectReport
status: draft
---

# Final Project Report: {{project_name}}

> **Purpose:** Provides the Project Board with a definitive account of how the project
> performed against its approved plan, whether its objectives were met, and what lessons
> should be carried forward. This is the primary closure document reviewed by the Project Board.
>
> **Produced in:** Closure phase
> **PRINCE2 equivalent:** End Project Report
> **ISO 21502:2020 basis:** Section 9 — Closing a project

---

## Project Summary
<!-- maps to: dct:description -->
<!-- Project name, purpose, planned dates vs. actual dates -->

{{project_summary}}

---

## Achievement of Objectives
<!-- maps to: pm:hasObjective -->
<!-- For each objective from the Project Charter: fully met / partially met / not met — with explanation -->

{{achievement_of_objectives}}

---

## Performance Against Plan
<!-- maps to: pm:hasTolerance -->

### Time
<!-- Planned vs. actual duration — state variance and reason -->

### Cost
<!-- Approved budget vs. actual spend — state variance and reason -->

### Quality
<!-- Summary of quality performance — events, failures, and sign-offs -->

### Scope
<!-- Scope delivered vs. approved scope baseline — note any agreed changes -->

### Benefits
<!-- Benefits realized vs. expected per Business Case -->

### Risk
<!-- Net risk position at closure vs. project start -->

{{performance_against_plan}}

---

## Business Case Review
<!-- maps to: dct:description -->
<!-- Benefits achieved or on track; planned Benefits Review date if benefits are post-project -->

{{business_case_review}}

---

## Lessons Summary
<!-- maps to: dct:description -->
<!-- Top 3–5 headline lessons — detail is in the Lessons Learned Report -->

{{lessons_summary}}

---

## Outstanding Actions
<!-- maps to: dct:description -->
<!-- Open actions at closure: owner, target date — state 'No outstanding actions' if none -->

{{outstanding_actions}}

---

## Recommendations
<!-- maps to: dct:description -->
<!-- Project Manager's recommendations to the Project Board, sponsor, or operational owner -->

{{recommendations}}

---

*This document was produced in the Closure phase per ISO 21502:2020 §9
and corresponds to the PRINCE2® End Project Report management product
([prince2.wiki — End Project Report](https://prince2.wiki/management-products/reports/end-project-report/)).*
