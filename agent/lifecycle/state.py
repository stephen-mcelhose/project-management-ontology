"""Session state — persisted as JSON at {output_dir}/.session.json.

Writes are atomic: data is written to a .tmp file then renamed, so the
session file is either complete or absent — never partial.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class GateState:
    gate_id: str
    answer: str | None = None
    skipped: bool = False


@dataclass
class DocumentState:
    document_id: str
    gates: dict[str, GateState] = field(default_factory=dict)
    written: bool = False
    valid: bool = False


@dataclass
class SessionState:
    project_name: str = ""
    current_phase: str = ""
    current_document: str = ""
    shared_context: dict[str, str] = field(default_factory=dict)
    documents: dict[str, DocumentState] = field(default_factory=dict)

    # ── Persistence ───────────────────────────────────────────────────────────

    @classmethod
    def load(cls, path: Path) -> SessionState:
        """Load from path; return a fresh SessionState if the file is missing."""
        if not path.exists():
            return cls()
        with path.open() as f:
            data = json.load(f)
        state = cls(
            project_name=data.get("project_name", ""),
            current_phase=data.get("current_phase", ""),
            current_document=data.get("current_document", ""),
            shared_context=data.get("shared_context", {}),
        )
        for doc_id, doc_data in data.get("documents", {}).items():
            doc = DocumentState(
                document_id=doc_id,
                written=doc_data.get("written", False),
                valid=doc_data.get("valid", False),
            )
            for gate_id, gate_data in doc_data.get("gates", {}).items():
                doc.gates[gate_id] = GateState(
                    gate_id=gate_id,
                    answer=gate_data.get("answer"),
                    skipped=gate_data.get("skipped", False),
                )
            state.documents[doc_id] = doc
        return state

    def save(self, path: Path) -> None:
        """Write to disk atomically (tmp → rename)."""
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "project_name": self.project_name,
            "current_phase": self.current_phase,
            "current_document": self.current_document,
            "shared_context": self.shared_context,
            "documents": {
                doc_id: {
                    "written": doc.written,
                    "valid": doc.valid,
                    "gates": {
                        gate_id: {"answer": gs.answer, "skipped": gs.skipped}
                        for gate_id, gs in doc.gates.items()
                    },
                }
                for doc_id, doc in self.documents.items()
            },
        }
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=2))
        tmp.rename(path)

    # ── Accessors ─────────────────────────────────────────────────────────────

    def document(self, doc_id: str) -> DocumentState:
        """Return the DocumentState for doc_id, creating it if absent."""
        if doc_id not in self.documents:
            self.documents[doc_id] = DocumentState(document_id=doc_id)
        return self.documents[doc_id]

    def is_document_complete(self, doc_id: str, required_gate_ids: list[str]) -> bool:
        """True when every required gate for doc_id has a non-None answer."""
        doc = self.documents.get(doc_id)
        if doc is None:
            return False
        for gate_id in required_gate_ids:
            gs = doc.gates.get(gate_id)
            if gs is None or gs.answer is None:
                return False
        return True

    def is_phase_complete(self, phase_manifest: Any) -> bool:
        """True when all required documents are written and valid."""
        required = phase_manifest.completion.get("required_documents", [])
        for doc_id in required:
            doc = self.documents.get(doc_id)
            if doc is None or not doc.written or not doc.valid:
                return False
        return True
