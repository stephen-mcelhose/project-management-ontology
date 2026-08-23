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

## The Two-Layer Pattern

The core insight behind this repository is that a structured process —
any structured process — is built from two distinct and separable layers:

**Layer 1 — the domain** answers *"what are things?"*

An ontology defines the vocabulary: what a `Risk` is, what properties a
`ProjectCharter` has, what `pm:hasSponsor` means, how a `Gate` relates to a
`Phase`. It is a schema for concepts, not a script for behaviour. The OWL/Turtle
files in `ontology/` are this layer.

**Layer 2 — the steps** answers *"what happens, and when?"*

A workflow layer defines the process: which gates must be completed before a
document is draft-complete, what format is required for each answer, who must
approve before the next phase begins, what triggers the transition. The
`instructions.yaml` and `_manifest.yaml` files in `templates/` are this layer.

These two layers are complementary. The ontology does not know about sequence.
The workflow does not know about semantics. Together they define a
domain-specific process assistant.

### A concrete illustration

Once you see the layers separately, you see that the workflow layer can be
expressed in many ways. The `_manifest.yaml` gate sequences are structurally
identical to a GitHub Actions workflow:

| Concept in `templates/`              | Concept in GitHub Actions               |
| ------------------------------------ | --------------------------------------- |
| `pm:Phase`                           | A workflow file                         |
| `pm:Document`                        | A job                                   |
| Gate in `instructions.yaml`          | A step within a job                     |
| `dependencies: [doc-a]`              | `needs: [job-a]`                        |
| `required: true`                     | Step failure blocks the job             |
| `required: false`                    | `continue-on-error: true`               |
| `shared_context:`                    | Workflow-level `env:` / job `outputs:`  |
| `completion.transition_condition`    | Phase-gate job + environment approval   |
| `next_phase: planning`               | `createWorkflowDispatch` at the end     |

The ontology layer (`ontology/*.ttl`) has no equivalent in GitHub Actions —
it holds the semantic meaning that the workflow engine operates on but does
not understand. That is the point: the engine is generic; the domain is
pluggable.

See [`docs/examples/pm-github-actions/`](docs/examples/pm-github-actions/)
for a full illustration, including a worked example simulating a PM completing
the Project Proposal gate sequence via GitHub Issue comments.

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

## Agent

### CLI — interactive terminal

```bash
make agent-run
# or via ADK directly:
adk run agent/
```

### UI — ADK web interface

```bash
adk web agent/
# then open http://localhost:8000
```

The web UI lets you chat with the agent in a browser. The agent reads `templates/` and writes completed documents to `output/`.

Start with the phase and document you want — e.g. *"I want to create a Project Proposal"* — and the agent walks you through the gates, capturing anything you volunteer along the way.

### Tests

```bash
make agent-test          # unit tests — no network, always runs in CI
```

### Evals

Evals drive the real model through scripted scenarios and assert on captured gate answers, tool call sequences, and rendered output.

```bash
# Scripted mode — deterministic, no Vertex AI credentials needed.
# Cases without scripted_responses are skipped.
.venv/bin/python -m pytest agent/evals/ -v

# Real-model mode — requires Vertex AI credentials (GOOGLE_CLOUD_PROJECT etc.).
# Gate answer assertions use an LLM judge (semantic equivalence, not exact match).
make agent-eval
# or:
.venv/bin/python -m pytest agent/evals/ --run-evals -v

# Run a single case:
.venv/bin/python -m pytest "agent/evals/test_eval_cases.py::test_eval_case[initiation-freeform]" --run-evals -v
```

Eval cases live in `agent/evals/cases/`. Each YAML file is a self-contained scenario with turns, scripted responses, and assertions.

---

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
