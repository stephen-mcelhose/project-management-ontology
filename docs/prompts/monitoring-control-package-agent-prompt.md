---
type: runbook
title: Monitoring & Control Package Agent Prompt
description: Agent instructions for building the Monitoring & Control Package template packs (Issues #25–#29).
timestamp: 2026-08-23T00:00:00Z
tags: [prompt, agent, monitoring-control]
---

## Task: Build Monitoring & Control Package template packs — Issues #25–#29

**Repo:** `/Users/stephen.mcelhose.ext/repos/process-assistant`
**GitHub:** `stephen-mcelhose/process-assistant`

---

### Prerequisite

The Planning Package (Milestone #2) is recommended but not strictly required. Templates are independent files — the only risk of parallel execution is ontology merge conflicts if multiple agents edit document.ttl simultaneously.
Monitoring & Control runs in parallel with Execution in practice, but the templates reference planning-phase documents as their baseline.

---

### Context

This repo contains a project management ontology (OWL/Turtle) and a growing library of document templates. Each PM document class has a corresponding template pack: three files plus a SHACL validation shape. One completed pack serves as the reference example:

```
templates/initiation/project-proposal/
  entry.yaml          ← metadata, standard citations, dependency chain, package
  instructions.yaml   ← agent gates (one per standard field, ordered, with maps_to)
  template.md         ← Markdown scaffold with {{placeholders}} and <!-- maps to --> comments
shapes/initiation/project-proposal.shacl.ttl
```

Read all four of these files before writing anything. They define the exact format expected.

---

### Your job

Build template packs for all five Monitoring & Control Package issues. **Parallelize research (Step 1) across all documents** — fetching PRINCE2 URLs and reading `document.ttl` has no shared state. **Do ontology gap-checking (Step 2) as a single consolidated pass** across every document in this batch before writing any template — documents in the same package frequently need the same or overlapping ontology properties (e.g. shared fields on `pm:Project`), and editing `ontology/modules/*.ttl` concurrently from multiple agents/sessions risks conflicting or duplicate properties. Once the ontology is settled and validated, templates and shapes (Steps 3–4) can again be written in parallel per document:

| Issue | Document | Ontology class | PRINCE2 source |
| ----- | -------- | -------------- | -------------- |
| [#25](https://github.com/stephen-mcelhose/process-assistant/issues/25) | Status Report | `pm:StatusReport` | https://prince2.wiki/management-products/reports/highlight-report/ |
| [#26](https://github.com/stephen-mcelhose/process-assistant/issues/26) | Risk Register | `pm:RiskRegister` | https://prince2.wiki/management-products/project-log/risk-register/ |
| [#27](https://github.com/stephen-mcelhose/process-assistant/issues/27) | Issue Log | `pm:IssueLog` | https://prince2.wiki/management-products/project-log/issue-register/ |
| [#28](https://github.com/stephen-mcelhose/process-assistant/issues/28) | Decision Log | `pm:DecisionLog` | https://prince2.wiki/management-products/project-log/daily-log/ |
| [#29](https://github.com/stephen-mcelhose/process-assistant/issues/29) | Change Log | `pm:ChangeLog` | https://prince2.wiki/management-products/baselines/management-approaches/issue/ |

> **Note:** These are living registers and logs — they are opened at the start of a project and maintained throughout. Templates should reflect this: sections should be structured as register/log entries (rows in a table or repeated blocks), not as one-time authored documents. The template captures the *schema for a single entry*, not the full register at a point in time.

Output paths follow this pattern:
```
templates/monitoring-control/{kebab-name}/entry.yaml
templates/monitoring-control/{kebab-name}/instructions.yaml
templates/monitoring-control/{kebab-name}/template.md
shapes/monitoring-control/{kebab-name}.shacl.ttl
```

---

### Step 0 — Environment setup (do this first)

```bash
git fetch origin
git rebase origin/main          # your worktree may predate later ontology/prompt commits
ls .venv/bin/python 2>/dev/null || make install   # create the venv if missing

# Create a feature branch — do NOT commit directly to main
git checkout -b feat/monitoring-control-package
```

---

### Process (follow exactly — read `docs/processes/defining-document-templates.md` for full detail)

**Step 1 — Research**
- Fetch the PRINCE2 URL for the document. Read the actual sections listed on the page — these define the fields your template must cover.
  - If your fetch tool returns empty content for a `prince2.wiki` page, fall back to `curl -s <url>` and strip HTML tags directly — the site is static and fetchable, the tool failure is silent, not a dead link.
- Note the ISO 21502:2020 equivalent section if discernible.
- Read `ontology/modules/document.ttl` to find the class and its existing `rdfs:seeAlso` annotations.

**Step 2 — Ontology gap check**
- Identify any fields from the standard that have no corresponding ontology property.
- If gaps exist, add properties to the relevant `ontology/modules/*.ttl` file.
- Run `python tools/validate/validate.py` — must pass before proceeding.

**Step 3 — Write the three template files**
- `entry.yaml`: id, title, phase (`monitoring-control`), phase_order, ontology_class URI, standard citations, prince2_equivalent (name + verified URL), dependencies, required_before, template/instructions/shacl_shape paths, `package: pkgs:MonitoringControlPackage`
- `instructions.yaml`: version, document id, gates array (one per standard field, ordered, each with: id, order, prompt, fills, maps_to, required, validation/guidance where appropriate), completion block
- `template.md`: YAML frontmatter, then Markdown sections matching the standard's structure, each with `<!-- maps to: property -->` inline comment and `{{field_id}}` placeholder matching the gate id. Footer cites ISO 21502:2020 and PRINCE2 with the verified URL.

**Step 4 — Write the SHACL shape**
- Copy the primer comment block from `shapes/initiation/project-proposal.shacl.ttl`
- Minimum constraints on every shape: `dct:title`, `dct:description`, `pm:describesProject` (range `pm:Project`), `pm:producedInPhase` (hasValue `phases:MonitoringControl`), `dct:created`, `dct:creator`
- Add document-specific constraints for fields the standard marks mandatory

**Step 5 — Verify**
```bash
# Ontology valid
python tools/validate/validate.py

# Template files exist and are non-empty
ls -la templates/monitoring-control/*/

# PRINCE2 URL returns 200 (do this for each document's URL)
curl -o /dev/null -s -w "%{http_code}" <prince2_url>
```
All checks must pass before committing.

**Step 6 — Commit, push, open PR, and close issues**

Commit order per document:
1. Ontology changes (if any): `chore: add pm:{Property} to {module}.ttl`
2. Template + shape: `feat: add {Document Name} template pack (Monitoring & Control phase)`

Once all five documents are committed, push the branch and open a PR:

```bash
git push -u origin feat/monitoring-control-package

gh pr create \
  --title "feat: add Monitoring & Control Package template packs (Issues #25–#29)" \
  --body "## Monitoring & Control Package

Adds 20 files across 5 Monitoring & Control phase document packs plus 5 SHACL NodeShapes — completing Milestone #4.

### Documents
| Issue | Document | Ontology class | PRINCE2 equivalent |
| ----- | -------- | -------------- | ------------------ |
| #25 | Status Report | \`pm:StatusReport\` | Highlight Report |
| #26 | Risk Register | \`pm:RiskRegister\` | Risk Register |
| #27 | Issue Log | \`pm:IssueLog\` | Issue Register |
| #28 | Decision Log | \`pm:DecisionLog\` | Daily Log |
| #29 | Change Log | \`pm:ChangeLog\` | Issue Management Approach |

### Checklist
- [ ] \`python tools/validate/validate.py\` passes
- [ ] All 5 SHACL shapes parse (rdflib triple count check)
- [ ] All PRINCE2 URLs return 200
- [ ] Issues #25–#29 closed

Closes #25
Closes #26
Closes #27
Closes #28
Closes #29" \
  --milestone "Monitoring & Control Package"
```

> **Reviewers:** Request at least 2 reviewers. Do not approve or merge the PR yourself — that is the human's job.

After the PR is open, close each issue with a completion comment:
```
## Completed

Template pack built at `templates/monitoring-control/{name}/`.
SHACL shape at `shapes/monitoring-control/{name}.shacl.ttl`.

### Sources used
- PRINCE2: [{product name}]({verified URL})
- ISO 21502:2020: https://www.iso.org/standard/74947.html

### Ontology changes
- {property added, or "none"}

### Gaps deferred
- {anything not in scope, or "none"}
```

---

### Key facts about the ontology

- Namespace: `https://stephen-mcelhose.github.io/project-management-ontology/`
- Prefix in files: `@prefix : <https://stephen-mcelhose.github.io/project-management-ontology/> .`
- All 27 document classes are in `ontology/modules/document.ttl` as `foaf:Document` subclasses
- Phase individuals live at `phases:MonitoringControl` (prefix `phases:`)
- Package for all five of these: `pkgs:MonitoringControlPackage`
- `pm:describesProject` (domain: `foaf:Document`, range: `pm:Project`) — links a document instance to its project
- `pm:producedInPhase` (domain: `foaf:Document`, range: `pm:PhaseType`) — links to the phase individual
- `pm:documentStatus`, `pm:approvedBy` exist on `foaf:Document` — use where relevant
- Python venv at `.venv/` — activate with `.venv/bin/python` or `source .venv/bin/activate`

---

### Constraints
- Every `dependencies` / `required_before` entry in `entry.yaml` must be verified against the actual `:hasHardDependency` triples in `ontology/modules/document.ttl` — do not infer the dependency chain from the issue table alone, they can differ.
- Section names and order in `template.md` must come from the actual PRINCE2 page — not guessed
- Every `maps_to` in `instructions.yaml` must reference a real property in the ontology — fix the ontology first if needed
- Do not close an issue if `python tools/validate/validate.py` fails or the PRINCE2 URL returns anything other than 200
- Do not add properties to the ontology without running `python tools/validate/validate.py` after
