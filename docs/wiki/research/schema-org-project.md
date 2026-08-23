---
type: concept
title: schema.org Project
description: schema.org's Project class models a collaborative enterprise as a subtype of Organization, providing general-purpose properties for funding, team membership, and lifecycle dates.
timestamp: 2024-08-22T00:00:00Z
resource: https://schema.org/Project
tags: [vocabulary, schema-org, project-management, seo]
---

# schema.org Project

`schema:Project` is part of the [schema.org](https://schema.org) vocabulary — a shared vocabulary for structured data on the web, primarily used for SEO and knowledge graph annotation.

## Class Hierarchy

```
Thing
  └─ Organization
       └─ Project
            ├─ ResearchProject
            └─ FundingAgency
```

`Project` is a **subclass of `Organization`**, which means it inherits all organizational properties. This is semantically meaningful (a project is a collaborative enterprise) but also practically significant — it means schema.org models project teams via `member`/`employee` rather than dedicated role properties.

## Key Namespace

```
https://schema.org/   (prefix: schema:)
```

## Most Useful Properties for PM Modeling

| Property               | Source        | PM Relevance                                     |
| ---------------------- | ------------- | ------------------------------------------------ |
| `schema:name`          | Thing         | Project name                                     |
| `schema:description`   | Thing         | Project description / scope summary              |
| `schema:identifier`    | Thing         | Project code or ID                               |
| `schema:foundingDate`  | Organization  | Project start date                               |
| `schema:dissolutionDate` | Organization | Project end/close date                          |
| `schema:member`        | Organization  | Team member (use with `OrganizationRole`)        |
| `schema:sponsor`       | Organization  | Project sponsor                                  |
| `schema:funder`        | Organization  | Funding body                                     |
| `schema:funding`       | Organization  | Links to a `Grant` (budget authority)            |
| `schema:subOrganization` | Organization | Sub-project, phase, or work package             |
| `schema:parentOrganization` | Organization | Portfolio or programme this project belongs to |
| `schema:event`         | Organization  | Project milestones, review gates, kickoffs       |
| `schema:keywords`      | Organization  | Tags / classification                            |

## Adjacent Classes Useful for PM

| Class                 | Role in PM context                                              |
| --------------------- | --------------------------------------------------------------- |
| `schema:Action`       | Tasks or activities (e.g., `PlanAction`, `CreateAction`)        |
| `schema:Event`        | Milestones, sprints, ceremonies                                 |
| `schema:OrganizationRole` | Typed team membership (PM, sponsor, developer)             |
| `schema:Grant`        | Budget authority / funding                                      |
| `schema:CreativeWork` | Deliverables, documents, reports                                |

## Comparison: schema.org vs DOAP vs PROJ

| Concern               | [schema.org Project](schema-org-project.md)   | [DOAP](doap.md)                  | [PROJ Ontology](proj-ontology.md)         |
| --------------------- | ------------------------ | ------------------------- | ------------------------- |
| General project type  | ✅ Yes (broad)           | ❌ Software only          | ✅ Yes (domain-neutral)   |
| Roles & team          | ⚠️ Via Organization      | ✅ Named dev roles        | ✅ Via PROV-O Agent       |
| Milestones            | ⚠️ Via Event             | ❌ No                     | ✅ Native                 |
| Linked data fit       | ⚠️ SEO-oriented          | ✅ RDF-native             | ✅ RDF-native             |
| Extensibility         | ✅ additionalType         | ⚠️ Limited                | ✅ Profile pattern        |

## Assessment for This Project

schema.org/Project is best used as a **bridge layer** for public discoverability and SEO annotation rather than a formal ontological base. Its `Thing` and `Organization` properties (especially `name`, `description`, `identifier`, `foundingDate`, `member`) are useful for mapping to Dublin Core-style metadata. However, the class hierarchy (Project ⊆ Organization) is semantically awkward for a formal PM ontology — a project is not an organization.

**Verdict**: Use selected schema.org properties as annotation targets for external discoverability, not as the structural backbone of the ontology.

## Sources

- [raw source](../raw/from-url-schema-org-project.md) — https://schema.org/Project
- [initial research](../raw/initial-research-user.md)

## See Also

- [DOAP](doap.md) — comparison vocabulary
- [PROJ Ontology](proj-ontology.md) — comparison vocabulary
