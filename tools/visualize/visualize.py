#!/usr/bin/env python3
"""
Generate a class/property graph from ontology TTL files and output as:
  - Graphviz DOT  → ontology-graph.dot
  - SVG           → ontology-graph.svg  (requires graphviz CLI)
  - HTML          → ontology-graph.html (interactive, uses vis.js CDN)

Usage:
  python tools/visualize/visualize.py [--output-dir docs/generated]
"""
import argparse
import subprocess
import sys
from pathlib import Path

from rdflib import Graph, OWL, RDF, RDFS, Namespace
from rdflib.namespace import XSD

PM = Namespace("https://stephen-mcelhose.github.io/project-management-ontology/")

ONTOLOGY_DIR = Path(__file__).parent.parent.parent / "ontology"
DEFAULT_OUT = Path(__file__).parent.parent.parent / "docs" / "generated"


def load_ontology(ontology_dir: Path) -> Graph:
    g = Graph()
    for ttl in sorted(ontology_dir.rglob("*.ttl")):
        try:
            g.parse(ttl, format="turtle")
        except Exception as e:
            print(f"  ⚠ Could not load {ttl.name}: {e}", file=sys.stderr)
    return g


def label(g: Graph, uri) -> str:
    for o in g.objects(uri, RDFS.label):
        if getattr(o, "language", None) in ("en", None):
            return str(o)
    return str(uri).split("/")[-1].split("#")[-1]


def build_dot(g: Graph) -> str:
    classes = set(g.subjects(RDF.type, OWL.Class))
    lines = [
        "digraph ontology {",
        '  rankdir=BT;',
        '  node [shape=box, style=filled, fillcolor="#e8f4f8", fontname="Helvetica"];',
        '  edge [fontname="Helvetica", fontsize=10];',
        "",
    ]
    ids: dict = {}
    for i, cls in enumerate(classes):
        node_id = f"c{i}"
        ids[cls] = node_id
        lines.append(f'  {node_id} [label="{label(g, cls)}"];')

    lines.append("")
    for cls in classes:
        for parent in g.objects(cls, RDFS.subClassOf):
            if parent in ids:
                lines.append(f'  {ids[cls]} -> {ids[parent]} [label="subClassOf", color="#555"];')

    lines.append("}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default=str(DEFAULT_OUT))
    args = parser.parse_args()

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    print("Loading ontology...")
    g = load_ontology(ONTOLOGY_DIR)
    print(f"  {len(g)} triples loaded")

    dot_src = build_dot(g)
    dot_path = out / "ontology-graph.dot"
    dot_path.write_text(dot_src)
    print(f"  ✓ DOT written to {dot_path}")

    svg_path = out / "ontology-graph.svg"
    try:
        subprocess.run(
            ["dot", "-Tsvg", str(dot_path), "-o", str(svg_path)],
            check=True, capture_output=True
        )
        print(f"  ✓ SVG written to {svg_path}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("  ⚠ Graphviz not found — skipping SVG. Install with: brew install graphviz")

    print("Done.")


if __name__ == "__main__":
    main()
