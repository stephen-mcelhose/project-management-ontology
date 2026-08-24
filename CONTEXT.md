# Process Assistant

A domain-agnostic process assistant: OWL vocabulary plus gate-based document
templates. Project management is the first packed domain, not the product.

## Language

**Process Assistant**:
The repository and the runtime pattern: read a manifest, walk gates, validate
against SHACL, emit documents.
_Avoid_: Project Management Ontology (as the product name)

**Domain**:
One ontology + SHACL + template-pack set the assistant can load, living under
`domains/{name}/` (today: `domains/pm/`).
_Avoid_: calling the whole repo "the ontology"

**pm: namespace**:
The PM OWL namespace
`https://stephen-mcelhose.github.io/process-assistant/pm/`. One base per
domain; the `/pm/` segment mirrors `domains/pm/`.
_Avoid_: dropping the `/pm/` segment, or reusing this base for another domain
