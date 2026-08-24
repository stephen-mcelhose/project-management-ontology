---
type: runbook
title: Planning Package Agent Prompt
description: Agent instructions for building the Planning Package template packs (Issues #13–#20).
timestamp: 2026-08-23T00:00:00Z
tags: [prompt, agent, planning]
---

## Task: Build Planning Package template packs — Issues #13–#20

**Repo:** `/Users/stephen.mcelhose.ext/repos/process-assistant`
**GitHub:** `stephen-mcelhose/process-assistant`

---

### Prerequisite

The Initiation Package (Milestone #1) is recommended but not strictly required. Templates are independent files — the only risk of parallel execution is ontology merge conflicts if multiple agents edit document.ttl simultaneously.

---

### Context

This repo contains a project management ontology (OWL/Turtle) and a growing library of document templates. Each PM document class has a corresponding template pack: three files plus a SHACL validation shape. One completed pack serves as the reference example:

```
domains/pm/templates/initiation/project-proposal/
  entry.yaml          ← metadata, standard citations, dependency chain, package
  instructions.yaml   ← agent gates (one per standard field, ordered, with maps_to)
  template.md         ← Markdown scaffold with {{placeholders}} and <!-- maps to --> comments
domains/pm/shapes/initiation/project-proposal.shacl.ttl
```

Read all four of these files before writing anything. They define the exact format expected.

---

### Your job

Build template packs for all eight Planning Package issues. **Parallelize research (Step 1) across all documents** — fetching PRINCE2 URLs and reading `document.ttl` has no shared state. **Do ontology gap-checking (Step 2) as a single consolidated pass** across every document in this batch before writing any template — documents in the same package frequently need the same or overlapping ontology properties (e.g. shared fields on `pm:Project`), and editing `domains/pm/ontology/modules/*.ttl` concurrently from multiple agents/sessions risks conflicting or duplicate properties. Once the ontology is settled and validated, templates and shapes (Steps 3–4) can again be written in parallel per document:

| Issue | Document | Ontology class | PRINCE2 source |
| ----- | -------- | -------------- | -------------- |
| [#13](https://github.com/stephen-mcelhose/process-assistant/issues/13) | Project Management Plan | `pm:ProjectManagementPlan` | https://prince2.wiki/management-products/baselines/project-initiation-documentation/ |
| [#14](https://github.com/stephen-mcelhose/process-assistant/issues/14) | Work Breakdown Structure | `pm:WorkBreakdownStructure` | https://prince2.wiki/management-products/baselines/plan/ |
| [#15](https://github.com/stephen-mcelhose/process-assistant/issues/15) | Project Schedule | `pm:ProjectSchedule` | https://prince2.wiki/management-products/baselines/plan/ |
| [#16](https://github.com/stephen-mcelhose/process-assistant/issues/16) | Resource Plan | `pm:ResourcePlan` | https://prince2.wiki/management-products/baselines/plan/ |
| [#17](https://github.com/stephen-mcelhose/process-assistant/issues/17) | Cost Estimate | `pm:CostEstimate` | https://prince2.wiki/management-products/baselines/business-case/ |
| [#18](https://github.com/stephen-mcelhose/process-assistant/issues/18) | Risk Management Plan | `pm:RiskManagementPlan` | https://prince2.wiki/management-products/baselines/management-approaches/risk/ |
| [#19](https://github.com/stephen-mcelhose/process-assistant/issues/19) | Quality Management Plan | `pm:QualityManagementPlan` | https://prince2.wiki/management-products/baselines/management-approaches/quality/ |
| [#20](https://github.com/stephen-mcelhose/process-assistant/issues/20) | Communication Plan | `pm:CommunicationPlan` | https://prince2.wiki/management-products/baselines/management-approaches/communication/ |

> **Note:** Issues #14, #15, and #16 all cite the PRINCE2 Plan product — read the same page once, then use the relevant section (product breakdown / schedule / resource) for each document.

Output paths follow this pattern:
```
domains/pm/templates/planning/{kebab-name}/entry.yaml
domains/pm/templates/planning/{kebab-name}/instructions.yaml
domains/pm/templates/planning/{kebab-name}/template.md
domains/pm/shapes/planning/{kebab-name}.shacl.ttl
```

---

### Step 0 — Environment setup (do this first)

```bash
git fetch origin
git rebase origin/main          # your worktree may predate later domains/pm/ontology/prompt commits
ls .venv/bin/python 2>/dev/null || make install   # create the venv if missing
```

---

### Process (follow exactly — read `docs/processes/defining-document-templates.md` for full detail)

**Step 1 — Research**
- Fetch the PRINCE2 URL for the document. Read the actual sections listed on the page — these define the fields your template must cover.
  - If your fetch tool returns empty content for a `prince2.wiki` page, fall back to `curl -s <url>` and strip HTML tags directly — the site is static and fetchable, the tool failure is silent, not a dead link.
- Note the ISO 21502:2020 equivalent section if discernible.
- Read `domains/pm/ontology/modules/document.ttl` to find the class and its existing `rdfs:seeAlso` annotations.

**Step 2 — Ontology gap check**
- Identify any fields from the standard that have no corresponding ontology property.
- If gaps exist, add properties to the relevant `domains/pm/ontology/modules/*.ttl` file.
- Run `python tools/validate/validate.py` — must pass before proceeding.

**Step 3 — Write the three template files**
- `entry.yaml`: id, title, phase (`planning`), phase_order, ontology_class URI, standard citations, prince2_equivalent (name + verified URL), dependencies, required_before, template/instructions/shacl_shape paths, `package: pkgs:PlanningPackage`
- `instructions.yaml`: version, document id, gates array (one per standard field, ordered, each with: id, order, prompt, fills, maps_to, required, validation/guidance where appropriate), completion block
- `template.md`: YAML frontmatter, then Markdown sections matching the standard's structure, each with `<!-- maps to: property -->` inline comment and `{{field_id}}` placeholder matching the gate id. Footer cites ISO 21502:2020 and PRINCE2 with the verified URL.

**Step 4 — Write the SHACL shape**
- Copy the primer comment block from `domains/pm/shapes/initiation/project-proposal.shacl.ttl`
- Minimum constraints on every shape: `dct:title`, `dct:description`, `pm:describesProject` (range `pm:Project`), `pm:producedInPhase` (hasValue `phases:Planning`), `dct:created`, `dct:creator`
- Add document-specific constraints for fields the standard marks mandatory

**Step 5 — Verify**
```bash
# Ontology valid
python tools/validate/validate.py

# Template files exist and are non-empty
ls -la domains/pm/templates/planning/*/

# PRINCE2 URL returns 200 (do this for each document's URL)
curl -o /dev/null -s -w "%{http_code}" <prince2_url>
```
All checks must pass before committing.

**Step 6 — Commit and close**

Commit order per document:
1. Ontology changes (if any): `chore: add pm:{Property} to {module}.ttl`
2. Template + shape: `feat: add {Document Name} template pack (Planning phase)`

Close each issue with a completion comment:
```
## Completed

Template pack built at `domains/pm/templates/planning/{name}/`.
SHACL shape at `domains/pm/shapes/planning/{name}.shacl.ttl`.

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

- Namespace: `https://stephen-mcelhose.github.io/process-assistant/pm/`
- Prefix in files: `@prefix : <https://stephen-mcelhose.github.io/process-assistant/pm/> .`
- All 27 document classes are in `domains/pm/ontology/modules/document.ttl` as `foaf:Document` subclasses
- Phase individuals live at `phases:Planning` (prefix `phases:`)
- Package for all eight of these: `pkgs:PlanningPackage`
- `pm:describesProject` (domain: `foaf:Document`, range: `pm:Project`) — links a document instance to its project
- `pm:producedInPhase` (domain: `foaf:Document`, range: `pm:PhaseType`) — links to the phase individual
- `pm:documentStatus`, `pm:approvedBy` exist on `foaf:Document` — use where relevant
- Python venv at `.venv/` — activate with `.venv/bin/python` or `source .venv/bin/activate`

---

### Constraints
- Every `dependencies` / `required_before` entry in `entry.yaml` must be verified against the actual `:hasHardDependency` triples in `domains/pm/ontology/modules/document.ttl` — do not infer the dependency chain from the issue table alone, they can differ.
- Section names and order in `template.md` must come from the actual PRINCE2 page — not guessed
- Every `maps_to` in `instructions.yaml` must reference a real property in the ontology — fix the ontology first if needed
- Do not close an issue if `python tools/validate/validate.py` fails or the PRINCE2 URL returns anything other than 200
- Do not add properties to the ontology without running `python tools/validate/validate.py` after
