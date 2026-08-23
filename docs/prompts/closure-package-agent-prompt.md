---
type: runbook
title: Closure Package Agent Prompt
description: Agent instructions for building the Closure Package template packs (Issues #30–#34).
timestamp: 2026-08-23T00:00:00Z
tags: [prompt, agent, closure]
---

## Task: Build Closure Package template packs — Issues #30–#34

**Repo:** `/Users/stephen.mcelhose.ext/repos/process-assistant`
**GitHub:** `stephen-mcelhose/process-assistant`

---

### Prerequisite

The Execution Package (Milestone #3) is recommended but not strictly required. Templates are independent files — the only risk of parallel execution is ontology merge conflicts if multiple agents edit document.ttl simultaneously.
Closure documents synthesise the full project record — templates must reference prior phase documents correctly.

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

Build template packs for all five Closure Package issues. **Parallelize research (Step 1) across all documents** — fetching PRINCE2 URLs and reading `document.ttl` has no shared state. **Do ontology gap-checking (Step 2) as a single consolidated pass** across every document in this batch before writing any template — documents in the same package frequently need the same or overlapping ontology properties (e.g. shared fields on `pm:Project`), and editing `ontology/modules/*.ttl` concurrently from multiple agents/sessions risks conflicting or duplicate properties. Once the ontology is settled and validated, templates and shapes (Steps 3–4) can again be written in parallel per document:

| Issue | Document | Ontology class | PRINCE2 source |
| ----- | -------- | -------------- | -------------- |
| [#30](https://github.com/stephen-mcelhose/process-assistant/issues/30) | Handover Document | `pm:HandoverDocument` | https://prince2.wiki/management-products/reports/end-project-report/ |
| [#31](https://github.com/stephen-mcelhose/process-assistant/issues/31) | Final Project Report | `pm:FinalProjectReport` | https://prince2.wiki/management-products/reports/end-project-report/ |
| [#32](https://github.com/stephen-mcelhose/process-assistant/issues/32) | Lessons Learned Report | `pm:LessonsLearnedReport` | https://prince2.wiki/management-products/reports/lessons-report/ |
| [#33](https://github.com/stephen-mcelhose/process-assistant/issues/33) | Archive Index | `pm:ArchiveIndex` | https://prince2.wiki/management-products/project-log/product-register/ |
| [#34](https://github.com/stephen-mcelhose/process-assistant/issues/34) | Project Closure Statement | `pm:ProjectClosureStatement` | https://prince2.wiki/management-products/reports/end-project-report/ |

> **Note:** Issues #30, #31, and #34 all cite the PRINCE2 End Project Report — read the page once, then use the relevant section for each document (handover evidence, performance summary, formal closure statement). They are distinct documents despite sharing a source.

Output paths follow this pattern:
```
templates/closure/{kebab-name}/entry.yaml
templates/closure/{kebab-name}/instructions.yaml
templates/closure/{kebab-name}/template.md
shapes/closure/{kebab-name}.shacl.ttl
```

---

### Step 0 — Environment setup (do this first)

```bash
git fetch origin
git rebase origin/main          # your worktree may predate later ontology/prompt commits
ls .venv/bin/python 2>/dev/null || make install   # create the venv if missing
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
- `entry.yaml`: id, title, phase (`closure`), phase_order, ontology_class URI, standard citations, prince2_equivalent (name + verified URL), dependencies, required_before, template/instructions/shacl_shape paths, `package: pkgs:ClosurePackage`
- `instructions.yaml`: version, document id, gates array (one per standard field, ordered, each with: id, order, prompt, fills, maps_to, required, validation/guidance where appropriate), completion block
- `template.md`: YAML frontmatter, then Markdown sections matching the standard's structure, each with `<!-- maps to: property -->` inline comment and `{{field_id}}` placeholder matching the gate id. Footer cites ISO 21502:2020 and PRINCE2 with the verified URL.

**Step 4 — Write the SHACL shape**
- Copy the primer comment block from `shapes/initiation/project-proposal.shacl.ttl`
- Minimum constraints on every shape: `dct:title`, `dct:description`, `pm:describesProject` (range `pm:Project`), `pm:producedInPhase` (hasValue `phases:Closure`), `dct:created`, `dct:creator`
- Add document-specific constraints for fields the standard marks mandatory

**Step 5 — Verify**
```bash
# Ontology valid
python tools/validate/validate.py

# Template files exist and are non-empty
ls -la templates/closure/*/

# PRINCE2 URL returns 200 (do this for each document's URL)
curl -o /dev/null -s -w "%{http_code}" <prince2_url>
```
All checks must pass before committing.

**Step 6 — Commit and close**

Commit order per document:
1. Ontology changes (if any): `chore: add pm:{Property} to {module}.ttl`
2. Template + shape: `feat: add {Document Name} template pack (Closure phase)`

Close each issue with a completion comment:
```
## Completed

Template pack built at `templates/closure/{name}/`.
SHACL shape at `shapes/closure/{name}.shacl.ttl`.

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
- Phase individuals live at `phases:Closure` (prefix `phases:`)
- Package for all five of these: `pkgs:ClosurePackage`
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
