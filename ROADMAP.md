# Roadmap

Implementation scorecard for the Project Management Ontology.
Updated manually — one row per milestone, one tick per issue closed.

---

## Template Layer — Phase Packages

Each package delivers one template pack per PM document in that phase:
`entry.yaml` + `instructions.yaml` + `template.md` + SHACL shape.

| Package                       | Templates | Done | Status         |
| ----------------------------- | :-------: | :--: | -------------- |
| Initiation Package            |     4     |  4   | ✅ Complete    |
| Planning Package              |     8     |  8   | ✅ Complete    |
| Execution Package             |     4     |  4   | ✅ Complete    |
| Monitoring & Control Package  |     6     |  6   | ✅ Complete    |
| **Closure Package**           |   **5**   |  0   | 🔄 In progress |
| **Total**                     |  **27**   |  22  |                |

### Closure Package detail

| #   | Document                  | Branch               | Status  |
| --- | ------------------------- | -------------------- | ------- |
| 30  | Handover Document         | feat/closure-package | ⏳ Open |
| 31  | Final Project Report      | feat/closure-package | ⏳ Open |
| 32  | Lessons Learned Report    | feat/closure-package | ⏳ Open |
| 33  | Archive Index             | feat/closure-package | ⏳ Open |
| 34  | Project Closure Statement | feat/closure-package | ⏳ Open |

---

## Infrastructure Milestones

| Milestone                       | Issues | Done | Status          | Blocked by           |
| ------------------------------- | :----: | :--: | --------------- | -------------------- |
| M3 · Artifact Hygiene           |   9    |  0   | ⏳ Not started  | —                    |
| M4 · Phase Manifests & Prompts  |   5    |  4   | 🔄 In progress  | Closure Package (#43)|
| M5 · ADK Agent                  |   1    |  0   | ⏳ Not started  | M3, M4               |
| M6 · Orchestrator               |   1    |  0   | ⏳ Not started  | M5                   |
| M7 · Skills & Automation        |   3    |  0   | ⏳ Not started  | —                    |

### M3 · Artifact Hygiene

| #   | Issue                                                          | Status  |
| --- | -------------------------------------------------------------- | ------- |
| 44  | Artifact layer: annotate gate output type                      | ⏳ Open |
| 45  | Artifact layer: define deferred_value convention               | ⏳ Open |
| 46  | Artifact layer: add structured validation rules to gates       | ⏳ Open |
| 47  | Tooling: add instructions-schema.json                          | ⏳ Open |
| 50  | Artifact layer: define orchestrator interface contract         | ⏳ Open |
| 51  | wiki: update PROMONT URL                                       | ⏳ Open |
| 52  | wiki: verify SNOMED CT member country count                    | ⏳ Open |
| 53  | wiki: audit foaf:currentProject usage in ontology             | ⏳ Open |
| 54  | ontology: full audit — correctness, PROV-O grounding, SHACL   | ⏳ Open |

### M4 · Phase Manifests & Prompts

| #   | Issue                                              | Status      |
| --- | -------------------------------------------------- | ----------- |
| 40  | Manifest: Planning phase                           | ✅ Closed   |
| 41  | Manifest: Execution phase                          | ✅ Closed   |
| 42  | Manifest: Monitoring & Control phase               | ✅ Closed   |
| 43  | Manifest: Closure phase                            | ⏳ Open     |
| 48  | Agent prompts for all phases                       | ✅ Closed   |

### M5 · ADK Agent

| #   | Issue                                              | Status  |
| --- | -------------------------------------------------- | ------- |
| 39  | Build Python ADK agent for OKF wiki + template Q&A | ⏳ Open |

### M6 · Orchestrator

| #   | Issue                                                  | Status  |
| --- | ------------------------------------------------------ | ------- |
| 49  | Orchestrator: multi-agent coordination across lifecycle | ⏳ Open |

### M7 · Skills & Automation

Generic csgdaa-code skills, reusable outside this project.
Developed from patterns discovered in the Closure Package.

| #   | Issue                                              | Status  |
| --- | -------------------------------------------------- | ------- |
| 55  | Skill: author a gate-based document template pack  | ⏳ Open |
| 56  | Skill: author a SHACL NodeShape from references    | ⏳ Open |
| 57  | Skill: author an OWL class into a Turtle module    | ⏳ Open |

---

## Sequencing

```
Closure Package ──────────────────────────────────┐
  └── M4 (Closure manifest #43) ─────────────────┤
                                                  ▼
                                   M3 · Artifact Hygiene
                                          │
                                          ▼
                                   M5 · ADK Agent
                                          │
                                          ▼
                                   M6 · Orchestrator

M7 · Skills & Automation  (parallel — no hard dependency)
```

M7 can run in parallel with any other milestone.
M3 and M4 can overlap once the Closure Package PR is merged.
M5 depends on M3 (interface contract) and M4 (manifests complete).
M6 depends on M5.

---

## Open issues without a milestone

| #  | Issue                              |
| -- | ---------------------------------- |
| 1  | Ingest base ontologies into llm-wiki |
