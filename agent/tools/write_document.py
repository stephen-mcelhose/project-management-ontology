"""Tool: write_document — render template and write filled document to output dir."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol

from agent.lifecycle.gates import Gate
from agent.lifecycle.state import SessionState
from agent.lifecycle.template import check_required_placeholders, render_template


class GateReaderProtocol(Protocol):
    def load_gates(self, doc_dir: str) -> list[Gate]: ...


class DocumentWriterProtocol(Protocol):
    def read_template(self, doc_dir: str) -> str: ...
    def write(self, path: Path, content: str) -> None: ...
    def shape_path(self, templates_dir: str, phase: str, doc_id: str) -> Path: ...
    def doc_dir(self, templates_dir: str, phase: str, doc_id: str) -> str: ...


def write_document(
    session: SessionState,
    session_path: Path,
    document_id: str,
    templates_dir: str,
    output_dir: str,
    gate_reader: GateReaderProtocol,
    document_writer: DocumentWriterProtocol,
) -> dict[str, Any]:
    """Render template.md and write to {output_dir}/{phase}/{document_id}.md.

    Returns {written: False, error: ...} if any required gate is unanswered.
    Idempotent: re-calling overwrites the previous file.
    """
    phase = session.current_phase
    doc_dir = document_writer.doc_dir(templates_dir, phase, document_id)
    gates = gate_reader.load_gates(doc_dir)
    required_ids = [g.id for g in gates if g.required]

    doc = session.document(document_id)
    answers = {gid: gs.answer for gid, gs in doc.gates.items() if gs.answer is not None}

    template_text = document_writer.read_template(doc_dir)
    missing = check_required_placeholders(template_text, required_ids, answers)
    if missing:
        return {
            "written": False,
            "error": f"Required gates not yet answered: {missing}",
        }

    content = render_template(template_text, answers)
    out_path = Path(output_dir) / phase / f"{document_id}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    document_writer.write(out_path, content)

    doc.written = True
    session.save(session_path)

    return {
        "written": True,
        "path": str(out_path),
        "document_id": document_id,
    }
