#!/usr/bin/env python3
"""
Validate all Turtle/OWL files in ontology/ using rdflib.
Usage: python tools/validate/validate.py
"""
import sys
from pathlib import Path
from rdflib import Graph, exceptions

ONTOLOGY_DIR = Path(__file__).parent.parent.parent / "ontology"


def validate_ttl(path: Path) -> bool:
    g = Graph()
    try:
        g.parse(path, format="turtle")
        print(f"  ✓ {path.relative_to(ONTOLOGY_DIR.parent.parent)}")
        return True
    except exceptions.ParserError as e:
        print(f"  ✗ {path.relative_to(ONTOLOGY_DIR.parent.parent)}: {e}", file=sys.stderr)
        return False


def main():
    files = list(ONTOLOGY_DIR.rglob("*.ttl"))
    if not files:
        print("No .ttl files found.")
        sys.exit(1)

    print(f"Validating {len(files)} Turtle file(s)...\n")
    results = [validate_ttl(f) for f in sorted(files)]

    passed = sum(results)
    failed = len(results) - passed
    print(f"\n{passed}/{len(results)} passed")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
