"""Tests for agent/lifecycle/state.py."""

import json
from pathlib import Path

import pytest

from agent.lifecycle.state import DocumentState, GateState, SessionState


@pytest.fixture()
def session_path(tmp_path):
    return tmp_path / ".session.json"


class TestLoadMissing:
    def test_missing_file_returns_fresh_state(self, session_path):
        s = SessionState.load(session_path)
        assert isinstance(s, SessionState)
        assert s.documents == {}
        assert s.shared_context == {}


class TestSaveAndReload:
    def test_roundtrip(self, session_path):
        s = SessionState(
            project_name="Test Project",
            current_phase="initiation",
            current_document="proposal",
        )
        s.document("proposal").gates["project_name"] = GateState(
            gate_id="project_name", answer="My Project"
        )
        s.save(session_path)

        loaded = SessionState.load(session_path)
        assert loaded.project_name == "Test Project"
        assert loaded.current_phase == "initiation"
        gate = loaded.documents["proposal"].gates["project_name"]
        assert gate.answer == "My Project"

    def test_save_creates_parent_dirs(self, tmp_path):
        path = tmp_path / "deep" / "nested" / ".session.json"
        s = SessionState(project_name="P", current_phase="initiation", current_document="d")
        s.save(path)
        assert path.exists()


class TestAtomicWrite:
    def test_no_partial_write_visible(self, session_path):
        """Write to tmp file then rename — the file either exists complete or not at all."""
        s = SessionState(project_name="A", current_phase="initiation", current_document="d")
        s.save(session_path)
        # After save, path should be the final file (not a .tmp)
        assert session_path.exists()
        tmp_path = session_path.with_suffix(".tmp")
        assert not tmp_path.exists()


class TestDocumentAccessor:
    def test_creates_document_on_first_access(self, session_path):
        s = SessionState.load(session_path)
        doc = s.document("proposal")
        assert isinstance(doc, DocumentState)
        assert "proposal" in s.documents

    def test_returns_same_instance_on_second_access(self, session_path):
        s = SessionState.load(session_path)
        doc1 = s.document("proposal")
        doc2 = s.document("proposal")
        assert doc1 is doc2


class TestIsDocumentComplete:
    def test_false_when_required_gate_missing(self):
        s = SessionState(project_name="P", current_phase="init", current_document="d")
        s.document("d").gates["g1"] = GateState(gate_id="g1", answer="yes")
        assert not s.is_document_complete("d", required_gate_ids=["g1", "g2"])

    def test_true_when_all_required_answered(self):
        s = SessionState(project_name="P", current_phase="init", current_document="d")
        s.document("d").gates["g1"] = GateState(gate_id="g1", answer="yes")
        s.document("d").gates["g2"] = GateState(gate_id="g2", answer="no")
        assert s.is_document_complete("d", required_gate_ids=["g1", "g2"])

    def test_false_when_answer_is_none(self):
        s = SessionState(project_name="P", current_phase="init", current_document="d")
        s.document("d").gates["g1"] = GateState(gate_id="g1", answer=None)
        assert not s.is_document_complete("d", required_gate_ids=["g1"])


class TestIsPhaseComplete:
    def _make_manifest(self, required_ids):
        class FakeManifest:
            completion = {"required_documents": required_ids}
        return FakeManifest()

    def test_false_when_document_not_written(self):
        s = SessionState(project_name="P", current_phase="init", current_document="d")
        s.document("d").written = False
        s.document("d").valid = True
        manifest = self._make_manifest(["d"])
        assert not s.is_phase_complete(manifest)

    def test_false_when_document_not_valid(self):
        s = SessionState(project_name="P", current_phase="init", current_document="d")
        s.document("d").written = True
        s.document("d").valid = False
        manifest = self._make_manifest(["d"])
        assert not s.is_phase_complete(manifest)

    def test_true_when_all_required_written_and_valid(self):
        s = SessionState(project_name="P", current_phase="init", current_document="d")
        s.document("d").written = True
        s.document("d").valid = True
        manifest = self._make_manifest(["d"])
        assert s.is_phase_complete(manifest)
