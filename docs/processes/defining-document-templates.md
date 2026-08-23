---
type: process
title: Defining Document Templates
description: >
  How to research, build, and validate a document template + ruleset for a PM
  document class. Follow this process every time you fill a GitHub issue that
  defines a template.
tags: [process, templates, ontology, shacl]
timestamp: 2026-08-22T00:00:00Z
---

# Process: Defining Document Templates

Follow this process **every time** you work on a GitHub issue that defines a
document template and ruleset. The goal is: every template is grounded in a
cited standard, every ontology gap found during research is fixed before the
template is written, and every URL is verified before it is committed.

---

## Working on a batch of issues (a package milestone)

When a prompt asks you to build several document packs at once (e.g. all
Issues in a Package milestone), parallelize by step, not by document:

- **Step 1 (Research) parallelizes cleanly.** Fetching PRINCE2 URLs and
  reading `document.ttl` per document has no shared state.
- **Step 2 (Ontology gap check) must be a single consolidated pass across
  the whole batch**, done before any template is written. Documents in the
  same package frequently need the same or overlapping properties (e.g.
  several documents adding fields to `pm:Project`). Running Step 2
  concurrently per-document — whether as separate agent sessions or just
  interleaved edits — risks duplicate or conflicting properties and
  `ontology/modules/*.ttl` merge conflicts.
- **Steps 3–4 (template + shape) parallelize again once the ontology is
  settled and `python tools/validate/validate.py` passes.**

## Environment setup (do this before Step 1)

```bash
git fetch origin
git rebase origin/main          # worktrees can predate later ontology/prompt commits
ls .venv/bin/python 2>/dev/null || make install   # create the venv if missing
```

---

## Overview

```
Issue filed
    │
    ▼
1. Research — fetch the real standard pages, read the actual sections
    │
    ▼
2. Ontology gap check — does the ontology need new properties or classes?
    │  yes → fix ontology first, validate, commit
    │  no  → continue
    ▼
3. Build the template pack
      templates/{phase}/{document-name}/
        entry.yaml          ← metadata + citations
        instructions.yaml   ← agent gates (how to fill)
        template.md         ← markdown scaffold
      templates/{phase}/_manifest.yaml   ← create or update
    │
    ▼
4. Write the SHACL shape
      shapes/{phase}/{document-name}.shacl.ttl
    │
    ▼
5. Verify — validate TTL, check all URLs return 200
    │
    ▼
6. Update the issue + commit
```

---

## Step 1 — Research

Before writing a single line of template, read the real sources.

### 1a. Identify the ontology class

Look up the document class in `ontology/modules/document.ttl`. Note:
- `pm:producedInPhase` — which phase it belongs to
- `pm:hasHardDependency` — what must exist before this document
- `dct:source` — which standard is cited
- `rdfs:seeAlso` — the PRINCE2 management product URL

### 1b. Fetch the PRINCE2 management product page

Use the verified URL from `rdfs:seeAlso`. Read **all** sections defined on the
page: purpose, composition, quality criteria, derivation, format.

```
# example
curl -s https://prince2.wiki/management-products/baselines/project-initiation-documentation/ | ...
# or use WebFetch
```

> **Lesson learned:** URL-fetch tools can silently return empty content for
> `prince2.wiki` pages instead of erroring. If that happens, don't assume the
> link is dead — the site is verified 200 and served as static HTML. Fall back
> to `curl -s <url>` and strip tags (e.g. regex on `<h1>`/`<h2>`/`<li>`) to
> recover the real section structure before concluding a URL needs fixing.

