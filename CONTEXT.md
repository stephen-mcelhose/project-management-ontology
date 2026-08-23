# Process Assistant

A domain-agnostic process assistant: OWL vocabulary plus gate-based document
templates. Project management is the first packed domain, not the product.

## Language

**Process Assistant**:
The repository and the runtime pattern: read a manifest, walk gates, validate
against SHACL, emit documents.
_Avoid_: Project Management Ontology (as the product name)

**Domain**:
One ontology + SHACL + template-pack set the assistant can load (today: PM).
_Avoid_: calling the whole repo "the ontology"

**pm: namespace**:
The PM OWL namespace
`https://stephen-mcelhose.github.io/project-management-ontology/`. Historical
GitHub Pages path; not renamed with the git repo.
_Avoid_: treating that URL as the current GitHub repo name
