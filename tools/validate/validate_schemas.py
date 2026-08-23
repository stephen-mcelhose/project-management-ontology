#!/usr/bin/env python3
"""Validate the artifact layer against schema, ontology, and manifest contracts.

Two validation passes:

1. instructions.yaml — validates every gate file against
   tools/schemas/instructions-schema.json and checks that maps_to CURIEs
   resolve in the OWL ontology graph.

2. Manifest consistency — validates templates/_project-manifest.yaml and the
   five phase _manifest.yaml files for internal cross-references:
   - Every phases[].id has a _manifest.yaml on disk.
   - Every _manifest.yaml on disk is listed in phases (no missing registrations).
   - Every cross_phase_context[].field is a real gate id in the named document.
   - Every cross_phase_context[].first_captured_in resolves to an existing
     instructions.yaml.
   - Every phase _manifest.yaml completion block has transition_condition.

Exits 0 if every check passes, 1 if any check fails.
"""

import json
import sys
from pathlib import Path

import jsonschema
import rdflib
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "tools" / "schemas" / "instructions-schema.json"
TEMPLATES_DIR = REPO_ROOT / "templates"
ONTOLOGY_DIR = REPO_ROOT / "ontology"

# Entry-point Turtle that declares the canonical pm: and dct: prefixes.
PM_ONTOLOGY_TTL = ONTOLOGY_DIR / "core" / "pm-ontology.ttl"


# ── Ontology loading ──────────────────────────────────────────────────────────


def _load_ontology() -> tuple[rdflib.Graph, dict[str, str]]:
    """Load all ontology Turtle files and return (graph, curie_prefix_map).

    The prefix map is extracted from pm-ontology.ttl before merging all files,
    because parsing multiple files together can clobber short prefixes with the
    default namespace.
    """
    # Step 1: extract the canonical prefix map from the entry-point file.
    seed = rdflib.Graph()
    seed.parse(PM_ONTOLOGY_TTL, format="turtle")
    curie_prefixes: dict[str, str] = {
        prefix: str(ns)
        for prefix, ns in seed.namespace_manager.namespaces()
        if prefix  # skip empty-string default namespace
    }

    # Step 2: load all Turtle files for the full existence check.
    graph = rdflib.Graph()
    for ttl in sorted(ONTOLOGY_DIR.rglob("*.ttl")):
        try:
            graph.parse(str(ttl), format="turtle")
        except (OSError, rdflib.exceptions.ParserError) as exc:
            print(f"  ⚠ Could not parse {ttl.relative_to(REPO_ROOT)}: {exc}", file=sys.stderr)

    return graph, curie_prefixes


def _uri_exists(uri: rdflib.URIRef, graph: rdflib.Graph) -> bool:
    """True if uri appears as a subject or predicate anywhere in the graph."""
    return (uri, None, None) in graph or (None, uri, None) in graph


# ── CURIE resolution ──────────────────────────────────────────────────────────


def check_maps_to(
    curie: str,
    graph: rdflib.Graph,
    curie_prefixes: dict[str, str],
    local_prefix: str = "pm",
) -> str | None:
    """Return an error string if the CURIE cannot be resolved, else None.

    Rules:
    - Unknown prefix → skip (warn, do not fail — may be an external vocab
      not imported into our ontology graph).
    - Known prefix that resolves to a URI not in the graph → error for the
      local namespace (pm:), warning for externals.
    """
    if ":" not in curie:
        return f"maps_to: '{curie}' is not a valid CURIE (missing prefix)"

    prefix, local = curie.split(":", 1)

    if prefix not in curie_prefixes:
        # Unknown prefix — not necessarily wrong, just untracked.
        return None

    uri = rdflib.URIRef(curie_prefixes[prefix] + local)

    if _uri_exists(uri, graph):
        return None

    if prefix == local_prefix:
        # Our own namespace — this is a hard error.
        return (
            f"maps_to: '{curie}' not found in ontology "
            f"[{uri}]"
        )
    else:
        # External namespace — report as a warning, not a blocking error.
        print(
            f"      ⚠ maps_to: '{curie}' not found in imported vocabularies "
            f"[{uri}]",
            file=sys.stderr,
        )
        return None


# ── Schema loading ────────────────────────────────────────────────────────────


def load_schema() -> dict:
    with SCHEMA_PATH.open() as f:
        return json.load(f)


