---
type: concept
title: DOAP
description: Description of a Project (DOAP) is an RDF vocabulary to describe software projects, and in particular open-source projects.
timestamp: 2024-08-22T00:00:00Z
resource: http://usefulinc.com/ns/doap#
tags: [vocabulary, rdf, software, project-management]
---

# DOAP: Description of a Project

**DOAP** is a vocabulary for describing software projects. While it is highly specialized for open-source software, its core concepts are foundational for modeling technical projects and their associated resources (like source control and releases).

## Core Classes

- **`doap:Project`**: The main class representing a project.
- **`doap:Version`**: Represents a specific release or milestone of the project.
- **`doap:Repository`**: Represents a source code repository (with subclasses like `doap:GitRepository`, `doap:SVNRepository`).
- **`doap:Specification`**: A document defining a standard or specification implemented by the project.

## Key Properties

- **`doap:name`**: The name of the project.
- **`doap:description`**: A detailed description of the project.
- **`doap:shortdesc`**: A brief, one-sentence summary.
- **`doap:homepage`**: The official web presence for the project.
- **`doap:maintainer`**: The agent ([[foaf:Person]] or [[foaf:Organization]]) responsible for project management and maintenance.
- **`doap:developer`**: An agent responsible for code contribution.
- **`doap:repository`**: Link to the structured repository information.
- **`doap:release`**: Link to a specific `doap:Version`.
- **`doap:created`**: Used within `doap:Version` for the release date.

## DOAP vs. schema.org/Project

While both define a "Project" type, they serve different purposes:
- **DOAP** is technical and granular, focusing on software-specific metadata like version control systems and specific release versions.
- **[[schema-org-project]]** treats a Project as a subtype of an Organization, focusing more on social, corporate, and funding aspects suitable for search engine discovery.

## Relevance to Project Management

DOAP is critical for:
- **Technical Resource Management**: Linking project tasks to specific source code repositories.
- **Release Tracking**: Modeling the evolution of a project through discrete versions.
- **Role Definition**: Distinguishing between maintainers, developers, documenters, and testers (complementing [[foaf]] and [[prov-o]]).

## Related Vocabularies
- [[foaf]]: Used for agents (maintainers, developers).
- [[dublin-core]]: Used for broader metadata (creation dates, subjects).
- [[prov-o]]: Used to model the provenance of project deliverables.

## Sources
- [DOAP Wiki](https://github.com/ewilderj/doap/wiki)
- [[raw/from-url-doap]]
