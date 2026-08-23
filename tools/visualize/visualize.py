#!/usr/bin/env python3
"""
Generate ontology visualizations. Produces two SVG files:

  documents.svg      — Document lifecycle view: phases as clusters,
                       hasHardDependency as arrows, colour-coded by phase.
  class-hierarchy.svg — Full OWL class hierarchy, colour-coded by namespace.

Usage:
  python tools/visualize/visualize.py [--output-dir docs/generated]
  make visualize
"""
import argparse
import subprocess
import sys
from pathlib import Path

from rdflib import Graph, OWL, RDF, RDFS, Namespace, URIRef

ONTOLOGY_DIR = Path(__file__).parent.parent.parent / "ontology"
DEFAULT_OUT  = Path(__file__).parent.parent.parent / "docs" / "generated"

PM     = Namespace("https://stephen-mcelhose.github.io/project-management-ontology/")
PHASES = Namespace("https://stephen-mcelhose.github.io/project-management-ontology/phases/")
PROJ   = Namespace("https://linked.data.gov.au/def/project#")
PROV   = Namespace("http://www.w3.org/ns/prov#")
FOAF   = Namespace("http://xmlns.com/foaf/0.1/")

# DIN 69901 phase order and display metadata
PHASE_META = [
    (PHASES.Initiation,       "1 · Initiation",       "#d4edda", "#28a745"),
    (PHASES.Planning,         "2 · Planning",          "#cce5ff", "#004085"),
    (PHASES.Execution,        "3 · Execution",         "#fff3cd", "#856404"),
    (PHASES.MonitoringControl,"4 · Monitoring & Control","#f8d7da","#721c24"),
    (PHASES.Closure,          "5 · Closure",           "#e2d9f3", "#6f42c1"),
]


# ── Helpers ────────────────────────────────────────────────────────────────────

def load(ontology_dir: Path) -> Graph:
    g = Graph()
    for ttl in sorted(ontology_dir.rglob("*.ttl")):
        try:
            g.parse(ttl, format="turtle")
        except Exception as e:
            print(f"  ⚠  Could not load {ttl.name}: {e}", file=sys.stderr)
    return g


def lbl(g: Graph, uri: URIRef) -> str:
    for o in g.objects(uri, RDFS.label):
        if getattr(o, "language", None) in ("en", None):
            return str(o)
    return str(uri).split("/")[-1].split("#")[-1]


def dot_id(uri: URIRef) -> str:
    """Safe Graphviz node identifier from a URI."""
    return str(uri).split("/")[-1].split("#")[-1].replace("-", "_").replace("&", "")


def render(dot_src: str, out_path: Path) -> None:
    dot_path = out_path.with_suffix(".dot")
    dot_path.write_text(dot_src)
    try:
        subprocess.run(
            ["dot", "-Tsvg", str(dot_path), "-o", str(out_path)],
            check=True, capture_output=True,
        )
        print(f"  ✓  {out_path.name}")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"  ⚠  Graphviz error for {out_path.name}: {e}", file=sys.stderr)


# ── View 1: Document lifecycle ─────────────────────────────────────────────────

def build_documents_dot(g: Graph) -> str:
    lines = [
        "digraph documents {",
        "  rankdir=LR;",
        "  graph [fontname=\"Helvetica\" fontsize=13 pad=0.4 nodesep=0.5 ranksep=1.2];",
        "  node  [fontname=\"Helvetica\" fontsize=11 shape=box style=\"filled,rounded\" margin=\"0.2,0.1\"];",
        "  edge  [fontname=\"Helvetica\" fontsize=9];",
        "",
    ]

    # Collect all document classes and their phases
    foaf_doc = FOAF.Document
    doc_classes = {
        s for s in g.subjects(RDFS.subClassOf, foaf_doc)
        if isinstance(s, URIRef)
    }

    doc_phase: dict[URIRef, URIRef] = {}
    for doc in doc_classes:
        for phase in g.objects(doc, PM.producedInPhase):
            doc_phase[doc] = phase

    # Phase clusters
    for phase_uri, phase_label, fill, border in PHASE_META:
        phase_docs = [d for d, p in doc_phase.items() if str(p) == str(phase_uri)]
        if not phase_docs:
            continue

        cluster_id = dot_id(phase_uri)
        lines += [
            f'  subgraph cluster_{cluster_id} {{',
            f'    label="{phase_label}";',
            f'    style="filled,rounded";',
            f'    fillcolor="{fill}";',
            f'    color="{border}";',
            f'    penwidth=2;',
            "",
        ]
        for doc in sorted(phase_docs, key=lambda d: lbl(g, d)):
            nid  = dot_id(doc)
            name = lbl(g, doc)
            lines.append(
                f'    {nid} [label="{name}" fillcolor="white" color="{border}" penwidth=1.5];'
            )
        lines += ["  }", ""]

    # Dependency edges
    lines.append("  // hasHardDependency edges")
    for doc in sorted(doc_classes, key=lambda d: lbl(g, d)):
        for dep in g.objects(doc, PM.hasHardDependency):
            if not isinstance(dep, URIRef):
                continue
            src = dot_id(doc)
            tgt = dot_id(dep)
            # Colour: cross-phase deps are bold orange, same-phase are grey
            src_phase = str(doc_phase.get(doc, ""))
            tgt_phase = str(doc_phase.get(dep, ""))
            if src_phase != tgt_phase:
                style = 'color="#e07b00" penwidth=2 style=dashed'
            else:
                style = 'color="#555555" penwidth=1.2'
            lines.append(f'  {src} -> {tgt} [{style} label="requires"];')

    lines.append("}")
    return "\n".join(lines)


