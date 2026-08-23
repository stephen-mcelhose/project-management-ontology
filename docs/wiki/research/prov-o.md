---
type: concept
title: PROV-O
description: The PROV Ontology provides a set of classes, properties, and restrictions that can be used to represent and interchange provenance information generated in different systems and under different contexts.
timestamp: 2024-08-22T00:00:00Z
resource: http://www.w3.org/ns/prov#
tags: [vocabulary, rdf, provenance, w3c]
---

# PROV-O: The PROV Ontology

The **PROV-O** ontology is a W3C recommendation for representing provenance information. In the context of project management, it provides a standardized way to track the lifecycle of artifacts, the activities that produced them, and the agents responsible for those activities.

## Core Classes

PROV-O is built around three starting point classes:

- **`prov:Entity`**: A physical, digital, or conceptual "thing" (e.g., a project charter, a source code repository, a requirements document).
- **`prov:Activity`**: Something that occurs over time and acts upon or with entities (e.g., "Drafting Requirements", "System Integration Test").
- **`prov:Agent`**: Something that bears responsibility for an activity or entity (e.g., a Project Manager, a Developer, or an automated build script).

## Key Properties

- **`prov:wasGeneratedBy`**: Links an Entity to the Activity that created it.
- **`prov:used`**: Links an Activity to an Entity that was consumed or utilized during its execution.
- **`prov:wasAssociatedWith`**: Links an Activity to the Agent responsible for it.
- **`prov:wasDerivedFrom`**: Links an Entity to another Entity that it was based on (e.g., a PDF report derived from a spreadsheet).
- **`prov:wasAttributedTo`**: Links an Entity to the Agent responsible for its existence.

## Modeling Provenance Chains

PROV-O allows for various levels of granularity in modeling history:
1. **Interleaved Chains**: `Entity` -> `wasGeneratedBy` -> `Activity` -> `used` -> `Entity`. This provides the most detail.
2. **Entity-Only Chains**: `Entity` -> `wasDerivedFrom` -> `Entity`. Useful for simple data lineage.
3. **Activity-Only Chains**: `Activity` -> `wasInformedBy` -> `Activity`. Focuses on process flow.

## Relevance to Project Management

In a project management ontology, PROV-O is essential for:
- **Audit Trails**: Tracking who changed what and when.
- **Deliverable Lineage**: Understanding how a final product relates to initial requirements.
- **Responsibility Mapping**: Connecting [FOAF](foaf.md) agents to project [DOAP](doap.md) activities.
- **Change Management**: Modeling how one version of an entity was derived from another.

## Usage in This Project

PROV-O is used **indirectly** in this project via the [PROJ Ontology](proj-ontology.md),
which is a PROV-O profile. The `prov:Entity`, `prov:Activity`, and `prov:Agent`
tripartite model is inherited through PROJ's specializations — raw `prov:` terms
may not appear directly in this project's Turtle files. See
[PROJ Ontology](proj-ontology.md) and [ADR-001](../../adrs/adr-001-base-ontology.md)
for how PROV-O concepts surface in the design.

## Related Vocabularies
- [PROJ Ontology](proj-ontology.md): PROV-O profile selected as the base for this project
- [DOAP](doap.md): Description of a Project
- [Dublin Core](dublin-core.md): Metadata for artifacts (Entities)
- [FOAF](foaf.md): Modeling Agents and Organizations

## Sources
- [PROV-O Specification](https://www.w3.org/TR/prov-o/)
- [raw source](../raw/from-url-prov-o.md)
