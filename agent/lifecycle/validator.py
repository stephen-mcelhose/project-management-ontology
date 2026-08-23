"""SHACL validation wrapper around pyshacl.

Returns ValidationResult — never raises on validation failure.
Failure details are data, not exceptions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ValidationResult:
    passed: bool
    messages: list[str] = field(default_factory=list)


def validate(document_path: Path, shape_path: Path) -> ValidationResult:
    """Run pyshacl against document_path using shape_path.

    Returns ValidationResult(passed, messages).
    Never raises — all failures are returned as data.
    """
    if not shape_path.exists():
        return ValidationResult(
            passed=False,
            messages=[f"Shape file not found: {shape_path}"],
        )
    if not document_path.exists():
        return ValidationResult(
            passed=False,
            messages=[f"Document file not found: {document_path}"],
        )
    try:
        import pyshacl  # noqa: PLC0415

        conforms, _, results_text = pyshacl.validate(
            str(document_path),
            shacl_graph=str(shape_path),
            inference="rdfs",
            serialize_report_graph=False,
        )
        if conforms:
            return ValidationResult(passed=True)
        # Extract human-readable violation messages from the results text
        lines = [
            line.strip()
            for line in results_text.splitlines()
            if line.strip() and not line.startswith("@")
        ]
        return ValidationResult(passed=False, messages=lines or [results_text])
    except Exception as exc:
        return ValidationResult(passed=False, messages=[str(exc)])