# ── Validation ────────────────────────────────────────────────────────────────


def validate_all(
    schema: dict,
    graph: rdflib.Graph,
    curie_prefixes: dict[str, str],
) -> tuple[int, int]:
    validator = jsonschema.Draft7Validator(schema)
    files = sorted(TEMPLATES_DIR.rglob("instructions.yaml"))

    if not files:
        print("No instructions.yaml files found.", file=sys.stderr)
        sys.exit(1)

    passed = 0
    failed = 0

    for path in files:
        rel = path.relative_to(REPO_ROOT)
        try:
            doc = yaml.safe_load(path.read_text())
        except yaml.YAMLError as exc:
            print(f"  ✗ {rel}  YAML parse error: {exc}", file=sys.stderr)
            failed += 1
            continue

        errors = sorted(validator.iter_errors(doc), key=lambda e: list(e.absolute_path))

        # ── Cross-reference checks ────────────────────────────────────────────
        # JSON Schema draft-07 cannot assert uniqueness across array items or
        # validate that one array's values exist in another array — both require
        # knowledge of the whole document at once. These checks fill that gap.
        # They are intentional behaviour of this tool, not schema limitations.
        cross_ref_errors: list[str] = []

        gate_ids = [g["id"] for g in doc.get("gates", []) if isinstance(g, dict) and "id" in g]

        # 1. Duplicate gate ids within the file.
        seen: set[str] = set()
        for gid in gate_ids:
            if gid in seen:
                cross_ref_errors.append(f"gates: duplicate id '{gid}'")
            seen.add(gid)

        # 2. Every required_gates entry must name a real gate id.
        required_gates = doc.get("completion", {}).get("required_gates", [])
        for ref in required_gates:
            if ref not in seen:
                cross_ref_errors.append(
                    f"completion.required_gates: '{ref}' does not match any gate id"
                )

        # 3. Every maps_to CURIE must resolve in the ontology.
        #    pm: CURIEs are hard errors; other known prefixes are warnings.
        for i, gate in enumerate(doc.get("gates", [])):
            if not isinstance(gate, dict):
                continue
            maps_to = gate.get("maps_to")
            if not maps_to:
                continue
            err = check_maps_to(maps_to, graph, curie_prefixes)
            if err:
                cross_ref_errors.append(f"gates[{i}] ({gate.get('id', '?')}): {err}")
        # ─────────────────────────────────────────────────────────────────────

        all_errors = bool(errors) or bool(cross_ref_errors)
        if all_errors:
            print(f"  ✗ {rel}", file=sys.stderr)
            for err in errors:
                path_str = " → ".join(str(p) for p in err.absolute_path) or "(root)"
                print(f"      {path_str}: {err.message}", file=sys.stderr)
            for msg in cross_ref_errors:
                print(f"      {msg}", file=sys.stderr)
            failed += 1
        else:
            print(f"  ✓ {rel}")
            passed += 1

    return passed, failed


# ── Manifest consistency ──────────────────────────────────────────────────────


def _gate_ids_for(instructions_path: Path) -> set[str] | None:
    """Return the set of gate ids in an instructions.yaml, or None on parse error."""
    try:
        doc = yaml.safe_load(instructions_path.read_text())
    except yaml.YAMLError:
        return None
    return {
        g["id"]
        for g in doc.get("gates", [])
        if isinstance(g, dict) and "id" in g
    }


