"""Tests for agent/lifecycle/gates.py."""

import pytest
import yaml

from agent.lifecycle.gates import Gate, load_gates, next_unfilled_required


# ── Helpers ───────────────────────────────────────────────────────────────────


def write_instructions(doc_dir, gates_data):
    doc_dir.mkdir(parents=True, exist_ok=True)
    data = {
        "version": 1,
        "document": doc_dir.name,
        "gates": gates_data,
        "completion": {"required_gates": [g["id"] for g in gates_data if g.get("required")]},
    }
    (doc_dir / "instructions.yaml").write_text(yaml.dump(data))


@pytest.fixture()
def doc_dir(tmp_path):
    d = tmp_path / "templates" / "initiation" / "proposal"
    return d


# ── load_gates ────────────────────────────────────────────────────────────────


class TestLoadGates:
    def test_sorted_by_order(self, doc_dir):
        write_instructions(doc_dir, [
            {"id": "c", "order": 3, "type": "prose", "prompt": "C?", "fills": "## C", "required": True},
            {"id": "a", "order": 1, "type": "prose", "prompt": "A?", "fills": "## A", "required": True},
            {"id": "b", "order": 2, "type": "list",  "prompt": "B?", "fills": "## B", "required": True},
        ])
        gates = load_gates(str(doc_dir))
        assert [g.id for g in gates] == ["a", "b", "c"]

    def test_optional_gates_included(self, doc_dir):
        write_instructions(doc_dir, [
            {"id": "req", "order": 1, "type": "prose", "prompt": "R?", "fills": "## R", "required": True},
            {"id": "opt", "order": 2, "type": "prose", "prompt": "O?", "fills": "## O", "required": False},
        ])
        gates = load_gates(str(doc_dir))
        ids = [g.id for g in gates]
        assert "opt" in ids
        assert "req" in ids

    def test_returns_gate_dataclass(self, doc_dir):
        write_instructions(doc_dir, [
            {"id": "name", "order": 1, "type": "prose", "prompt": "Name?",
             "fills": "## Name", "maps_to": "dct:title", "required": True,
             "validation": "Must be a noun.", "guidance": "Be specific."},
        ])
        gates = load_gates(str(doc_dir))
        g = gates[0]
        assert isinstance(g, Gate)
        assert g.id == "name"
        assert g.maps_to == "dct:title"
        assert g.validation == "Must be a noun."
        assert g.guidance == "Be specific."

    def test_optional_fields_default_to_none(self, doc_dir):
        write_instructions(doc_dir, [
            {"id": "x", "order": 1, "type": "prose", "prompt": "X?", "fills": "## X", "required": True},
        ])
        g = load_gates(str(doc_dir))[0]
        assert g.maps_to is None
        assert g.validation is None
        assert g.guidance is None
        assert g.validation_rules == {}

    def test_missing_file_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError, match="instructions.yaml"):
            load_gates(str(tmp_path / "nonexistent"))


# ── next_unfilled_required ────────────────────────────────────────────────────


class TestNextUnfilledRequired:
    def _gates(self):
        return [
            Gate(id="a", order=1, type="prose", prompt="A?", fills="## A", required=True),
            Gate(id="b", order=2, type="prose", prompt="B?", fills="## B", required=True),
            Gate(id="c", order=3, type="prose", prompt="C?", fills="## C", required=False),
            Gate(id="d", order=4, type="prose", prompt="D?", fills="## D", required=True),
        ]

    def test_returns_first_unanswered_required(self):
        gates = self._gates()
        result = next_unfilled_required(gates, answers={"a": "answer-a"})
        assert result is not None
        assert result.id == "b"

    def test_returns_none_when_all_required_answered(self):
        gates = self._gates()
        answers = {"a": "x", "b": "y", "d": "z"}
        assert next_unfilled_required(gates, answers) is None

    def test_skips_optional_gaps(self):
        gates = self._gates()
        # a, b answered; c is optional (unanswered); d is next required
        answers = {"a": "x", "b": "y"}
        result = next_unfilled_required(gates, answers)
        assert result is not None
        assert result.id == "d"

    def test_no_answers_returns_first_required(self):
        gates = self._gates()
        result = next_unfilled_required(gates, answers={})
        assert result is not None
        assert result.id == "a"

    def test_empty_gates_returns_none(self):
        assert next_unfilled_required([], answers={}) is None
