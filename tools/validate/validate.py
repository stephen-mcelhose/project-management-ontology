#!/usr/bin/env python3
"""
Validate all Turtle/OWL files in domains/pm/ontology/ using rdflib.

Checks:
  1. Syntax  — every .ttl file parses without error
  2. Semantic — structural invariants on the pm: ontology graph

Usage: python tools/validate/validate.py
       make validate
"""
import sys
from pathlib import Path

from rdflib import OWL, RDF, RDFS, Graph, Namespace, exceptions

ONTOLOGY_DIR = Path(__file__).parent.parent.parent / "domains" / "pm" / "ontology"

PM     = Namespace("https://stephen-mcelhose.github.io/process-assistant/pm/")
PROJ   = Namespace("https://linked.data.gov.au/def/project#")
PROV   = Namespace("http://www.w3.org/ns/prov#")
PHASES = Namespace("https://stephen-mcelhose.github.io/process-assistant/pm/phases/")

HASH_NS = "https://stephen-mcelhose.github.io/process-assistant/pm#"


# ── Step 1: Syntax ─────────────────────────────────────────────────────────────

def validate_syntax(files: list[Path]) -> tuple[int, int]:
    passed = failed = 0
    for path in sorted(files):
        g = Graph()
        try:
            g.parse(path, format="turtle")
            print(f"  ✓ {path.relative_to(ONTOLOGY_DIR.parent)}")
            passed += 1
        except exceptions.ParserError as e:
            print(f"  ✗ {path.relative_to(ONTOLOGY_DIR.parent)}: {e}", file=sys.stderr)
            failed += 1
    return passed, failed


# ── Step 2: Semantic ───────────────────────────────────────────────────────────

def validate_semantics(g: Graph) -> list[str]:
    errors = []

    def chk(cond: bool, msg: str) -> None:
        if not cond:
            errors.append(msg)
        else:
            print(f"  ✓ {msg}")

    # Namespace consistency — no hash-style pm: classes
    bad = [str(s) for s in g.subjects(RDF.type, OWL.Class) if str(s).startswith(HASH_NS)]
    chk(not bad, f"No hash-namespace classes (found {len(bad)})")

    # PROJ wiring
    chk((PM.Project, RDFS.subClassOf, PROJ.Project) in g,
        ":Project rdfs:subClassOf proj:Project")
    chk((PROJ.Project, RDFS.subClassOf, PROV.Activity) in g,
        "proj:Project rdfs:subClassOf prov:Activity (stated in vendor/proj.ttl)")
    chk((PM.Phase, RDFS.subClassOf, PROV.Activity) in g,
        ":Phase rdfs:subClassOf prov:Activity")

    # DIN 69901 phase vocabulary
    expected = ["Initiation", "Planning", "Execution", "MonitoringControl", "Closure"]
    missing = [p for p in expected if (PHASES[p], RDF.type, PM.PhaseType) not in g]
    chk(not missing, f"All 5 DIN 69901 phases defined ({', '.join(missing) if missing else 'OK'})")

    # Document annotation property — domain must be foaf:Document, not a pm: stub
    FOAF = Namespace("http://xmlns.com/foaf/0.1/")
    chk((PM.producedInPhase, RDF.type, OWL.ObjectProperty) in g,
        ":producedInPhase ObjectProperty defined")
    chk((PM.producedInPhase, RDFS.domain, FOAF.Document) in g,
        ":producedInPhase domain is foaf:Document (not a pm: stub)")

    # All OWL classes must have rdfs:label
    classes = list(g.subjects(RDF.type, OWL.Class))
    unlabelled = [str(c) for c in classes if not list(g.objects(c, RDFS.label))]
    chk(not unlabelled,
        f"All {len(classes)} owl:Class resources have rdfs:label "
        f"({', '.join(unlabelled) if unlabelled else 'OK'})")

    return errors


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    files = list(ONTOLOGY_DIR.rglob("*.ttl"))
    if not files:
        print("No .ttl files found.", file=sys.stderr)
        sys.exit(1)

    # Syntax
    print(f"── Syntax ({len(files)} files) ─────────────────────────────────────")
    passed, failed = validate_syntax(files)
    print(f"\n  {passed}/{len(files)} passed\n")
    if failed:
        sys.exit(1)

    # Semantics
    print("── Semantics ────────────────────────────────────────────────────────")
    g = Graph()
    for ttl in sorted(files):
        g.parse(ttl, format="turtle")

    errors = validate_semantics(g)
    print()
    if errors:
        for e in errors:
            print(f"  ✗ {e}", file=sys.stderr)
        print(f"\n  {len(errors)} semantic error(s). Fix before proceeding.", file=sys.stderr)
        sys.exit(1)
    else:
        print("  All semantic checks passed.")


if __name__ == "__main__":
    main()
