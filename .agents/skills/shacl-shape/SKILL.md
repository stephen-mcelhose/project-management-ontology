---
name: shacl-shape
description: >
  Author a SHACL NodeShape from reference examples. Given one or more reference shape files
  and a class specification, produce a new NodeShape whose prefix block, baseline constraints,
  datatype convention, and message register exactly match the references. The skill is
  domain-agnostic — it reads all conventions from the workspace, never assumes them.
  Default output: domains/{namespace}/shapes/{classname}.shacl.ttl (namespace derived from the class
  prefix, e.g. okf:POCStepEvidence → domains/okf/shapes/poc-step-evidence.shacl.ttl).
  Trigger on: "/shacl-shape", "generate a SHACL shape for", "create a shape for",
  "add a SHACL shape", "write a NodeShape for", "validate [ClassName] with SHACL".
version: "1.0.0"
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
---

# shacl-shape — SHACL NodeShape Author

Produce a new SHACL NodeShape that exactly matches the conventions of the project's existing
shapes: same prefix block, same baseline properties, same datatype choices, same message
wording register.

---

## Inputs

Gather these before starting. Ask with `AskUserQuestion` if missing.

| Input | Required | Description |
| ----- | -------- | ----------- |
| Reference shape paths | Yes (≥2) | Paths to existing `.shacl.ttl` files in the workspace. Fail loudly if fewer than two are provided. |
| Class CURIE | Yes | Namespace-prefixed class (e.g. `okf:POCStepEvidence`). The prefix is used to derive the default output namespace. |
| Class URI | Yes | Full IRI for the class (e.g. `https://eis-intake-firehose/ontology/okf#POCStepEvidence`). |
| Shape namespace prefix | Recommended | Prefix and IRI for shape names (e.g. `okf-sh:` → `<https://eis-intake-firehose/ontology/okf/shapes#>`). Derive from reference shapes if not given. |
| Ontology file path | Recommended | Path to the OWL/Turtle ontology file so properties and enumerations can be read directly. |
| Class-specific properties | Yes | Properties for this class: each with path CURIE, cardinality (min/max), datatype or class constraint, and a plain-English description of what the constraint validates. |
| Output path | Optional | Full file path override. If omitted, defaults to `domains/{namespace}/shapes/{slug}.shacl.ttl` where `{namespace}` is the class prefix (e.g. `okf`) and `{slug}` is the kebab-case class name. |

### Default output path derivation

Given class CURIE `okf:POCStepEvidence`:
- Namespace: `okf`
- Slug: `poc-step-evidence` (CamelCase → kebab-case)
- Default path: `domains/okf/shapes/poc-step-evidence.shacl.ttl`

If the output directory does not exist, create it. If an explicit output path is given,
use it instead.

---

## Step 1 — Read reference shapes

Read **every** reference shape file provided. Fail with a clear error if fewer than two
files are given:
> `"shacl-shape requires at least two reference shape files. Please provide paths to
> existing .shacl.ttl files in the project."`

Extract and record:

1. **Prefix block** — the exact `@prefix` declarations in order.
2. **Primer comment block** — the header comment (SHACL explanation, validation command). Record its structure and the variable parts (file path, class name).
3. **NodeShape naming pattern** — how the shape is named (`{shape-prefix}:{ClassName}Shape`).
4. **`rdfs:label` and `rdfs:comment` patterns** — language tags, sentence structure.
5. **Baseline property constraints** — constraints that appear in **every** reference shape. Record `sh:path`, cardinality, datatype, and the full `sh:message` text including language tag.
6. **Datatype convention** — `xsd:string` or `rdf:langString`; whether `@en` tags are used on messages.
7. **Message wording pattern** — sentence structure, article ("A {ClassName} must…"), how property names appear.
8. **Section comment style** — format of inline comments above property blocks (e.g. `# ── Label ──────`).

---

## Step 2 — Read ontology (if provided)

Read the ontology file. For the target class:
- Confirm it exists.
- List its data properties and object properties (domain + range).
- Note any cardinality comments in the file (e.g. `# POC requires exactly 3 POCStepEvidence`).
- Note enumeration values for restricted properties (e.g. `okf:status` constrained to a set via `owl:oneOf`).

