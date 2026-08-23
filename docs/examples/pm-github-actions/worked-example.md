# Worked Example — PM Initiation as a GitHub Actions State Machine

> [!WARNING]
> **ILLUSTRATIVE ONLY — DO NOT ACTIVATE**
>
> This document simulates [`pm-01-initiation.yml`](./pm-01-initiation.yml), which contains known
> security defects (script injection, no concurrency control, no authorization).
> It exists to illustrate an architectural pattern, not to be run.

---

## What this shows

The `issue_comment` event-driven state machine pattern: instead of a linear
script with `echo` statements pretending to be gates, each gate is a real
GitHub event cycle. The workflow posts a prompt and exits. A human reply
triggers the next run.

```
workflow_dispatch ──► open Issue ──► post Gate 1 prompt ──► EXIT
                                             │
                                     human replies in Issue
                                             │
                              issue_comment trigger fires
                                             │
                                     read active gate label
                                             │
                                  validate comment body
                                      │           │
                                    FAIL        PASS
                                      │           │
                               post "try      tick checklist
                               again" note    advance label
                               EXIT           post Gate N+1
                                              prompt & EXIT
                                                   │
                                          (repeat until Gate 12)
                                                   │
                                          post completion comment
                                          dispatch next document
                                          EXIT
```

**State storage:** a GitHub Issue label (`pm:gate:N`). Visible in the UI at
all times. No hidden state, no database.

**Known limitation (no LLM):** Validation is structural, not semantic.
Format hints in each prompt are load-bearing — the human must follow them
exactly or the regex parser rejects the answer. With an LLM in the loop,
format hints become advisory.

---

## Simulation

### Step 1 — PM triggers `workflow_dispatch`

```
Workflow:     PM · Phase 1 · Initiation
project_name: Unified Reporting Platform
sponsor:      Jane Smith
document:     project-proposal

▶ Run workflow
```

---

### Step 2 — Workflow opens the tracking Issue

> **[PM · Initiation] Unified Reporting Platform — project-proposal** `#47`
>
> Labels: `pm:gate` · `pm:initiation` · `pm:project-proposal` · `pm:gate:1`
>
> ---
> ## PM Document: `project-proposal`
> **Phase:** Initiation | **Project:** Unified Reporting Platform | **Sponsor:** Jane Smith
> **Ontology class:** pm:ProjectProposal
>
> ---
> ## Gates
> <!-- The workflow ticks these as each gate passes. -->
> - [ ] Gate 1  · project_name         [dct:title]
> - [ ] Gate 2  · problem_statement     [dct:description]
> - [ ] Gate 3  · objectives            [proj:purpose]
> - [ ] Gate 4  · expected_benefits     [proj:purpose]
> - [ ] Gate 5  · scope_in
> - [ ] Gate 6  · scope_out
> - [ ] Gate 7  · sponsor               [pm:hasSponsor]
> - [ ] Gate 8  · stakeholders          [pm:RoleAssignment]
> - [ ] Gate 9  · rough_budget          [pm:budget]  *(optional)*
> - [ ] Gate 10 · rough_timeline        [pm:plannedEndDate]  *(optional)*
> - [ ] Gate 11 · risks_assumptions     [pm:Risk]
> - [ ] Gate 12 · authorization_request

---

### Step 3 — Bot posts Gate 1 prompt

> **github-actions[bot]**
>
> ## 🔖 Gate 1 of 12 — Project Name
> *maps\_to: `dct:title` · required*
>
> What is the name of this project?
>
> **Format** *(validation is structural — follow this exactly)*
> ```
> Name: <your project name>
> ```
>
> **Rules:** Must be a proper noun phrase. Avoid generic names like "New System".
>
> > Reply with the formatted block above.

---

### Step 4 — PM replies ✅

> **s.mcelhose**
>
> ```
> Name: Unified Reporting Platform
> ```

`issue_comment` trigger fires → Workflow run #2 starts.
`parse()` → `"Unified Reporting Platform"` · `validate()` → `null` (pass).
Label rotated: `pm:gate:1` → `pm:gate:2`. Issue body Gate 1 ticked.

---

### Step 5 — Bot posts Gate 2 prompt (combined accept + next)

> **github-actions[bot]**
>
> ## ✅ Gate 1 — Project Name — accepted
>
> ---
>
> ## 🔖 Gate 2 of 12 — Problem / Opportunity
> *maps\_to: `dct:description` · required*
>
> What problem or opportunity is this project addressing?
> Describe the current situation and why it is unsatisfactory.
>
> **Rules:** Must describe a specific observable problem, not a solution.
>
> **Format** *(required — validation is structural)*
> ```
> Problem: <describe the problem or opportunity here,
>          can span multiple lines>
> ```
>
> > Reply to this comment with the formatted block above.

