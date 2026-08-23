"""Tool: get_progress — return current phase/document/gate position."""

from __future__ import annotations

from typing import Any

from agent.lifecycle.state import SessionState


def get_progress(session: SessionState) -> dict[str, Any]:
    """Return a snapshot of current progress. Does not modify session state."""
    doc = session.documents.get(session.current_document)
    answered = sum(
        1 for gs in (doc.gates.values() if doc else []) if gs.answer is not None
    )
    return {
        "current_phase": session.current_phase,
        "current_document": session.current_document,
        "answered_gates": answered,
        "project_name": session.project_name,
    }
