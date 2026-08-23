"""Load gate sequences from instructions.yaml."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class Gate:
    id: str
    order: int
    type: str
    prompt: str
    fills: str
    required: bool
    maps_to: str | None = None
    validation: str | None = None
    guidance: str | None = None
    validation_rules: dict[str, Any] = field(default_factory=dict)
    deferred_value: str | None = None


def load_gates(document_dir: str) -> list[Gate]:
    """Load and sort gates from {document_dir}/instructions.yaml.

    Raises FileNotFoundError with the expected path if the file is missing.
    """
    path = Path(document_dir) / "instructions.yaml"
    if not path.exists():
        raise FileNotFoundError(f"instructions.yaml not found: {path}")

    with path.open() as f:
        data = yaml.safe_load(f)

    gates = [
        Gate(
            id=g["id"],
            order=g["order"],
            type=g.get("type", "prose"),
            prompt=g["prompt"],
            fills=g.get("fills", ""),
            required=g.get("required", True),
            maps_to=g.get("maps_to"),
            validation=g.get("validation"),
            guidance=g.get("guidance"),
            validation_rules=g.get("validation_rules", {}),
            deferred_value=g.get("deferred_value"),
        )
        for g in data.get("gates", [])
    ]
    return sorted(gates, key=lambda g: g.order)


def next_unfilled_required(gates: list[Gate], answers: dict[str, str]) -> Gate | None:
    """Return the next required gate with no recorded answer, or None if all done."""
    for gate in gates:
        if gate.required and gate.id not in answers:
            return gate
    return None
