## Task: Build Execution Package template packs — Issues #21–#24

**Repo:** `/Users/stephen.mcelhose.ext/repos/project-management-ontology`
**GitHub:** `stephen-mcelhose/project-management-ontology`

---

### Prerequisite

The Planning Package (Milestone #2) is recommended but not strictly required. Templates are independent files — the only risk of parallel execution is ontology merge conflicts if multiple agents edit document.ttl simultaneously.

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

Build template packs for all four Execution Package issues, **in parallel**:

| Issue | Document | Ontology class | PRINCE2 source |
| ----- | -------- | -------------- | -------------- |
| [#21](https://github.com/stephen-mcelhose/project-management-ontology/issues/21) | Work Package Description | `pm:WorkPackageDescription` | https://prince2.wiki/management-products/baselines/work-package/ |
| [#22](https://github.com/stephen-mcelhose/project-management-ontology/issues/22) | Deliverable Status Report | `pm:DeliverableStatusReport` | https://prince2.wiki/management-products/reports/checkpoint-report/ |
| [#23](https://github.com/stephen-mcelhose/project-management-ontology/issues/23) | Change Request | `pm:ChangeRequest` | https://prince2.wiki/management-products/reports/issue-report/ |
| [#24](https://github.com/stephen-mcelhose/project-management-ontology/issues/24) | Quality Audit Report | `pm:QualityAuditReport` | https://prince2.wiki/management-products/project-log/quality-register/ |

> **Note:** These are operational documents produced repeatedly during delivery — a Work Package Description may be issued many times; a Change Request is raised per change event. Templates should reflect this: section names and prompts should be written for individual instances, not as registers.

Output paths follow this pattern:
```
templates/execution/{kebab-name}/entry.yaml
templates/execution/{kebab-name}/instructions.yaml
templates/execution/{kebab-name}/template.md
shapes/execution/{kebab-name}.shacl.ttl
```

---

### Process (follow exactly — read `docs/processes/defining-document-templates.md` for full detail)

**Step 1 — Research**
- Fetch the PRINCE2 URL for the document. Read the actual sections listed on the page — these define the fields your template must cover.
- Note the ISO 21502:2020 equivalent section if discernible.
- Read `ontology/modules/document.ttl` to find the class and its existing `rdfs:seeAlso` annotations.

**Step 2 — Ontology gap check**
- Identify any fields from the standard that have no corresponding ontology property.
- If gaps exist, add properties to the relevant `ontology/modules/*.ttl` file.
- Run `python tools/validate/validate.py` — must pass before proceeding.

**Step 3 — Write the three template files**
- `entry.yaml`: id, title, phase (`execution`), phase_order, ontology_class URI, standard citations, prince2_equivalent (name + verified URL), dependencies, required_before, template/instructions/shacl_shape paths, `package: pkgs:ExecutionPackage`
- `instructions.yaml`: version, document id, gates array (one per standard field, ordered, each with: id, order, prompt, fills, maps_to, required, validation/guidance where appropriate), completion block
- `template.md`: YAML frontmatter, then Markdown sections matching the standard's structure, each with `<!-- maps to: property -->` inline comment and `{{field_id}}` placeholder matching the gate id. Footer cites ISO 21502:2020 and PRINCE2 with the verified URL.

**Step 4 — Write the SHACL shape**
- Copy the primer comment block from `shapes/initiation/project-proposal.shacl.ttl`
- Minimum constraints on every shape: `dct:title`, `dct:description`, `pm:describesProject` (range `pm:Project`), `pm:producedInPhase` (hasValue `phases:Execution`), `dct:created`, `dct:creator`
- Add document-specific constraints for fields the standard marks mandatory

**Step 5 — Verify**
```bash
# Ontology valid
python tools/validate/validate.py

# Template files exist and are non-empty
ls -la templates/execution/*/

# PRINCE2 URL returns 200 (do this for each document's URL)
curl -o /dev/null -s -w "%{http_code}" <prince2_url>
```
All checks must pass before committing.

**Step 6 — Commit and close**

Commit order per document:
1. Ontology changes (if any): `chore: add pm:{Property} to {module}.ttl`
2. Template + shape: `feat: add {Document Name} template pack (Execution phase)`

Close each issue with a completion comment:
```
## Completed

Template pack built at `templates/execution/{name}/`.
SHACL shape at `shapes/execution/{name}.shacl.ttl`.

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
- Phase individuals live at `phases:Execution` (prefix `phases:`)
- Package for all four of these: `pkgs:ExecutionPackage`
- `pm:describesProject` (domain: `foaf:Document`, range: `pm:Project`) — links a document instance to its project
- `pm:producedInPhase` (domain: `foaf:Document`, range: `pm:PhaseType`) — links to the phase individual
- `pm:documentStatus`, `pm:approvedBy` exist on `foaf:Document` — use where relevant
- Python venv at `.venv/` — activate with `.venv/bin/python` or `source .venv/bin/activate`

---

### Constraints
- Section names and order in `template.md` must come from the actual PRINCE2 page — not guessed
- Every `maps_to` in `instructions.yaml` must reference a real property in the ontology — fix the ontology first if needed
- Do not close an issue if `python tools/validate/validate.py` fails or the PRINCE2 URL returns anything other than 200
- Do not add properties to the ontology without running `python tools/validate/validate.py` after
