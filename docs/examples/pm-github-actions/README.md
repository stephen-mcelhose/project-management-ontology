# PM Workflow as GitHub Actions — Illustrative Example

> [!WARNING]
> **ILLUSTRATIVE ONLY — DO NOT MOVE `pm-01-initiation.yml` TO `.github/workflows/`**
>
> The workflow file in this directory contains known security defects that were
> deliberately left unfixed to keep the illustration readable:
>
> - **SCRIPT INJECTION** — `inputs.sponsor` and `inputs.project_name` are
>   interpolated directly into JavaScript string literals. A value containing
>   a single quote breaks the script; a crafted value executes arbitrary JS.
> - **NO CONCURRENCY CONTROL** — rapid successive comments trigger simultaneous
>   runs that corrupt the label-based state machine.
> - **NO AUTHORIZATION** — any commenter can advance a gate.
>
> This is an illustrative artifact. GitHub only executes workflows under
> `.github/workflows/` — files here are inert.

---

## The point of this example

**Ontology** defines what things *are*. **GitHub Actions** are acting as the workflow engine, defines what things *do*.
They are complementary layers, not alternatives.

| Concept in `domains/pm/ontology/` + `domains/pm/templates/`     | Concept in `pm-01-initiation.yml`                     |
| ----------------------------------------- | ----------------------------------------------------- |
| `pm:Phase`                                | A workflow file                                       |
| `pm:Document` (`entry.yaml`)              | A dispatched instance of the workflow                 |
| `pm:WorkflowStep` / Gate (`instructions.yaml`) | A branch in the gate-router step                 |
| `dependencies: [doc-a, doc-b]`            | `needs: [job-a, job-b]`                               |
| `shared_context:` (manifest)              | Issue body — written once, read by all subsequent runs |
| `maps_to: dct:title` (gate field)         | Comment annotation + output key                       |
| `required: true` (gate field)             | Validation failure → retry prompt posted              |
| `required: false` (gate field)            | `skip` reply accepted; `deferred_value` used          |
| `completion.transition_condition`         | Gate 12 pass → `createWorkflowDispatch` next document |
| `next_document: business-case`            | `workflow_id: pm-01-initiation.yml, document: business-case` |

The ontology answers: *"What is a Risk? What properties does a ProjectCharter have?
What does `pm:hasSponsor` mean?"*

The workflow answers: *"When does a gate open? What format is required? Who
approves? What happens when all gates pass?"*

---

## How the state machine works

This is **not** a linear script. Each workflow run is short-lived — it posts
one gate prompt then exits. A human comment triggers the next run.

```
workflow_dispatch ──► open Issue ──► post Gate 1 prompt ──► EXIT
                                             │
                                     human replies in Issue
                                             │
                              issue_comment trigger fires
                                             │
                                     read label: pm:gate:N
                                             │
                                  validate reply format
                                      │           │
                                    FAIL        PASS
                                      │           │
                               retry prompt   tick checklist
                               EXIT           advance label to N+1
                                              post Gate N+1 prompt
                                              EXIT
                                                   │
                                          (repeat until Gate 12)
                                                   │
                                          close Issue, add pm:draft
                                          dispatch next document
                                          EXIT
```

**State** is stored as a GitHub Issue label (`pm:gate:3`, etc.) — visible
in the UI at all times, no hidden store.

---

## Known limitation — no LLM

Without an LLM, validation is structural (regex), not semantic. Format hints
in each gate prompt are **load-bearing**: the PM must follow them exactly or
the parser rejects the answer even if the content is correct.

With an LLM in the loop, `validate()` would call the model, format hints
would become advisory, and retry rate would drop significantly.

See [`worked-example.md`](./worked-example.md) for a full simulation showing
two validation failures and an optional gate skip.

---

## Files

| File                  | Purpose                                              |
| --------------------- | ---------------------------------------------------- |
| `pm-01-initiation.yml` | The illustrative workflow (Initiation phase only)   |
| `worked-example.md`   | Step-by-step simulation of the workflow running      |
| `README.md`           | This file — the analogy and architecture explained   |
