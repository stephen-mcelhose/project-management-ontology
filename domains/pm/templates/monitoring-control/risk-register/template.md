---
type: template
document_class: pm:RiskRegister
phase: monitoring-control
standard: ISO 21502:2020
prince2_equivalent: Risk Register
ontology_uri: https://stephen-mcelhose.github.io/process-assistant/pm/RiskRegister
status: draft
---

# Risk Register Entry: {{entry_id}}

> **Purpose:** Captures and maintains information on a single identified risk — threat or
> opportunity — including its assessment, ownership, response strategy, and current status.
>
> **Produced in:** Monitoring & Control phase
> **Living document:** Opened at project initiation; one entry per identified risk.
> **Scales:** Probability, impact, and expected value scales are defined in the Risk Management Plan.

---

## Risk Entry
<!-- maps to: dct:identifier -->

**Risk ID:** {{entry_id}}

---

## Risk Type
<!-- maps to: dct:description -->
<!-- Threat (negative event) or Opportunity (positive event) -->

{{risk_type}}

---

## Risk Description
<!-- maps to: dct:description -->
<!-- Format: "Due to [cause], there is a risk that [event], which could lead to [impact]." -->

{{risk_description}}

---

## Assessment

### Probability
<!-- maps to: pm:likelihood -->
<!-- Use the scale defined in the Risk Management Plan (e.g. Very Low / Low / Medium / High / Very High) -->

{{probability}}

### Impact
<!-- maps to: pm:impact -->
<!-- Use the scale defined in the Risk Management Plan (e.g. Negligible / Minor / Moderate / Major / Catastrophic) -->

{{impact_severity}}

### Expected Value
<!-- maps to: dct:description -->
<!-- Probability × Impact score (per Risk Management Plan numeric scale) -->

{{expected_value}}

### Proximity
<!-- maps to: dct:description -->
<!-- When is this risk likely to materialise? (e.g. 'Within this stage', 'Before go-live') -->

{{proximity}}

---

## Ownership

### Risk Owner
<!-- maps to: pm:riskOwner -->
<!-- Named individual responsible for monitoring and managing this risk -->

{{risk_owner}}

---

## Response

### Strategy
<!-- maps to: pm:hasResponse -->
<!-- Threats: Avoid / Reduce / Transfer / Accept -->
<!-- Opportunities: Exploit / Enhance / Share / Reject -->

{{response_strategy}}

### Actions
<!-- maps to: dct:description -->
<!-- Specific actions with owner and target date for each -->

{{response_actions}}

---

## Status
<!-- maps to: pm:documentStatus -->
<!-- Open / Active / Closed / Expired -->

{{risk_status}}

---

## Date Identified
<!-- maps to: dct:created -->

{{date_identified}}

---

*This document was produced in the Monitoring & Control phase per ISO 21502:2020 §9
and corresponds to the PRINCE2® Risk Register management product
([prince2.wiki — Risk Register](https://prince2.wiki/management-products/project-log/risk-register/)).*