---

### Step 6 — PM replies without the format prefix ❌

> **s.mcelhose**
>
> We have too many reporting tools and nobody knows which one to use.
> Finance uses Excel, ops uses Tableau, and the exec team gets PDFs
> emailed manually every Friday.

`issue_comment` trigger fires → Workflow run #3 starts.
`parse()` looks for `Problem:` prefix → `null`. `validate(null)` → error.
Label unchanged: still `pm:gate:2`.

---

### Step 7 — Bot rejects

> **github-actions[bot]**
>
> ## ❌ Gate 2 — Problem / Opportunity — format error
>
> **Problem:** Reply must start with `"Problem:"` and describe a specific observable situation.
>
> Check the format hint in the previous prompt and reply again.
>
> > ⚠️ This validator is structural (no LLM). Your answer may be
> > correct but the format must match exactly for it to be accepted.

---

### Step 8 — PM retries with correct format ✅

> **s.mcelhose**
>
> ```
> Problem: We have too many reporting tools and nobody knows which one to use.
>          Finance uses Excel, ops uses Tableau, and the exec team gets PDFs
>          emailed manually every Friday. There is no single source of truth,
>          reconciliation takes 2 days per month, and exec decisions are made
>          on stale data.
> ```

`parse()` → long string · `validate()` → pass (length > 20).
Label: `pm:gate:2` → `pm:gate:3`.

---

### Steps 9–11 — Gates 3–6, PM answers correctly (fast-forward)

Each follows the same accept + next prompt cycle.

Issue body after Gate 6:

> - [x] Gate 1  · project\_name
> - [x] Gate 2  · problem\_statement
> - [x] Gate 3  · objectives
> - [x] Gate 4  · expected\_benefits
> - [x] Gate 5  · scope\_in
> - [x] Gate 6  · scope\_out
> - [ ] Gate 7  · sponsor  ← active label `pm:gate:7`

---

### Step 12 — Gate 7 — `named_individual` validation fails

> **s.mcelhose**
>
> ```
> Sponsor: Data & Analytics Leadership Team
> ```

`parse()` → `"Data & Analytics Leadership Team"`.
`validate()` → regex `/^[A-Z][a-z]+ [A-Z][a-z]+/` fails.

> **github-actions[bot]**
>
> ## ❌ Gate 7 — Proposed Sponsor — format error
>
> **Problem:** Reply must be `"Sponsor: First Last"` — a named individual, not a team or department.
>
> > ⚠️ This validator is structural (no LLM). Your answer may be
> > correct but the format must match exactly for it to be accepted.

> **s.mcelhose**
>
> ```
> Sponsor: Jane Smith
> ```

Pass · `pm:gate:7` → `pm:gate:8`.

---

### Step 13 — Gate 9 — PM skips optional gate

> **github-actions[bot]**
>
> ## 🔖 Gate 9 of 12 — Rough Budget
> *maps\_to: `pm:budget` · optional*
>
> *This gate is optional — reply `skip` to defer.*
>
> **Format**
> ```
> Budget: <e.g. "<€50k", "€100–200k", "TBD">
> ```

> **s.mcelhose**
>
> `skip`

`isSkip && !gate.required` → pass with `deferred_value: "Not yet estimated."`.
`pm:gate:9` → `pm:gate:10`.

---

### Step 14 — Gate 12 passes — completion

> **github-actions[bot]**
>
> ## ✅ Gate 12 — Authorization Request — accepted
>
> ---
>
> ## ✅ Project Proposal — `output_status: draft`
>
> All required gates satisfied.
> **next\_document:** business-case
>
> *dispatching Business Case...*

Issue label `pm:draft` added. Issue closed.
`createWorkflowDispatch` fires `pm-01-initiation.yml` with `document: business-case`.

---

## Final state — Issue #47

| Field      | Value                                                                  |
| ---------- | ---------------------------------------------------------------------- |
| State      | Closed                                                                 |
| Labels     | `pm:gate` · `pm:initiation` · `pm:project-proposal` · `pm:draft`      |
| Checklist  | 12/12 ticked                                                           |
| Runs fired | 14 (1 dispatch + 1 per comment, including retries at Gates 2 and 7)    |

---

## The format-hint tax

Gates 2 and 7 required retries purely because of structural validation.
The PM's first Gate 2 answer was semantically correct — it described an
observable problem. A structural parser cannot know that.

This is the honest cost of running this pattern without an LLM:

| With LLM                              | Without LLM                            |
| ------------------------------------- | -------------------------------------- |
| Format hints advisory                 | Format hints load-bearing              |
| Semantic validation ("is this a real problem?") | Length/regex check only     |
| Retry rate low                        | Retry rate depends on PM discipline    |
| `validate()` calls the model          | `validate()` is a regex               |
