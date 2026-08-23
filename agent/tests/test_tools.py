"""Tests for agent/tools/*.py — Protocol-based fakes, no filesystem or LLM."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest

from agent.lifecycle.gates import Gate
from agent.lifecycle.state import DocumentState, GateState, SessionState
from agent.lifecycle.validator import ValidationResult
from agent.tools.get_next_gate import get_next_gate
from agent.tools.get_progress import get_progress
from agent.tools.record_answer import record_answer
from agent.tools.validate_document import validate_document
from agent.tools.write_document import write_document


# ── Fakes ─────────────────────────────────────────────────────────────────────


def _gate(id, order=1, required=True):
    return Gate(id=id, order=order, type="prose", prompt=f"{id}?",
                fills=f"## {id}", required=required)


def _session(phase="initiation", doc="proposal") -> SessionState:
    return SessionState(project_name="Test", current_phase=phase, current_document=doc)


class FakeGateReader:
    def __init__(self, gates):
        self._gates = gates

    def load_gates(self, doc_dir: str) -> list[Gate]:
        return self._gates


class FakeValidator:
    def __init__(self, passed=True, messages=None):
        self._result = ValidationResult(passed=passed, messages=messages or [])

    def validate(self, document_path: Path, shape_path: Path) -> ValidationResult:
        return self._result


class FakeDocumentWriter:
    def __init__(self, template_text="## {{gate_id}}\n{{gate_id}}"):
        self._template = template_text
        self.written: dict[str, str] = {}

    def read_template(self, doc_dir: str) -> str:
        return self._template

    def write(self, path: Path, content: str) -> None:
        self.written[str(path)] = content

    def shape_path(self, templates_dir: str, phase: str, doc_id: str) -> Path:
        return Path(templates_dir) / "shapes" / phase / f"{doc_id}.shacl.ttl"

    def doc_dir(self, templates_dir: str, phase: str, doc_id: str) -> str:
        return str(Path(templates_dir) / phase / doc_id)


# ── get_progress ──────────────────────────────────────────────────────────────


class TestGetProgress:
    def test_returns_current_position(self):
        session = _session(phase="initiation", doc="proposal")
        result = get_progress(session)
        assert result["current_phase"] == "initiation"
        assert result["current_document"] == "proposal"

    def test_does_not_modify_session(self):
        session = _session()
        import copy
        before = copy.deepcopy(session)
        get_progress(session)
        assert session.current_phase == before.current_phase
        assert session.documents == before.documents

    def test_counts_answered_gates(self):
        session = _session()
        session.document("proposal").gates["a"] = GateState(gate_id="a", answer="yes")
        session.document("proposal").gates["b"] = GateState(gate_id="b", answer=None)
        result = get_progress(session)
        assert result["answered_gates"] == 1


# ── get_next_gate ─────────────────────────────────────────────────────────────


class TestGetNextGate:
    def test_returns_first_unanswered_required(self):
        gates = [_gate("a", 1), _gate("b", 2)]
        session = _session()
        session.document("proposal").gates["a"] = GateState(gate_id="a", answer="yes")
        reader = FakeGateReader(gates)
        result = get_next_gate(
            session=session,
            document_id="proposal",
            templates_dir="/fake",
            gate_reader=reader,
        )
        assert result is not None
        assert result["id"] == "b"

    def test_returns_none_when_all_done(self):
        gates = [_gate("a", 1), _gate("b", 2)]
        session = _session()
        session.document("proposal").gates["a"] = GateState(gate_id="a", answer="yes")
        session.document("proposal").gates["b"] = GateState(gate_id="b", answer="yes")
        reader = FakeGateReader(gates)
        result = get_next_gate(
            session=session,
            document_id="proposal",
            templates_dir="/fake",
            gate_reader=reader,
        )
        assert result is None

    def test_does_not_modify_session(self):
        gates = [_gate("a", 1)]
        session = _session()
        reader = FakeGateReader(gates)
        get_next_gate(session=session, document_id="proposal",
                      templates_dir="/fake", gate_reader=reader)
        assert "a" not in session.document("proposal").gates


# ── record_answer ─────────────────────────────────────────────────────────────


class TestRecordAnswer:
    def test_persists_answer(self, tmp_path):
        session = _session()
        session_path = tmp_path / ".session.json"
        gates = [_gate("a", 1), _gate("b", 2)]
        reader = FakeGateReader(gates)
        result = record_answer(
            session=session,
            session_path=session_path,
            document_id="proposal",
            gate_id="a",
            answer="My answer",
            templates_dir="/fake",
            gate_reader=reader,
        )
        assert result["recorded"] is True
        assert session.document("proposal").gates["a"].answer == "My answer"
        assert session_path.exists()  # written to disk

    def test_idempotent_overwrites_previous_answer(self, tmp_path):
        session = _session()
        session_path = tmp_path / ".session.json"
        gates = [_gate("a", 1)]
        reader = FakeGateReader(gates)
        record_answer(session=session, session_path=session_path, document_id="proposal",
                      gate_id="a", answer="first", templates_dir="/fake", gate_reader=reader)
        record_answer(session=session, session_path=session_path, document_id="proposal",
                      gate_id="a", answer="second", templates_dir="/fake", gate_reader=reader)
        assert session.document("proposal").gates["a"].answer == "second"

    def test_unknown_gate_id_returns_error(self, tmp_path):
        session = _session()
        session_path = tmp_path / ".session.json"
        gates = [_gate("a", 1)]
        reader = FakeGateReader(gates)
        result = record_answer(
            session=session, session_path=session_path, document_id="proposal",
            gate_id="unknown_gate", answer="x", templates_dir="/fake", gate_reader=reader,
        )
        assert result["recorded"] is False
        assert "error" in result

    def test_returns_all_complete_flag(self, tmp_path):
        session = _session()
        session_path = tmp_path / ".session.json"
        gates = [_gate("a", 1)]
        reader = FakeGateReader(gates)
        result = record_answer(
            session=session, session_path=session_path, document_id="proposal",
            gate_id="a", answer="done", templates_dir="/fake", gate_reader=reader,
        )
        assert result["all_required_complete"] is True


# ── write_document ────────────────────────────────────────────────────────────


class TestWriteDocument:
    def test_writes_rendered_content(self, tmp_path):
        session = _session()
        session_path = tmp_path / ".session.json"
        session.document("proposal").gates["name"] = GateState(gate_id="name", answer="Acme")
        writer = FakeDocumentWriter(template_text="# {{name}}")
        gates = [_gate("name", 1)]
        reader = FakeGateReader(gates)
        result = write_document(
            session=session, session_path=session_path, document_id="proposal",
            templates_dir="/fake", output_dir=str(tmp_path / "output"),
            gate_reader=reader, document_writer=writer,
        )
        assert result["written"] is True
        written_content = list(writer.written.values())[0]
        assert "Acme" in written_content

    def test_missing_required_gate_returns_error(self, tmp_path):
        session = _session()
        session_path = tmp_path / ".session.json"
        writer = FakeDocumentWriter(template_text="# {{name}}")
        gates = [_gate("name", 1, required=True)]
        reader = FakeGateReader(gates)
        result = write_document(
            session=session, session_path=session_path, document_id="proposal",
            templates_dir="/fake", output_dir=str(tmp_path / "output"),
            gate_reader=reader, document_writer=writer,
        )
        assert result["written"] is False
        assert "error" in result
        # No file written
        assert writer.written == {}

    def test_idempotent_second_write_overwrites(self, tmp_path):
        session = _session()
        session_path = tmp_path / ".session.json"
        session.document("proposal").gates["name"] = GateState(gate_id="name", answer="V1")
        writer = FakeDocumentWriter(template_text="# {{name}}")
        gates = [_gate("name", 1)]
        reader = FakeGateReader(gates)
        write_document(session=session, session_path=session_path, document_id="proposal",
                       templates_dir="/fake", output_dir=str(tmp_path / "output"),
                       gate_reader=reader, document_writer=writer)
        session.document("proposal").gates["name"].answer = "V2"
        write_document(session=session, session_path=session_path, document_id="proposal",
                       templates_dir="/fake", output_dir=str(tmp_path / "output"),
                       gate_reader=reader, document_writer=writer)
        written_content = list(writer.written.values())[-1]
        assert "V2" in written_content


# ── validate_document ─────────────────────────────────────────────────────────


class TestValidateDocument:
    def test_passed_updates_session_valid_true(self, tmp_path):
        session = _session()
        session_path = tmp_path / ".session.json"
        session.document("proposal").written = True
        validator = FakeValidator(passed=True)
        result = validate_document(
            session=session, session_path=session_path, document_id="proposal",
            templates_dir="/fake", output_dir=str(tmp_path / "output"),
            validator=validator,
        )
        assert result["passed"] is True
        assert session.document("proposal").valid is True

    def test_failure_updates_session_valid_false(self, tmp_path):
        session = _session()
        session_path = tmp_path / ".session.json"
        session.document("proposal").written = True
        validator = FakeValidator(passed=False, messages=["Missing required property"])
        result = validate_document(
            session=session, session_path=session_path, document_id="proposal",
            templates_dir="/fake", output_dir=str(tmp_path / "output"),
            validator=validator,
        )
        assert result["passed"] is False
        assert "Missing required property" in result["messages"]
        assert session.document("proposal").valid is False

    def test_failure_is_data_not_exception(self, tmp_path):
        session = _session()
        session_path = tmp_path / ".session.json"
        validator = FakeValidator(passed=False, messages=["Violation"])
        result = validate_document(
            session=session, session_path=session_path, document_id="proposal",
            templates_dir="/fake", output_dir=str(tmp_path / "output"),
            validator=validator,
        )
        assert isinstance(result, dict)
