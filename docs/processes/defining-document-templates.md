---
type: process
title: Defining Document Templates
description: >
  How to research, build, and validate a document template + ruleset for a PM
  document class. Follow this process every time you fill a GitHub issue that
  defines a template.
tags: [process, templates, ontology, shacl]
updated: 2026-08-23
---

# Process: Defining Document Templates

Follow this process **every time** you work on a GitHub issue that defines a
document template and ruleset. The goal is: every template is grounded in a
cited standard, every ontology gap found during research is fixed before the
template is written, and every URL is verified before it is committed.

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
  prompt: "The question the agent asks the user."
  fills: "## Section Heading in template.md"
  maps_to: {ontology:property}   # e.g. dct:title, pm:hasSponsor
  required: true | false
  validation: "Rule the agent checks before accepting the answer."
  guidance: "Optional: extra instruction to the agent, not shown to the user."
```

Rules for gates:
- All fields sourced from the standard (Step 1b) must have a gate
- Required gates are those the standard marks as mandatory or quality criteria
- `maps_to` must reference a real property in the ontology (Step 2)
- End the file with a `completion:` block naming required gates and the
  `next_document` in the dependency chain

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
```

All three checks must pass before committing.

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
- [ ] 4.  SHACL shape written
- [ ] 5.  make validate passes
- [ ] 5.  All rdfs:seeAlso URLs return 200
- [ ] 5.  Template files non-empty
- [ ] 6.  Issue updated with completion record
- [ ] 6.  Committed in correct order
```
