# Roadmap

Implementation scorecard for Process Assistant (PM is the first domain pack).
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
| **Closure Package**           |   **5**   |  5   | ✅ Complete    |
| **Total**                     |  **27**   |  27  |                |

### Closure Package detail

| #   | Document                  | Status       |
| --- | ------------------------- | ------------ |
| 30  | Handover Document         | ✅ Complete  |
| 31  | Final Project Report      | ✅ Complete  |
| 32  | Lessons Learned Report    | ✅ Complete  |
| 33  | Archive Index             | ✅ Complete  |
| 34  | Project Closure Statement | ✅ Complete  |

---

## Infrastructure Milestones

| Milestone                           | Issues | Done | Status          | Blocked by           |
| ----------------------------------- | :----: | :--: | --------------- | -------------------- |
| M3 · Artifact Hygiene               |   9    |  5   | 🔄 In progress  | —                    |
| M4 · Phase Manifests & Prompts      |   5    |  5   | ✅ Complete     | —                    |
| M5 · Process Agent                  |   1    |  1   | ✅ Complete     | —                    |
| M5.1 · Agent Quality                |   3    |  2   | 🔄 In progress  | —                    |
| M6 · Process Agent: Control & State |   1    |  0   | ⏳ Ready        | —                    |
| M7 · Skills & Automation            |   4    |  0   | 🔄 In progress  | —                    |

### M3 · Artifact Hygiene

| #   | Issue                                                          | Status       |
| --- | -------------------------------------------------------------- | ------------ |
| 44  | Artifact layer: annotate gate output type                      | ✅ Closed    |
| 45  | Artifact layer: define deferred_value convention               | ✅ Closed    |
| 46  | Artifact layer: add structured validation rules to gates       | ✅ Closed    |
| 47  | Tooling: add instructions-schema.json                          | ✅ Closed    |
| 50  | Artifact layer: define orchestrator interface contract         | ✅ Closed    |
| 51  | wiki: update PROMONT URL                                       | ⏳ Open      |
| 52  | wiki: verify SNOMED CT member country count                    | ⏳ Open      |
| 53  | wiki: audit foaf:currentProject usage in ontology             | ⏳ Open      |
| 54  | ontology: full audit — correctness, PROV-O grounding, SHACL   | ⏳ Open      |

### M4 · Phase Manifests & Prompts

| #   | Issue                                              | Status      |
| --- | -------------------------------------------------- | ----------- |
| 40  | Manifest: Planning phase                           | ✅ Closed   |
| 41  | Manifest: Execution phase                          | ✅ Closed   |
| 42  | Manifest: Monitoring & Control phase               | ✅ Closed   |
| 43  | Manifest: Closure phase                            | ✅ Closed   |
| 48  | Agent prompts for all phases                       | ✅ Closed   |

### M5 · Process Agent

| #   | Issue                                                              | Status      |
| --- | ------------------------------------------------------------------ | ----------- |
| 39  | Process agent: drive and transition artifacts via ontology-encoded lifecycle | ✅ Closed |

Shipped: `python -m agent` CLI, gate loop, session persistence, eval runner
with scripted and real-model modes. See ADR-006, ADR-007, ADR-008.

### M5.1 · Agent Quality _(follow-ups from M5)_

| #   | Issue                                              | Status       |
| --- | -------------------------------------------------- | ------------ |
| 72  | Exercise eval with real agent end-to-end           | ✅ Closed    |
| 73  | test: unit tests for llm_judge parse logic         | ✅ Closed    |
| 67  | feat: eval harness for process agent               | ⏳ Open      |
| 78  | Process agent: write RDF instance files so SHACL validation can run | ⏳ Open |

### M6 · Process Agent: Control & State

| #   | Issue                                                                          | Status  |
| --- | ------------------------------------------------------------------------------ | ------- |
| 49  | Process agent: human-in-the-loop review, out-of-order navigation, multi-project state | ⏳ Open |

M5 is complete — this milestone is unblocked. Start #65 (LangGraph spike) when
#49 is picked up (see ADR-006).

### M7 · Skills & Automation

| #   | Issue                                              | Status       |
| --- | -------------------------------------------------- | ------------ |
| 55  | Skill: author a gate-based document template pack  | ⏳ Open      |
| 56  | Skill: author a SHACL NodeShape from references    | ⏳ Open      |
| 57  | Skill: author an OWL class into a Turtle module    | ⏳ Open      |
| 75  | Build scaffold tools for shacl-shape and template-pack skills | ⏳ Open |

Draft skills exist in `.agents/skills/template-pack/` and
`.agents/skills/shacl-shape/`; issues stay open until scaffold tooling (#75)
lands and the skills are exercised end-to-end.

### M8 · Generic Process Framework _(stretch goal)_

Extract the domain-agnostic core so any structured process — compliance
audits, clinical trials, procurement, HR onboarding — can plug in its own
OWL ontology + gate-based template packs and get the same AI-guided
document generation that PM gets today.

| #  | Issue                                                          | Status      |
| -- | -------------------------------------------------------------- | ----------- |
| 68 | feat: domain-agnostic workflow agent                           | ⏳ Open     |
| —  | Define domain-pack spec (ontology + templates + manifest contract) | 🔮 Future |
| —  | Extract domain-agnostic process agent core from PM impl        | 🔮 Future   |
| —  | Pilot: second domain (e.g. compliance audit or software delivery) | 🔮 Future |

ADR-009 adopted `domains/pm/` layout and rebased the `pm:` namespace — the
packaging shape is in place; #68 tracks runtime discovery, validation, and
authoring docs.

---

## Sequencing

```
✅ Closure Package (27 templates)
✅ M4 · Phase Manifests & Prompts
✅ M5 · Process Agent
         │
         ├────────────────────────────┬──────────────────────────┐
         ▼                            ▼                          ▼
M6 · Control & State            M5.1 · Agent Quality        M3 · Artifact Hygiene
(#49, then spike #65)           (#67 eval harness,          (wiki + ontology
                                 #78 RDF ingest)              cleanup — #51–54)
         │                            │
         └────────────┬───────────────┘
                      ▼
              M8 · Generic Process Framework  (stretch — #68)

M7 · Skills & Automation  (parallel — #55–57, #75)
```

M7 can run in parallel with any other milestone.
M5 shipped with the M3 contract (#50) and M4 manifests complete.
M6 depends on M5 — now unblocked.
M5.1 hardens the shipped agent; #78 unblocks real SHACL validation.
M8 depends on M6 — the PM agent must be stable before extracting a generic core.

---

## Exploratory Spikes

Time-boxed investigations. Each produces a written recommendation or go/no-go — not direct deliverables.

| #  | Issue                                                  | Emerged from | Status  |
| -- | ------------------------------------------------------ | ------------ | ------- |
| 62 | Spike: conditional gate branching in instructions.yaml | #47 / M3     | ⏳ Open |
| 63 | Spike: auto-generate SHACL shapes from pm: ontology   | #47 / M3     | ⏳ Open |
| 65 | Spike: evaluate LangGraph as orchestration layer       | ADR-006 / M6 | ⏳ Open — **start when #49 is picked up** |
| 69 | Spike: scaffold generator for _project-manifest.yaml phases block | #50 / ADR-008 | ⏳ Open |

---

## Open issues without a milestone

| #  | Issue                                | Notes |
| -- | ------------------------------------ | ----- |
|  1 | Ingest base ontologies into llm-wiki | |
| 61 | chore: consider renaming the repository | **Done** — repo is `process-assistant`; see ADR-009. Close when convenient. |