def validate_project_manifest() -> tuple[int, int]:
    """Validate _project-manifest.yaml and phase _manifest.yaml files.

    Checks (all are blocking failures):
    1. _project-manifest.yaml exists and parses.
    2. Every phases[].id has a _manifest.yaml on disk.
    3. Every _manifest.yaml on disk is listed in phases (no missing phases).
    4. Every cross_phase_context[].first_captured_in resolves to an
       instructions.yaml that exists.
    5. Every cross_phase_context[].field is a real gate id in that file.
    6. Every phase _manifest.yaml completion block has transition_condition.

    Returns (passed, failed) where each "item" is one file checked.
    """
    passed = 0
    failed = 0

    project_path = TEMPLATES_DIR / "_project-manifest.yaml"
    rel = project_path.relative_to(REPO_ROOT)

    # ── Check 1: file exists and parses ──────────────────────────────────────
    if not project_path.exists():
        print(f"  ✗ {rel}  NOT FOUND", file=sys.stderr)
        return 0, 1

    try:
        data = yaml.safe_load(project_path.read_text())
    except yaml.YAMLError as exc:
        print(f"  ✗ {rel}  YAML parse error: {exc}", file=sys.stderr)
        return 0, 1

    errors: list[str] = []

    # ── Check 2: every declared phase has a _manifest.yaml on disk ───────────
    declared_ids: list[str] = [
        entry.get("id", "") for entry in data.get("phases", [])
    ]
    for phase_id in declared_ids:
        manifest = TEMPLATES_DIR / phase_id / "_manifest.yaml"
        if not manifest.exists():
            errors.append(
                f"phases: '{phase_id}' declared but "
                f"{manifest.relative_to(REPO_ROOT)} not found"
            )

    # ── Check 3: every _manifest.yaml on disk is listed in phases ────────────
    on_disk = {p.parent.name for p in TEMPLATES_DIR.glob("*/_manifest.yaml")}
    for phase_id in sorted(on_disk - set(declared_ids)):
        errors.append(
            f"phases: '{phase_id}' has a _manifest.yaml on disk "
            f"but is not listed in phases"
        )

    # ── Checks 4 & 5: cross_phase_context fields resolve to real gate ids ────
    for i, entry in enumerate(data.get("cross_phase_context", [])):
        field = entry.get("field", "")
        captured_in = entry.get("first_captured_in", "")

        if "/" not in captured_in:
            errors.append(
                f"cross_phase_context[{i}] ({field}): first_captured_in "
                f"'{captured_in}' must be {{phase}}/{{document}}"
            )
            continue

        phase_id, doc_id = captured_in.split("/", 1)
        instructions = TEMPLATES_DIR / phase_id / doc_id / "instructions.yaml"

        if not instructions.exists():
            errors.append(
                f"cross_phase_context[{i}] ({field}): "
                f"{instructions.relative_to(REPO_ROOT)} not found"
            )
            continue

        gate_ids = _gate_ids_for(instructions)
        if gate_ids is None:
            errors.append(
                f"cross_phase_context[{i}] ({field}): "
                f"could not parse {instructions.relative_to(REPO_ROOT)}"
            )
            continue

        if field not in gate_ids:
            errors.append(
                f"cross_phase_context[{i}]: field '{field}' is not a gate id "
                f"in {instructions.relative_to(REPO_ROOT)}"
            )

    if errors:
        print(f"  ✗ {rel}", file=sys.stderr)
        for msg in errors:
            print(f"      {msg}", file=sys.stderr)
        failed += 1
    else:
        print(f"  ✓ {rel}")
        passed += 1

    # ── Check 6: every phase _manifest.yaml has transition_condition ──────────
    for phase_manifest in sorted(TEMPLATES_DIR.glob("*/_manifest.yaml")):
        rel_pm = phase_manifest.relative_to(REPO_ROOT)
        try:
            pm_data = yaml.safe_load(phase_manifest.read_text())
        except yaml.YAMLError as exc:
            print(f"  ✗ {rel_pm}  YAML parse error: {exc}", file=sys.stderr)
            failed += 1
            continue

        if "transition_condition" not in pm_data.get("completion", {}):
            print(f"  ✗ {rel_pm}", file=sys.stderr)
            print(
                f"      completion: missing transition_condition",
                file=sys.stderr,
            )
            failed += 1
        else:
            print(f"  ✓ {rel_pm}")
            passed += 1

    return passed, failed


def main() -> None:
    schema = load_schema()

    print("── Loading ontology graph ───────────────────────────────────────────")
    graph, curie_prefixes = _load_ontology()
    known = ", ".join(f"{p}:" for p in sorted(curie_prefixes))
    print(f"  {len(graph)} triples loaded. Known CURIE prefixes: {known}\n")

    files = sorted(TEMPLATES_DIR.rglob("instructions.yaml"))
    print(f"── Schema + ontology validation ({len(files)} files) ────────────────")
    passed, failed = validate_all(schema, graph, curie_prefixes)
    print(f"\n  {passed}/{passed + failed} passed\n")

    print("── Manifest consistency validation ──────────────────────────────────")
    m_passed, m_failed = validate_project_manifest()
    print(f"\n  {m_passed}/{m_passed + m_failed} passed\n")

    if failed or m_failed:
        total = failed + m_failed
        print(
            f"  {total} check(s) failed. Fix before proceeding.",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
