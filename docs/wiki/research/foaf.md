---
type: concept
title: FOAF
description: Friend of a Friend (FOAF) is an ontology describing persons, their activities and their relations to other people and objects.
timestamp: 2024-08-22T00:00:00Z
resource: http://xmlns.com/foaf/0.1/
tags: [vocabulary, rdf, social, agent]
---

# FOAF: Friend of a Friend

**FOAF** is a foundational vocabulary for describing people and the social organizations they belong to. In the context of project management, FOAF provides the classes and properties needed to model project team members, stakeholders, and organizational structures.

## Core Classes

- **`foaf:Agent`**: The base class for any entity that can perform actions (includes people, organizations, and software).
- **`foaf:Person`**: A human being involved in a project.
- **`foaf:Organization`**: A formal body (company, department, etc.) involved in or sponsoring a project.
- **`foaf:Group`**: A collection of agents (e.g., a project task force).

## Key Properties

- **`foaf:name`**: The primary name of the person or organization.
- **`foaf:mbox`**: A unique identifier for an agent via their email address (often used for merging data across systems).
- **`foaf:member`**: Indicates that an agent is part of a group or organization.
- **`foaf:currentProject`**: Links a person to a project they are currently working on.
- **`foaf:pastProject`**: Links a person to a project they have previously completed.

> **Spec status**: Both `foaf:currentProject` and `foaf:pastProject` carry
> `term_status: testing` in the FOAF 0.1 specification — they are not marked
> stable and should be used with caution in production linked data. Consult
> the [FOAF specification](http://xmlns.com/foaf/spec/) for the current term
> status of any property before use.

## FOAF Agents and Project Roles

While FOAF provides the basic link between people and projects, it does not natively define specific "roles" (like Scrum Master or Lead Developer). Instead, it is designed to be extended by other vocabularies:

- **[DOAP](doap.md)**: Provides specific properties like `doap:maintainer` and `doap:developer` that refine the general `foaf:maker` relationship.
- **[PROV-O](prov-o.md)**: Uses `prov:Agent` (a superclass of `foaf:Agent`) to connect people to specific activities and their outcomes.

## Relevance to Project Management

FOAF is essential for:
- **Resource Management**: Uniquely identifying team members across different tools using `foaf:mbox`.
- **Stakeholder Analysis**: Mapping the relationships and organizations involved in a project.
- **Communication Mapping**: Providing the contact information and organizational context for project participants.

## Related Vocabularies
- [DOAP](doap.md): Refines FOAF agent links with software-specific roles.
- [PROV-O](prov-o.md): Models the responsibility of FOAF agents for project activities.
- [Dublin Core](dublin-core.md): Connects FOAF agents to the artifacts they create (`dcterms:creator`).

## Sources
- [FOAF Specification](http://xmlns.com/foaf/spec/)
- [raw source](../raw/from-url-foaf.md)
