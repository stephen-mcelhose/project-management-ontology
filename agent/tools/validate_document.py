"""Tool: validate_document — run SHACL validation on a written document."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol

from agent.lifecycle.state import SessionState
from agent.lifecycle.validator import ValidationResult


class ValidatorProtocol(Protocol):
    def validate(self, document_path: Path, shape_path: Path) -> ValidationResult: ...


def validate_document(
    session: SessionState,
    session_path: Path,
    document_id: str,
    templates_dir: str,
    output_dir: str,
    validator: ValidatorProtocol,
) -> dict[str, Any]:
    """Validate {output_dir}/{phase}/{document_id}.md against its SHACL shape.

    Updates DocumentState.valid in session and writes to disk.
    Returns {passed, messages} — never raises.
    """
    phase = session.current_phase
    doc_path = Path(output_dir) / phase / f"{document_id}.md"
    # shapes/ is a sibling of templates/ inside the domain pack, not a child.
    shape_path = Path(templates_dir).parent / "shapes" / phase / f"{document_id}.shacl.ttl"

    result = validator.validate(doc_path, shape_path)

    doc = session.document(document_id)
    doc.valid = result.passed
    session.save(session_path)

    return {
        "passed": result.passed,
        "messages": result.messages,
        "document_id": document_id,
    }
