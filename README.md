# Project Management Ontology

A formal ontology for project management concepts expressed in [Turtle (TTL)](https://www.w3.org/TR/turtle/) and [OWL 2](https://www.w3.org/TR/owl2-overview/), with document templates annotated using [OKF frontmatter](https://okfn.org/) and workflow generation tooling.

## Vision

Project management is the first use case. The deeper goal is a **generic
ontology-based process assistant** — a pattern where any structured process
domain (compliance audits, clinical trial management, procurement, HR
onboarding, software delivery) can bring its own OWL ontology and gate-based
template packs and get the same AI-guided document generation for free.

The PM implementation is the proof of concept. The process agent (M5) is
designed from the start to be domain-agnostic: it reads a manifest, follows
gates, validates against SHACL shapes, and advances a lifecycle — without
knowing anything about project management specifically.

---

## Goals

1. **Formalize** project management concepts (projects, tasks, milestones, risks, roles, deliverables, workflows) as a linked-data ontology
2. **Reuse** well-known base ontologies (PROV-O, DOAP, schema.org, Dublin Core, FOAF)
3. **Visualize** the ontology using standard RDF/OWL tooling
4. **Template** project documents annotated with OKF frontmatter
5. **Generate** workflows from ontology + document templates

## Structure

```
ontology/
├── core/           # Root ontology — imports and binds modules
├── modules/        # Domain modules: project, task, milestone, risk, resource, role, deliverable, workflow
├── imports/        # Cached copies of imported base ontologies
└── shapes/         # SHACL constraint shapes

docs/
├── wiki/           # LLM-wiki knowledge base (llm-wiki skill)
└── templates/      # Document templates with OKF frontmatter

tools/
├── visualize/      # Visualization scripts (Widoco, OWLViz, Graphviz)
└── validate/       # Validation scripts (SHACL, RDFLib)

workflows/          # Derived workflow definitions
```

## Quickstart

```bash
# Validate ontology
make validate

# Visualize (generates HTML docs + SVG graph)
make visualize

# Lint wiki
make wiki-lint
```

## Base Ontologies

| Ontology      | Namespace                                    | Purpose                            |
| ------------- | -------------------------------------------- | ---------------------------------- |
| PROV-O        | `http://www.w3.org/ns/prov#`                 | Provenance, agents, activities     |
| DOAP          | `http://usefulinc.com/ns/doap#`              | Description of a project           |
| schema.org    | `https://schema.org/`                        | General-purpose types and actions  |
| Dublin Core   | `http://purl.org/dc/terms/`                  | Metadata (title, description, etc.)|
| FOAF          | `http://xmlns.com/foaf/0.1/`                 | Agents, persons, organizations     |

## License

[CC BY 4.0](LICENSE)
