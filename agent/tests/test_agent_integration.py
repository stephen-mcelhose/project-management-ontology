"""Integration tests: full tool pipeline + ADK InMemoryRunner with scripted model.

These tests exercise the complete stack:
  Session ↔ Lifecycle modules ↔ Tools ↔ Filesystem

No real LLM calls. No network.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import AsyncGenerator

import pytest
import yaml

from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.adk.models.registry import LLMRegistry
from google.genai import types

from agent.agent import build_agent, build_runner
from agent.lifecycle.gates import Gate
from agent.lifecycle.state import DocumentState, GateState, SessionState
from agent.lifecycle.validator import ValidationResult
from agent.tools.get_next_gate import get_next_gate
from agent.tools.get_progress import get_progress
from agent.tools.record_answer import record_answer
from agent.tools.validate_document import validate_document
from agent.tools.write_document import write_document


# ── Fakes ─────────────────────────────────────────────────────────────────────


class FakeGateReader:
    def __init__(self, gates):
        self._gates = gates

    def load_gates(self, doc_dir: str) -> list[Gate]:
        return self._gates


class FakeDocumentWriter:
    def __init__(self, template_text):
        self._template = template_text
        self.written: dict[str, str] = {}

    def read_template(self, doc_dir: str) -> str:
        return self._template

    def write(self, path: Path, content: str) -> None:
        self.written[str(path)] = content

    def shape_path(self, templates_dir: str, phase: str, doc_id: str) -> Path:
        return Path("/shapes") / phase / f"{doc_id}.shacl.ttl"

    def doc_dir(self, templates_dir: str, phase: str, doc_id: str) -> str:
        return f"{templates_dir}/{phase}/{doc_id}"


class FakeValidator:
    def __init__(self, passed=True):
        self._result = ValidationResult(passed=passed)

    def validate(self, document_path, shape_path):
        return self._result


def _gates():
    return [
        Gate(id="project_name", order=1, type="prose", prompt="Project name?",
             fills="## Project Name", required=True),
        Gate(id="problem", order=2, type="prose", prompt="Problem?",
             fills="## Problem", required=True),
        Gate(id="optional_note", order=3, type="prose", prompt="Optional note?",
             fills="## Optional Note", required=False),
    ]


# ── Test 1: Fresh session — full tool pipeline ────────────────────────────────


class TestFreshSessionToolPipeline:
    """Walk the full tool pipeline for a fresh session, no LLM."""

    def test_full_gate_walk_then_write_and_validate(self, tmp_path):
        session_path = tmp_path / ".session.json"
        session = SessionState(
            project_name="Acme Project",
            current_phase="initiation",
            current_document="proposal",
        )
        gates = _gates()
        reader = FakeGateReader(gates)
        template = "# {{project_name}}\n\n{{problem}}\n\n{{optional_note}}"
        writer = FakeDocumentWriter(template_text=template)
        validator = FakeValidator(passed=True)

        # 1. get_progress — no gates answered yet
        progress = get_progress(session)
        assert progress["current_phase"] == "initiation"
        assert progress["answered_gates"] == 0

        # 2. get_next_gate — first is project_name
        gate = get_next_gate(
            session=session, document_id="proposal",
            templates_dir="/fake", gate_reader=reader,
        )
        assert gate is not None
        assert gate["id"] == "project_name"

        # 3. record_answer for project_name
        result = record_answer(
            session=session, session_path=session_path, document_id="proposal",
            gate_id="project_name", answer="Acme Modernisation",
            templates_dir="/fake", gate_reader=reader,
        )
        assert result["recorded"] is True
        assert result["all_required_complete"] is False
        assert session_path.exists()

        # 4. Next gate is problem
        gate = get_next_gate(
            session=session, document_id="proposal",
            templates_dir="/fake", gate_reader=reader,
        )
        assert gate["id"] == "problem"

        # 5. record_answer for problem — now all required done
        result = record_answer(
            session=session, session_path=session_path, document_id="proposal",
            gate_id="problem", answer="Legacy system is slow.",
            templates_dir="/fake", gate_reader=reader,
        )
        assert result["all_required_complete"] is True

        # 6. get_next_gate now returns None (optional gate not counted as required)
        gate = get_next_gate(
            session=session, document_id="proposal",
            templates_dir="/fake", gate_reader=reader,
        )
        assert gate is None

        # 7. write_document
        write_result = write_document(
            session=session, session_path=session_path, document_id="proposal",
            templates_dir="/fake", output_dir=str(tmp_path / "output"),
            gate_reader=reader, document_writer=writer,
        )
        assert write_result["written"] is True
        assert len(writer.written) == 1
        content = list(writer.written.values())[0]
        assert "Acme Modernisation" in content
        assert "Legacy system is slow." in content
        assert "{{" not in content  # no leftover placeholders
        assert session.documents["proposal"].written is True

        # 8. validate_document
        val_result = validate_document(
            session=session, session_path=session_path, document_id="proposal",
            templates_dir="/fake", output_dir=str(tmp_path / "output"),
            validator=validator,
        )
        assert val_result["passed"] is True
        assert session.documents["proposal"].valid is True

        # 9. session file reflects final state
        loaded = SessionState.load(session_path)
        assert loaded.documents["proposal"].written is True
        assert loaded.documents["proposal"].valid is True
        assert loaded.documents["proposal"].gates["project_name"].answer == "Acme Modernisation"


# ── Test 2: Resume session ────────────────────────────────────────────────────


class TestResumeSession:
    """Load a pre-populated session and verify the agent skips completed gates."""

    def test_resumes_at_correct_gate(self, tmp_path):
        session_path = tmp_path / ".session.json"

        # Pre-populate: project_name is answered, problem is not
        pre_session = SessionState(
            project_name="Resume Test",
            current_phase="initiation",
            current_document="proposal",
        )
        pre_session.document("proposal").gates["project_name"] = GateState(
            gate_id="project_name", answer="Already answered"
        )
        pre_session.save(session_path)

        # Load the session as the agent would
        session = SessionState.load(session_path)
        assert session.project_name == "Resume Test"

        gates = _gates()
        reader = FakeGateReader(gates)

        # Agent should find 'problem' as next gate (project_name already answered)
        gate = get_next_gate(
            session=session, document_id="proposal",
            templates_dir="/fake", gate_reader=reader,
        )
        assert gate is not None
        assert gate["id"] == "problem"

        # Progress shows one gate already answered
        progress = get_progress(session)
        assert progress["answered_gates"] == 1

    def test_all_done_returns_none(self, tmp_path):
        session_path = tmp_path / ".session.json"

        pre_session = SessionState(
            project_name="Done Test",
            current_phase="initiation",
            current_document="proposal",
        )
        for gate in _gates():
            if gate.required:
                pre_session.document("proposal").gates[gate.id] = GateState(
                    gate_id=gate.id, answer="answered"
                )
        pre_session.save(session_path)

        session = SessionState.load(session_path)
        reader = FakeGateReader(_gates())
        gate = get_next_gate(
            session=session, document_id="proposal",
            templates_dir="/fake", gate_reader=reader,
        )
        assert gate is None


# ── Test 3: Runner construction ───────────────────────────────────────────────


class TestRunnerConstruction:
    """Verify the ADK runner builds and creates sessions without error."""

    def test_runner_creates_session(self, tmp_path):
        session = SessionState(
            project_name="Runner Test",
            current_phase="initiation",
            current_document="proposal",
        )
        agent = build_agent(
            session=session,
            session_path=tmp_path / ".session.json",
            templates_dir="templates/",
            output_dir=str(tmp_path / "output"),
            model="gemini-2.0-flash",
            gate_reader=FakeGateReader(_gates()),
            document_writer=FakeDocumentWriter("# {{project_name}}"),
            validator=FakeValidator(),
        )
        runner = build_runner(agent)

        adk_session = asyncio.run(
            runner.session_service.create_session(
                app_name=runner.app_name, user_id="test-user"
            )
        )
        assert adk_session is not None
        assert adk_session.id is not None
