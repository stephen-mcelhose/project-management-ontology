"""Concrete GateReader — loads gates from the real filesystem."""

from __future__ import annotations

from agent.lifecycle.gates import Gate, load_gates


class FileGateReader:
    """Loads gates from instructions.yaml on the real filesystem."""

    def load_gates(self, doc_dir: str) -> list[Gate]:
        return load_gates(doc_dir)
