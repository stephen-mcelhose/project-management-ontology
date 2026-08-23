"""Tool: get_next_gate — return next unfilled required gate for a document."""

from __future__ import annotations

from typing import Any, Protocol

from agent.lifecycle.gates import Gate, next_unfilled_required
from agent.lifecycle.state import SessionState


class GateReaderProtocol(Protocol):
    def load_gates(self, doc_dir: str) -> list[Gate]: ...


def get_next_gate(
    session: SessionState,
    document_id: str,
    templates_dir: str,
    gate_reader: GateReaderProtocol,
) -> dict[str, Any] | None:
    """Return the next unfilled required gate, or None if all required are done.

    Does not modify session state.
    """
    doc = session.documents.get(document_id)
    answers = {gid: gs.answer for gid, gs in doc.gates.items() if gs.answer is not None} if doc else {}

    doc_dir = f"{templates_dir}/{session.current_phase}/{document_id}"
    gates = gate_reader.load_gates(doc_dir)
    gate = next_unfilled_required(gates, answers)
    if gate is None:
        return None
    return {
        "id": gate.id,
        "prompt": gate.prompt,
        "fills": gate.fills,
        "maps_to": gate.maps_to,
        "type": gate.type,
        "required": gate.required,
        "validation": gate.validation,
        "guidance": gate.guidance,
    }