# ── View 2: Class hierarchy ────────────────────────────────────────────────────

def ns_colour(uri: URIRef) -> tuple[str, str]:
    """(fillcolor, fontcolor) by namespace."""
    s = str(uri)
    if s.startswith(str(PM)):     return "#cce5ff", "#004085"   # pm: — blue
    if s.startswith(str(PROJ)):   return "#d4edda", "#155724"   # proj: — green
    if s.startswith(str(PROV)):   return "#fff3cd", "#856404"   # prov: — yellow
    if s.startswith(str(FOAF)):   return "#f8d7da", "#721c24"   # foaf: — red
    return "#f0f0f0", "#333333"                                  # other — grey


def build_hierarchy_dot(g: Graph) -> str:
    # Only include classes that have rdfs:label (excludes blank nodes etc.)
    classes = {
        s for s in g.subjects(RDF.type, OWL.Class)
        if isinstance(s, URIRef) and list(g.objects(s, RDFS.label))
    }

    lines = [
        "digraph hierarchy {",
        "  rankdir=BT;",
        "  graph [fontname=\"Helvetica\" fontsize=12 pad=0.5 nodesep=0.4 ranksep=0.9];",
        "  node  [fontname=\"Helvetica\" fontsize=10 shape=box style=\"filled,rounded\"];",
        "  edge  [fontname=\"Helvetica\" fontsize=8 color=\"#555555\"];",
        "",
        "  // Legend",
        '  subgraph cluster_legend {',
        '    label="Namespace";  style=filled;  fillcolor="#fafafa";  color="#cccccc";',
        '    pm_leg   [label="pm:"   fillcolor="#cce5ff" fontcolor="#004085"];',
        '    proj_leg [label="proj:" fillcolor="#d4edda" fontcolor="#155724"];',
        '    prov_leg [label="prov:" fillcolor="#fff3cd" fontcolor="#856404"];',
        '    foaf_leg [label="foaf:" fillcolor="#f8d7da" fontcolor="#721c24"];',
        '  }',
        "",
    ]

    ids: dict[URIRef, str] = {}
    for i, cls in enumerate(sorted(classes, key=str)):
        nid  = f"n{i}"
        ids[cls] = nid
        fill, font = ns_colour(cls)
        name = lbl(g, cls)
        lines.append(f'  {nid} [label="{name}" fillcolor="{fill}" fontcolor="{font}"];')

    lines.append("")
    for cls in sorted(classes, key=str):
        for parent in g.objects(cls, RDFS.subClassOf):
            if isinstance(parent, URIRef) and parent in ids:
                lines.append(f'  {ids[cls]} -> {ids[parent]};')

    lines.append("}")
    return "\n".join(lines)


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default=str(DEFAULT_OUT))
    args = parser.parse_args()

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    print("Loading ontology...")
    g = load(ONTOLOGY_DIR)
    print(f"  {len(g)} triples\n")

    print("Generating visualizations...")
    render(build_documents_dot(g),  out / "documents.svg")
    render(build_hierarchy_dot(g),  out / "class-hierarchy.svg")
    print(f"\nOutput → {out}/")


if __name__ == "__main__":
    main()