Also note in `1a`: cross-check every dependency you plan to write into
`entry.yaml` (`dependencies:` / `required_before:`) against the actual
`:hasHardDependency` triples in `document.ttl`. Don't infer the chain from an
issue table or from what "feels" like the right order — the ontology is the
source of truth and can differ (e.g. a downstream document's real hard
dependency may skip one you'd otherwise assume).

Write down every field the standard names. Do not invent fields.

### 1c. Check the ISO 21502 citation (optional but preferred)

ISO 21502:2020 is paywalled, but the `dct:source` URI records the citation.
If an open summary or commentary exists, cross-reference the PRINCE2 sections
against ISO 21502 terminology. Note any terminology differences in
`skos:scopeNote` on the ontology class.

### 1d. Verify all URLs return 200

**Every** `rdfs:seeAlso` URL in `document.ttl` must be a live 200. Run:

```bash
curl -o /dev/null -s -w "%{http_code}  %{url_effective}\n" \
  -L "<url-from-rdfs:seeAlso>"
```

If a URL returns 301, follow the redirect and update the ontology with the
final URL. If it returns 404, find the correct URL before proceeding.
Do not commit dead links.

> **Lesson learned (2026-08-23):** `prince2.wiki` restructured its URLs from
> flat `/{slug}/` to nested paths. The old flat URLs mostly 404. Always verify
> before trusting a URL sourced from an AI model or index page.

---

## Step 2 — Ontology gap check

After reading the standard, ask: *does the ontology have properties to
represent every required field?*

Common gaps to look for:

| Field type | Expected property |
| ---------- | ----------------- |
| Document title | `dct:title` |
| Document description / purpose | `dct:description` |
| Document links to a project | `pm:describesProject` ← **not yet defined** |
| Author / creator | `dct:creator` |
| Creation date | `dct:created` |
| Named sponsor | `pm:hasSponsor` (on `pm:Project`) |
| Budget | `pm:budget` (on `pm:Project`) |
| Dates | `pm:plannedStartDate`, `pm:plannedEndDate` |
| Risk | `pm:Risk`, `pm:likelihood`, `pm:impact` |
| Role assignment | `pm:RoleAssignment`, `pm:assignedAgent`, `pm:assignedRole` |

### If a gap exists

1. Add the missing class or property to the relevant `ontology/modules/*.ttl`
2. Add `rdfs:label`, `rdfs:comment`, domain, range
3. Add `rdfs:isDefinedBy :`
4. Run `make validate` — must pass before continuing
5. Commit the ontology change **separately** from the template
   (`chore: add pm:describesProject property`)

Do not write templates that reference properties that do not exist in the
ontology.

---

## Step 3 — Build the template pack

Create the folder: `templates/{phase}/{document-name}/`

Phase folder names match the DIN 69901 phase identifiers:

| Phase | Folder |
| ----- | ------ |
| Initiation | `templates/initiation/` |
| Planning | `templates/planning/` |
| Execution | `templates/execution/` |
| Monitoring & Control | `templates/monitoring-control/` |
| Closure | `templates/closure/` |

### 3a. `entry.yaml`

```yaml
id: {document-name}            # kebab-case
title: {Human Readable Title}
phase: {phase}
phase_order: {N}               # position within the phase

ontology_class: https://stephen-mcelhose.github.io/project-management-ontology/{ClassName}

standard:
  name: ISO 21502:2020 — Guidance on project management
  url: https://www.iso.org/standard/74947.html
din_69901:
  phase: {Phase}
  part: DIN 69901-2:2009
  url: https://www.beuth.de/en/standard/din-69901-2/119948897
prince2_equivalent:
  name: {PRINCE2 management product name}
  url: {verified 200 URL from prince2.wiki/management-products/...}

dependencies:                  # pm:hasHardDependency predecessors
  - {document-name}
required_before:               # documents that depend on this one
  - {document-name}

template: template.md
instructions: instructions.yaml
shacl_shape: ../../../shapes/{phase}/{document-name}.shacl.ttl
```

### 3b. `instructions.yaml`

One gate per required or important field, in fill order. Each gate:

```yaml
- id: {field_id}
  order: {N}
  type: {gate-output-type}        # see type vocabulary below
  prompt: "The question the agent asks the user."
  fills: "## Section Heading in template.md"
  maps_to: {ontology:property}   # e.g. dct:title, pm:hasSponsor
  required: true | false
  deferred_value: "..."           # required when required: false — see below
  validation: "Rule the agent checks before accepting the answer."
  validation_rules:               # optional — see below
    {key}: {value}
  guidance: "Optional: extra instruction to the agent, not shown to the user."
```

#### Gate output type vocabulary (ADR-004)

The `type:` field declares the rendering shape of the gate's output. Valid
values are defined as `pm:GateOutputType` named individuals in
`ontology/modules/document.ttl`.

| `type:`      | Category | Description                                                        |
|--------------|----------|--------------------------------------------------------------------|
| `string`     | Scalar   | Free-form inline text filling a `{{placeholder}}` token            |
| `date`       | Scalar   | ISO 8601 calendar date (YYYY-MM-DD)                               |
| `identifier` | Scalar   | Unique code with a naming convention (e.g. CR-001)                |
| `prose`      | Block    | Narrative paragraph(s), no required internal structure             |
| `list`       | Block    | Ordered or unordered enumeration of discrete items                 |
| `table`      | Block    | Markdown table with defined column headers                         |
| `section`    | Section  | Prose with its own internal sub-structure (headings, nested blocks)|

**Choosing the right type:**
- If `fills:` contains a `{{placeholder}}` token → scalar (`string`, `date`,
  or `identifier`)
- If `fills:` names a `## Section` and the agent writes paragraphs → `prose`
- If the section is a list or table → `list` or `table`
- If the section needs its own internal headings or multiple nested blocks
  → `section`

`type:` is optional but all gates should be annotated before M5. To add a
new type, follow the amendment process in ADR-004.

#### Deferred value convention (issue #45)

Every gate with `required: false` **must** carry a `deferred_value:` field.
This is the literal text the agent writes into the template when the user
cannot or chooses not to answer the gate. It prevents raw `{{placeholder}}`
strings from appearing in output documents.

Choose the value that makes most sense in context:

| Situation                                   | Use                                               |
|---------------------------------------------|---------------------------------------------------|
| General optional content not yet available  | `"*Deferred — to be confirmed before phase completion.*"` |
| A date slot where the date is not yet set   | `"*To be confirmed.*"`                            |
| An assignee/owner slot with no one assigned | `"*Unassigned.*"`                                 |
| A numeric or calculated field               | `"*Not yet estimated.*"` / `"*Not yet calculated.*"` |
| An outcome that has not yet been decided    | `"*Pending.*"`                                    |
| An assessment field not yet performed       | `"*Not yet assessed.*"`                           |

Rules:
- `deferred_value:` is mandatory for every `required: false` gate
- The value is italic Markdown (`*...*`) to visually distinguish deferred
  content from real content in rendered output
- Never leave a deferred section empty or with a raw `{{placeholder}}` — the
  deferred value exists precisely to prevent this

#### Structured validation rules (ADR-005)

When a `validation:` prose field expresses a constraint that is
programmatically checkable, add a `validation_rules:` block alongside it.
The prose is always preserved — `validation_rules:` is additive.

Valid keys (full specification in ADR-005):

| Key | Value | Use when |
|-----|-------|----------|
| `unique: true` | boolean | Identifier must never be reused in the same register |
| `allowed_values: [...]` | list of strings | Value must be one of a fixed set of options |
| `min_items: N` | integer | Output must contain at least N enumerable items |
| `named_individual: true` | boolean | Value must be a specific named person, not a role or team |
| `required_parts: [...]` | list of strings | Structured output must address each named part |
| `format: currency` | literal | Value must be a number with a currency symbol (e.g. `€120,000`) |
| `references_document: <id>` | kebab-case doc ID | Content must reference the named sibling document |

Rules:
- Only add `validation_rules:` when at least one constraint can be expressed
  with the above keys — qualitative rules ("must be concise") stay prose-only
- Multiple keys are allowed on one gate
- `validation:` prose must always accompany `validation_rules:`
- Keys outside the vocabulary are rejected by `instructions-schema.json` (#47)

To propose a new key, follow the amendment process in ADR-005.

Rules for gates:
- All fields sourced from the standard (Step 1b) must have a gate
- Required gates are those the standard marks as mandatory or quality criteria
- `maps_to` must reference a real property in the ontology (Step 2)
- End the file with a `completion:` block naming required gates and the
  `next_document` in the dependency chain

After writing the file, confirm it is schema-valid: `make validate-schemas`
(enforced by `tools/schemas/instructions-schema.json`).

### 3c. `template.md`

```markdown
---
type: template
document_class: pm:{ClassName}
phase: {phase}
standard: ISO 21502:2020
prince2_equivalent: {Name}
ontology_uri: https://stephen-mcelhose.github.io/project-management-ontology/{ClassName}
status: draft
---

# {Document Title}: {{project_name}}

> Purpose, phase, and what must be completed before this.

## {Section from standard}
<!-- maps to: {ontology:property} -->
{{placeholder}}
```

Rules for the scaffold:
- Section names and order come from the standard (Step 1b), not intuition
- Every section has an inline `<!-- maps to: ... -->` comment citing the
  ontology property
- Placeholders use `{{field_id}}` matching gate `id` values in `instructions.yaml`
- Footer cites the standard and PRINCE2 equivalent with the verified URL

---

## Step 3d — Update the phase manifest

Every phase has a `_manifest.yaml` at `templates/{phase}/_manifest.yaml`
(see ADR-003). Update it to include this document:

- **If this is the first document in a new phase:** create the manifest from
  the template in ADR-003. Set `phase_local_order: 1`.
- **If adding to an existing phase:** add the document in the correct position,
  incrementing `phase_local_order`. Update `dependencies` and `required_before`
  on any documents whose chain this document joins.
- If this document introduces a new shared context field (a field that should
  not be re-asked across subsequent documents), add it to `shared_context`.
- Commit the manifest update in the **same commit** as the template pack (Step 6).

---

## Step 4 — Write the SHACL shape

Create `shapes/{phase}/{document-name}.shacl.ttl`.

Minimum required constraints for every document shape:

```turtle
pm-sh:{ClassName}Shape
    a sh:NodeShape ;
    sh:targetClass pm:{ClassName} ;

    # title
    sh:property [ sh:path dct:title ; sh:minCount 1 ; sh:datatype xsd:string ;
                  sh:message "Must have dct:title."@en ] ;

    # description
    sh:property [ sh:path dct:description ; sh:minCount 1 ;
                  sh:message "Must have dct:description."@en ] ;

    # links to the project it describes
    sh:property [ sh:path pm:describesProject ; sh:minCount 1 ;
                  sh:class pm:Project ;
                  sh:message "Must reference the project via pm:describesProject."@en ] ;

    # phase
    sh:property [ sh:path pm:producedInPhase ; sh:minCount 1 ;
                  sh:hasValue phases:{Phase} ;
                  sh:message "Must be linked to the {Phase} phase."@en ] ;

    # provenance
    sh:property [ sh:path dct:created ; sh:minCount 1 ; sh:datatype xsd:date ;
                  sh:message "Must record dct:created."@en ] ;
    sh:property [ sh:path dct:creator ; sh:minCount 1 ;
                  sh:message "Must identify dct:creator."@en ] .
```

Add document-specific constraints for every field that the standard marks
as required or quality criteria.

Add the SHACL primer comment block at the top of every shape file (copy from
`shapes/initiation/project-proposal.shacl.ttl`).

---

## Step 5 — Verify

```bash
# 1. Ontology syntax + semantics
make validate

# 2. All rdfs:seeAlso URLs in document.ttl return 200
python3 - << 'EOF'
from rdflib import Graph, RDFS, URIRef
import subprocess, sys
g = Graph()
g.parse("ontology/modules/document.ttl", format="turtle")
urls = [str(o) for s, p, o in g if str(p) == str(RDFS.seeAlso)]
for url in sorted(set(urls)):
    r = subprocess.run(["curl","-o","/dev/null","-s","-w","%{http_code}",url],
                       capture_output=True, text=True)
    status = r.stdout.strip()
    mark = "✓" if status == "200" else "✗"
    print(f"  {mark} {status}  {url}")
EOF

# 3. Template files exist and are non-empty
ls -la templates/{phase}/{document-name}/

# 4. instructions.yaml validates against the gate schema
make validate-schemas
```

All four checks must pass before committing.

---

## Step 6 — Update the issue and commit

### Update the GitHub issue

Replace the issue body with a completion record:

```markdown
## Completed

Template pack built at `templates/{phase}/{document-name}/`.
SHACL shape at `shapes/{phase}/{document-name}.shacl.ttl`.

### Sources used
- PRINCE2: [{product name}]({verified URL})
- ISO 21502:2020: https://www.iso.org/standard/74947.html

### Ontology changes
- {property added, or "none"}

### Gaps deferred
- {anything not in scope, or "none"}
```

### Commit order

1. Ontology changes (if any): `chore: add pm:{Property} to {module}.ttl`
2. Template + SHACL: `feat: add {document name} template pack ({phase} phase)`

Commit messages must name the document class and phase.

---

## Checklist

Copy into the GitHub issue before starting:

```
- [ ] 1a. Ontology class located in document.ttl
- [ ] 1b. PRINCE2 page fetched and sections documented
- [ ] 1c. ISO 21502 cross-reference noted (if accessible)
- [ ] 1d. All rdfs:seeAlso URLs verified 200
- [ ] 2.  Ontology gaps identified and fixed (or none found)
- [ ] 2.  make validate passes after ontology changes
- [ ] 3a. entry.yaml written
- [ ] 3b. instructions.yaml written (one gate per standard field)
- [ ] 3c. template.md written (sections sourced from standard)
- [ ] 3d. _manifest.yaml created or updated for the phase
- [ ] 4.  SHACL shape written
- [ ] 5.  make validate passes
- [ ] 5.  All rdfs:seeAlso URLs return 200
- [ ] 5.  Template files non-empty
- [ ] 5.  make validate-schemas passes
- [ ] 6.  Issue updated with completion record
- [ ] 6.  Committed in correct order
```
