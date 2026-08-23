---
name: template-pack
description: >
  Author a gate-based document template pack from reference examples. Given one or more
  reference template pack directories and a document specification, produce a new pack
  (entry.yaml + instructions.yaml + template.md) whose field names, gate structure,
  placeholder syntax, and section layout exactly match the references. The skill is
  domain-agnostic — it reads all conventions from the workspace, never assumes them.
  Default output: templates/{namespace}/{slug}/ (namespace derived from the ontology class
  prefix, e.g. okf:POCStepEvidence → templates/okf/poc-step-evidence-01-discovery/).
  Trigger on: "/template-pack", "create a template pack for", "generate a template for",
  "add a template pack", "write a document template", "scaffold a gate template".
version: "1.0.0"
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
  - WebFetch
  - AskUserQuestion
---

# template-pack — Gate-Based Document Template Author

Produce a new template pack (three files: entry.yaml + instructions.yaml + template.md)
that exactly matches the conventions of the project's existing packs. Gates in
`instructions.yaml` and section headings in `template.md` must correspond exactly —
this is enforced before any file is written.

---

## Inputs

Gather these before starting. Ask with `AskUserQuestion` if missing.

| Input | Required | Description |
| ----- | -------- | ----------- |
| Reference pack paths | Yes (≥2) | Paths to existing pack directories, each containing entry.yaml + instructions.yaml + template.md. Fail loudly if fewer than two are provided. |
| Document slug | Yes | Kebab-case identifier (e.g. `poc-step-evidence-01-discovery`). Becomes the directory name and the `document:` key in instructions.yaml. |
| Document title | Yes | Human-readable name (e.g. `POC Step Evidence — 01 Discovery`). |
| Ontology class CURIE | Yes | Class identifier (e.g. `okf:POCStepEvidence`). The prefix drives the default output namespace. |
| Ontology class URI | Yes | Full IRI (e.g. `https://eis-intake-firehose/ontology/okf#POCStepEvidence`). Used in entry.yaml. |
| Ontology file path | Recommended | Path to the OWL/Turtle file so `maps_to` CURIEs can be verified. |
| Standard or source URL | Recommended | URL of the specification or process framework to derive gate prompts from. Fetched in Step 3. |
| Dependencies | Optional | Slugs of packs this one depends on (comma-separated). |
| Output directory | Optional | Explicit parent directory override. If omitted, defaults to `templates/{namespace}/` where `{namespace}` is the class prefix. |
| Phase or category | Recommended | Grouping label used in entry.yaml (e.g. `discovery`, `feasibility`). |

### Default output path derivation

Given class CURIE `okf:POCStepEvidence` and slug `poc-step-evidence-01-discovery`:
- Namespace: `okf`
- Default output directory: `templates/okf/`
- Default pack directory: `templates/okf/poc-step-evidence-01-discovery/`

If the output directory does not exist, create it. If an explicit output directory is given,
use it instead.

---

## Step 1 — Read reference packs

Read **all three files** in each reference pack directory. Fail with a clear error if fewer
than two pack directories are provided:
> `"template-pack requires at least two reference pack directories. Please provide paths to
> existing pack directories containing entry.yaml, instructions.yaml, and template.md."`

Extract and record from each pack:

**From entry.yaml:**
- Field names and their order — these become the schema for the new file.
- Which fields are always present vs. conditional.
- Value conventions (e.g. is `ontology_class` a full URI or CURIE? Is `phase_order` an integer?).

**From instructions.yaml:**
- Top-level keys and order (`version`, `document`, `gates`, `completion`).
- Gate field names present in every gate vs. conditional fields (`validation`, `guidance`, `deferred_value`).
- Gate `type` values in use (`prose`, `section`, `list`).
- How `fills` is formatted (e.g. `"## Section Heading"` — note the exact prefix).
- How `maps_to` is formatted (namespace prefix + property name casing style).
- Completion block structure: keys present, value types, use of `null`.

**From template.md:**
- Frontmatter field names and order.
- Title line pattern (note `{{placeholder}}` token syntax and position).
- Purpose block pattern (blockquote structure, labels, content).
- Section heading format — must match `fills` values character-for-character.
- Placeholder token syntax (e.g. `{{gate_id}}`).
- Inline comment style (e.g. `<!-- maps to: property -->`).
- Guidance comment style (e.g. `<!-- Brief description of expected content -->`).
- Section divider usage (e.g. `---` between sections).
- Footer/attribution pattern.

---

## Step 2 — Resolve property CURIEs

If an ontology file was provided, read it. For the target class, list its data and object
properties (domain + range). These are candidates for `maps_to` values.

