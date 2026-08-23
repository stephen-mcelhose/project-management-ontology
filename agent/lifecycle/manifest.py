"""Load phase and project manifests from the template artifact layer.

Ontology mapping
----------------
PhaseManifest  → pm:Phase      (ontology/modules/phase.ttl)
DocumentEntry  → pm:Document   (ontology/modules/document.ttl)
ProjectManifest → pm:Project   (ontology/modules/project.ttl)

These Python dataclasses mirror the artifact-layer YAML schema, not the
full OWL model — the OWL classes carry richer semantics (prov:Activity
subclassing, phase ordering, etc.) that are not needed at runtime.
If you add fields here, check whether a corresponding OWL property already
exists before inventing a new one.  Run make validate-schemas to check
any maps_to CURIEs you introduce in instructions.yaml files.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class DocumentEntry:
    # Ontology: pm:Document (ontology/modules/document.ttl)
    id: str
    phase_local_order: int
    title: str
    path: str
    dependencies: list[str] = field(default_factory=list)
    required_before: list[str] = field(default_factory=list)


@dataclass
class PhaseEntry:
    # Ontology: pm:Phase (ontology/modules/phase.ttl)
    id: str


@dataclass
class PhaseManifest:
    # Ontology: pm:Phase (ontology/modules/phase.ttl)
    phase: str
    phase_label: str
    documents: list[DocumentEntry]
    shared_context: list[dict[str, Any]]
    completion: dict[str, Any]


@dataclass
class ProjectManifest:
    # Ontology: pm:Project (ontology/modules/project.ttl)
    phases: list[PhaseEntry]


def load_project_manifest(templates_dir: str) -> ProjectManifest:
    """Load templates/_project-manifest.yaml.

    Raises FileNotFoundError with the expected path if the file is missing.
    """
    path = Path(templates_dir) / "_project-manifest.yaml"
    if not path.exists():
        raise FileNotFoundError(
            f"Project manifest not found: {path}\n"
            "Create templates/_project-manifest.yaml to define phase order."
        )
    with path.open() as f:
        data = yaml.safe_load(f)
    phases = [PhaseEntry(id=p["id"]) for p in data.get("phases", [])]
    return ProjectManifest(phases=phases)


def load_phase_manifest(templates_dir: str, phase_id: str) -> PhaseManifest:
    """Load templates/{phase_id}/_manifest.yaml.

    Raises FileNotFoundError with the phase id if the file is missing.
    """
    path = Path(templates_dir) / phase_id / "_manifest.yaml"
    if not path.exists():
        raise FileNotFoundError(
            f"Phase manifest not found for '{phase_id}': {path}"
        )
    with path.open() as f:
        data = yaml.safe_load(f)

    raw_docs = data.get("documents", [])
    documents = sorted(
        [
            DocumentEntry(
                id=d["id"],
                phase_local_order=d.get("phase_local_order", 0),
                title=d.get("title", ""),
                path=d.get("path", ""),
                dependencies=d.get("dependencies", []),
                required_before=d.get("required_before", []),
            )
            for d in raw_docs
        ],
        key=lambda d: d.phase_local_order,
    )

    return PhaseManifest(
        phase=data.get("phase", phase_id),
        phase_label=data.get("phase_label", phase_id),
        documents=documents,
        shared_context=data.get("shared_context", []),
        completion=data.get("completion", {}),
    )
