---
type: concept
title: Dublin Core Terms
description: The Dublin Core Metadata Initiative (DCMI) Terms provide a set of cross-domain elements for describing resources.
timestamp: 2024-08-22T00:00:00Z
resource: http://purl.org/dc/terms/
tags: [vocabulary, rdf, metadata, dcmi]
---

# Dublin Core Terms (DCTERMS)

The **Dublin Core Terms** (DCTERMS) represent the most widely used vocabulary for describing digital and physical artifacts. In a project management ontology, these terms provide the foundational metadata for all project-related [[prov-o:Entity]] instances, such as documents, reports, and deliverables.

## Core Metadata Properties

The following properties are essential for artifact metadata:

- **`dcterms:title`**: The name of the artifact.
- **`dcterms:description`**: A summary or account of the artifact.
- **`dcterms:creator`**: The [[foaf:Agent]] (person or organization) responsible for creating the artifact.
- **`dcterms:created`**: The date of the artifact's initial creation (using ISO 8601).
- **`dcterms:modified`**: The date of the artifact's most recent revision.
- **`dcterms:format`**: The file format (e.g., `application/pdf`) or physical medium.
- **`dcterms:subject`**: The topic or keywords associated with the artifact.

## Relational Properties

DCTERMS provides powerful properties for modeling relationships between artifacts:

- **`dcterms:relation`**: A general link to a related resource.
- **`dcterms:hasPart`**: Identifies a child component of the current artifact (e.g., a chapter in a report).
- **`dcterms:isPartOf`**: Identifies the parent container of the artifact (e.g., a document within a project folder).

## Relevance to Project Management

Dublin Core provides the "who, what, when, and where" for project deliverables. While [[prov-o]] models the *process* of how an artifact was created, Dublin Core models the *identity* and *characteristics* of the artifact itself.

- **Artifact Organization**: Using `dcterms:isPartOf` to structure project documentation.
- **Search & Discovery**: Using `dcterms:subject` to categorize deliverables across different [[doap]] projects.
- **Compliance & Audit**: Using `dcterms:created` and `dcterms:modified` to maintain a timeline of project outputs.

## Related Vocabularies
- [[prov-o]]: Complements DCTERMS by providing process-oriented provenance.
- [[foaf]]: Used for the agents linked via `dcterms:creator`.
- [[doap]]: Used to describe the projects that produce these artifacts.

## Sources
- [DCMI Metadata Terms Specification](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/)
- [[raw/from-url-dublin-core]]
