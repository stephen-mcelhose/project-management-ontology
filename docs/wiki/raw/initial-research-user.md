# Raw Research: PM Ontology Landscape (User-provided)

> Source: user-provided research note, 2024-08-22
> Status: READ-ONLY — never edit this file

---

Because the Project Management Institute (PMI) treats the PMBOK Guide text as highly protected
proprietary intellectual property, there is no officially sanctioned, single global W3C-endorsed
PMBOK ontology download (unlike standard domains like medical with SNOMED or finance with FIBO).
However, several highly respected, pre-existing, open-access academic and enterprise ontologies
perfectly fit the goal of mapping project management and documentation artifacts.

## 1. The PROJECT Ontology (PROJ)

Managed and hosted by the official BioPortal registry, this is a highly standardized profile
extended directly from the W3C's native PROV-O (Provenance Ontology) specification.

- **What it does**: Provides a domain-neutral profile explicitly designed to publish information
  describing project structures, goals, milestones, and project planning components.
- **Documentation**: BioPortal PROJ Registry — https://bioportal.bioontology.org
- **Usage pattern**: Links actions to things. Document versions mapped as subclass items of
  prov:Entity that are generated or altered by standard project milestones.

## 2. PROMONT Ontology

Developed specifically as an open-source reference ontology to represent the complete lifecycle
and engineering breakdown of complex project management operations.

- **What it does**: Bridges standard web services and physical business processes, mapping
  workflows directly to specific decision points, executions, and deliverables.
- **Reference**: https://ai.ia.agh.edu.pl
- **Use case**: Semantic middleware setups validating task dependencies against corporate file
  submissions.

## 3. SEON (Software Engineering Ontology Network) – SPO & SPMS

If documents involve technical/IT/software/digital engineering project spaces, the Software
Project Management Ontology (SPMO / SPMS) is excellent.

- **What it does**: Built explicitly to solve the "Semantic Documentation" problem — maps
  real-world spreadsheets, text files, and wiki entries directly to project scope, schedule,
  and cost tracking.
- **Documentation**: https://www.inf.ufes.br
- **Research**: Using Semantic Documentation in Project Management

## 4. ProjectCO v2.0 (Project Management Core Ontology)

Published on ResearchGate, a multi-tier architectural project ontology mapping organizational
entities to deep project attributes.

- **What it does**: Breaks down foundational structures of tasks, resources, assignments, and
  temporal limits into an actionable class matrix.
- **Documentation**: https://www.researchgate.net

## Supporting Vocabularies Recommended

| Vocabulary     | Key properties                                          | Role                                      |
| -------------- | ------------------------------------------------------- | ----------------------------------------- |
| Dublin Core    | `dcterms:format`, `dcterms:creator`, `dcterms:created` | Artifact metadata                         |
| W3C PROV-O     | `prov:wasGeneratedBy`, `prov:used`                      | Which project phase generated which file  |

## Source URLs

- [1] https://keet.wordpress.com — PMI/PMBOK ontology IP commentary
- [2] https://www.ovaledge.com
- [3] https://www.inf.ufes.br — SEON/SPMO
- [4] https://www.inf.ufes.br
- [5] https://bioportal.bioontology.org — PROJ ontology
- [6] https://ai.ia.agh.edu.pl — PROMONT
- [7] https://www.researchgate.net — SEON/SPMO research paper
- [8] https://www.researchgate.net — ProjectCO v2.0
