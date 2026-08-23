"""Tool: record_answer — persist a gate answer and advance completion state."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol

from agent.lifecycle.gates import Gate
from agent.lifecycle.state import GateState, SessionState


class GateReaderProtocol(Protocol):
    def load_gates(self, doc_dir: str) -> list[Gate]: ...


def record_answer(
    session: SessionState,
    session_path: Path,
    document_id: str,
    gate_id: str,
    answer: str,
    templates_dir: str,
    gate_reader: GateReaderProtocol,
) -> dict[str, Any]:
    """Record an answer for gate_id in document_id.

    Writes session to disk before returning.
    Idempotent: re-calling with the same gate_id overwrites the previous answer.
    Returns {recorded, all_required_complete} or {recorded: False, error}.
    """
    doc_dir = f"{templates_dir}/{session.current_phase}/{document_id}"
    gates = gate_reader.load_gates(doc_dir)
    gate_ids = {g.id for g in gates}

    if gate_id not in gate_ids:
        return {
            "recorded": False,
            "error": f"Gate '{gate_id}' does not exist in {document_id}. "
                     f"Valid gates: {sorted(gate_ids)}",
        }

    doc = session.document(document_id)
    doc.gates[gate_id] = GateState(gate_id=gate_id, answer=answer)
    session.save(session_path)

    required_ids = [g.id for g in gates if g.required]
    answers = {gid: gs.answer for gid, gs in doc.gates.items() if gs.answer is not None}
    all_done = all(rid in answers for rid in required_ids)

    return {
        "recorded": True,
        "gate_id": gate_id,
        "document_id": document_id,
        "all_required_complete": all_done,
    }