Use this to fill in or validate the class-specific properties input.

---

## Step 3 — Write the prefix block

Reproduce the prefix block **exactly** as found in the reference shapes. Add only the
domain-specific prefixes needed for this class (class namespace, shape namespace) if they
differ from the references. Do not add prefixes that are not used.

---

## Step 4 — Write the primer comment block

Reproduce the primer comment block from the references verbatim, substituting:
- The output file path (top of the comment)
- The class name in the "what is this file?" sentence
- The class name in the `sh:targetClass` example line
- The class name in the property example line
- The output file path in the `pyshacl -s` validation command

All explanatory prose (what SHACL is, "how to read a shape", tool install) is copied
verbatim from the reference.

---

## Step 5 — Write the NodeShape declaration

```turtle
{shape-ns}:{ClassName}Shape
    a sh:NodeShape ;

    # Target: applies to any RDF node typed as {ns}:{ClassName}
    sh:targetClass {ns}:{ClassName} ;

    rdfs:label "{ClassName} shape"@en ;
    rdfs:comment "{One sentence describing what this shape validates and against which standard.}"@en ;
```

`rdfs:label` pattern: `"{ClassName} shape"@en` (lowercase "shape").
`rdfs:comment`: "Validates that a filled {ClassName} instance satisfies…" — tailor to the
actual standard or requirement this class represents.

---

## Step 6 — Write baseline property constraints

Reproduce every property constraint found in all reference shapes in Step 1 (item 5),
in the same order they appeared in the references, using the same section comment style.

Do not modify, reorder, or omit any baseline constraint.

---

## Step 7 — Write class-specific property constraints

For each property in the class-specific inputs:

```turtle
    # ── {Plain-English label} ────────────────────────────────────────────────
    sh:property [
        sh:path     {prefix}:{property} ;
        sh:minCount {n} ;
        [sh:maxCount {n} ;]
        [sh:datatype {xsd:type} ;]
        [sh:class    {ns}:{ClassName} ;]
        [sh:hasValue {value} ;]
        [sh:minLength {n} ;]
        [sh:in       ({value1} {value2} …) ;]
        sh:message  "A {ClassName} must {plain-English requirement}."@en ;
    ] ;
```

Rules:
- Use `sh:in` for enumeration-constrained properties (status, decision, etc.).
- Use `sh:class` for object properties whose range is an OWL class.
- Use `sh:hasValue` for fixed-value constraints.
- `sh:datatype` from ontology range or project convention.
- `sh:message` follows the exact wording pattern from the references.
- The final property block closes with ` .` (not ` ;`).

---

## Step 8 — Secondary shapes (if needed)

If the reference shapes include secondary NodeShape blocks for linked node types, and the
class inputs warrant similar linked-node validation, add secondary shapes following the same
pattern. Secondary shapes are optional — only add when clearly useful.

---

## Step 9 — Parse check

Run before writing:

```bash
python3 -c "
from rdflib import Graph; import sys
g = Graph()
try:
    g.parse('{output_path}', format='turtle')
    print('OK —', len(g), 'triples')
except Exception as e:
    print('PARSE ERROR:', e); sys.exit(1)
"
```

If rdflib is unavailable, check manually:
- Balanced `[` / `]` brackets
- Every `sh:property [` block closed before the next
- Last triple ends with ` .`
- No conflict markers

Do not write the file if the parse check fails. Diagnose and fix first.

---

## Step 10 — Write and report

Write to the resolved output path (default or explicit). Create the directory if needed.
Report:
- Output path
- Property constraint count (baseline + class-specific)
- Parse result

---

## Rules

- **Never hardcode conventions.** All prefix block, baseline properties, datatype choices, and message style come from the reference shapes.
- **Fail loudly on missing references.** Fewer than two reference shapes → stop and ask.
- **Never invent properties.** If a class-specific property isn't in the ontology and the user hasn't specified it, flag it and ask.
- **Parse before writing.** A shape with a syntax error has zero value.
- **One file per class.** Secondary shapes for linked nodes go in the same file.