Match gates to properties: when a gate captures a specific typed value (status, date,
decision enumeration), use the dedicated property (e.g. `okf:decision`). When a gate
captures rich narrative text with no dedicated property, use the generic description
property from the references (e.g. `dct:description`).

Do not invent CURIEs — flag any unverifiable `maps_to` value in the output report.

---

## Step 3 — Research the standard (if URL provided)

Fetch the URL. Identify:

1. **Required sections** → required gates (one gate per section).
2. **Optional sections or quality criteria** → optional gates.
3. **Purpose statement** → used in template.md purpose block and entry.yaml description.
4. **Document dependencies** → used for `dependencies` in entry.yaml.

Write every gate prompt from what the standard or framework actually says. If the framework
says "Record the value hypothesis and the condition that would falsify it", the gate prompt
says exactly that — not generic placeholder text.

If no URL is provided, derive gates from the class properties and known content requirements
of the document type. Use reference pack gate density as a guide (typically 4–8 gates).

---

## Step 4 — Design the gate list

Produce an ordered gate list. Rules:

- **One gate per template section.** No gate without a section; no section without a gate.
- **Gate `id`** is snake_case derived from the section heading (`## Step Decision` → `step_decision`).
- **Gate `order`** is a 1-based integer in document reading order.
- **`fills`** is the exact section heading string as it will appear in template.md.
- **`maps_to`** is the verified property CURIE this gate captures.
- **`required`** is `true` for sections the standard mandates; `false` for optional sections.
- **`type`** follows reference convention: `prose` for single narrative blocks, `section` for multi-part structured content, `list` for bullet/table content.
- **`guidance`** only when the gate needs extra agent instruction beyond the prompt.
- **`validation`** only when a machine-checkable rule applies.
- **`deferred_value`** for optional gates only; reproduce the reference wording exactly.

Completion block:
- `required_gates`: IDs of every gate where `required: true`.
- `output_status`: reproduce from references (typically `draft`).
- `next_document`: slug of the next pack in chain, or `null` if terminal.

---

## Step 5 — Cross-check alignment

Before writing any file, verify:

1. **Gate ↔ section parity:** every `fills` value appears as a heading in the planned template, and every planned heading corresponds to a gate. Any mismatch is a **blocking error** — fix before proceeding.
2. **Required gates consistency:** every `required: true` gate is in `completion.required_gates`, and every ID in `required_gates` is marked `required: true`. Mismatches are blocking.
3. **Placeholder coverage:** every gate has a `{{gate_id}}` token planned for its template section.

State the cross-check result explicitly before writing any file.

---

## Step 6 — Write entry.yaml

Use the field names, order, and value conventions from the reference packs. Include every
field present in both references. Omit fields present in only one reference if they are
clearly domain-specific to that pack. Set `shacl_shape` to the expected default path
(`shapes/{namespace}/{slug}.shacl.ttl`) — note it as pending if the shape does not yet exist.

---

## Step 7 — Write instructions.yaml

Use the top-level key order and gate field order from the reference packs. Include a header
comment block in the style of the references (document type, standard basis, usage notes).

---

## Step 8 — Write template.md

1. **Frontmatter** — reproduce field names and order from references. Set `status: draft`.
2. **Title** — follow reference pattern; include `{{placeholder}}` tokens for variable parts.
3. **Purpose block** — reproduce the blockquote structure; include purpose, phase/category, and standard.
4. **Sections** — one `##` heading per gate in gate order. Heading text must match `fills` exactly (character-for-character).
5. **Per-section body:**
   - `<!-- maps to: {maps_to} -->` comment (match reference style exactly).
   - Brief guidance comment describing expected content (match reference comment style).
   - `{{gate_id}}` placeholder on its own line.
   - `---` divider after each section if the references use one.
6. **Footer** — reproduce reference footer/attribution, updated for this document type.

---

## Step 9 — Write files and report

Create the pack directory and write all three files. Report:

- Output directory path
- Gate count (required / optional breakdown)
- Cross-check result (pass or fail + detail)
- Any `maps_to` CURIEs that could not be verified against the ontology (flag for review)

---

## Rules

- **Never hardcode conventions.** All field names, gate structure, placeholder syntax, and frontmatter keys come from the reference packs only.
- **Fail loudly on missing references.** Fewer than two pack directories → stop and ask.
- **Gate ↔ section parity is non-negotiable.** Every gate has a section; every section has a gate. Enforce in Step 5 — do not write output with a mismatch.
- **Prompts come from the standard.** Every prompt must be traceable to a specific requirement in the source standard or framework. Do not write generic boilerplate.
- **`maps_to` must be verifiable.** Flag unverifiable CURIEs in the report; never silently invent them.
- **One pack, one directory.** All three files live in one directory named after the slug.
