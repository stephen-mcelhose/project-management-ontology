"""Tool: get_phase_gates — return all gate ids and prompts for the current phase.

Returns {document_id: {gate_id: prompt}} for every document in the phase.
The agent uses this map to recognise volunteered information and route it to
the correct document/gate without guessing ids.
"""

from __future__ import annotations

import yaml
from pathlib import Path
from typing import Any, Protocol

from agent.lifecycle.gates import Gate


class GateReaderProtocol(Protocol):
    def load_gates(self, doc_dir: str) -> list[Gate]: ...


def get_phase_gates(
    phase: str,
    templates_dir: str,
    gate_reader: GateReaderProtocol,
) -> dict[str, dict[str, str]]:
    """Return {document_id: {gate_id: prompt}} for all documents in the phase.

    Reads the phase manifest to discover documents, then loads each document's
    gates. Silently skips any document whose instructions.yaml is missing.
    """
    manifest_path = Path(templates_dir) / phase / "_manifest.yaml"
    if not manifest_path.exists():
        return {}

    manifest = yaml.safe_load(manifest_path.read_text())
    result: dict[str, dict[str, str]] = {}

    for doc_entry in manifest.get("documents", []):
        doc_id = doc_entry["id"]
        doc_dir = str(Path(templates_dir) / phase / doc_id)
        try:
            gates = gate_reader.load_gates(doc_dir)
            result[doc_id] = {g.id: g.prompt for g in gates}
        except FileNotFoundError:
            pass

    return result
