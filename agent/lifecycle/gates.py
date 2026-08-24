"""Load gate sequences from instructions.yaml.

Ontology mapping
----------------
Gate is the Python representation of one entry in instructions.yaml.
Conceptually it corresponds to pm:WorkflowStep in the OWL model
(domains/pm/ontology/modules/workflow.ttl), but carries extra artifact-layer
fields (fills, guidance, deferred_value) that are template concerns,
not ontology concerns.

The maps_to field holds a CURIE (e.g. pm:hasSponsor, dct:title) that
names the OWL property the gate's answer is recorded against.
make validate-schemas checks every maps_to CURIE against the loaded
ontology graph — add that check to CI if you add new gates.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class Gate:
    # Ontology: pm:WorkflowStep (domains/pm/ontology/modules/workflow.ttl)
    id: str
    order: int
    type: str
    prompt: str
    fills: str
    required: bool
    maps_to: str | None = None      # CURIE — must resolve in ontology; see make validate-schemas
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


def next_unfilled_gate(gates: list[Gate], answers: dict[str, str]) -> Gate | None:
    """Return the next gate (required or optional) with no recorded answer.

    Gates are walked in order. Optional gates are asked just like required
    ones — the user can skip them, but any answer they volunteer is recorded.
    The required flag only controls whether the document can be written
    (required gates must be present; optional ones may be blank).
    """
    for gate in gates:
        if gate.id not in answers:
            return gate
    return None
