"""Integration test: full agent loop via InMemoryRunner + ScriptedModel.

Exercises the complete stack end-to-end:
  User message → LlmAgent → ScriptedModel → FunctionCall → tool executed
  → result fed back → model called again → ... → final text event

Uses minimal-walk.yaml as the case definition. The same runner.py harness
will drive real evals (#67) against a live model.

No real LLM calls. No network.
"""

from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from google.adk.models.registry import LLMRegistry

from agent.agent import build_agent, build_runner
from agent.evals.runner import EvalCase, run_case, is_subsequence
from agent.evals.scripted_model import ScriptedModel
from agent.lifecycle.gates import Gate
from agent.lifecycle.state import SessionState
from agent.lifecycle.validator import ValidationResult

# Register ScriptedModel once for the test session
LLMRegistry.register(ScriptedModel)

CASES_DIR = Path(__file__).parent.parent / "evals" / "cases"
MINIMAL_WALK = CASES_DIR / "minimal-walk.yaml"


# ── Fakes matching the minimal-walk.yaml gates ────────────────────────────────


def _gates():
    return [
        Gate(id="name", order=1, type="prose", prompt="What is the project name?",
             fills="## Name", required=True),
        Gate(id="summary", order=2, type="prose", prompt="What is the project summary?",
             fills="## Summary", required=True),
    ]


class FakeGateReader:
    def load_gates(self, doc_dir: str) -> list[Gate]:
        return _gates()


class FakeDocumentWriter:
    def __init__(self):
        self.written: dict[str, str] = {}

    def read_template(self, doc_dir: str) -> str:
        return "# {{name}}\n\n{{summary}}"

    def write(self, path: Path, content: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        self.written[str(path)] = content

    def shape_path(self, templates_dir: str, phase: str, doc_id: str) -> Path:
        return Path("/fake/shapes") / phase / f"{doc_id}.shacl.ttl"

    def doc_dir(self, templates_dir: str, phase: str, doc_id: str) -> str:
        return f"{templates_dir}/{phase}/{doc_id}"


class FakeValidator:
    def validate(self, document_path: Path, shape_path: Path) -> ValidationResult:
        return ValidationResult(passed=True)


# ── Test ──────────────────────────────────────────────────────────────────────


class TestAgentLoop:
    def test_minimal_walk(self, tmp_path):
        """Full runner.run() loop: 3 user turns, 2 gates, write, validate."""
        case = EvalCase.load(MINIMAL_WALK)
        ScriptedModel.load(case.build_scripted_responses())

        session_path = tmp_path / ".session.json"
        output_dir = str(tmp_path / "output")

        session = SessionState(
            project_name="",
            current_phase=case.phase,
            current_document=case.document,
        )

        writer = FakeDocumentWriter()
        agent = build_agent(
            session=session,
            session_path=session_path,
            templates_dir="templates/",
            output_dir=output_dir,
            model="scripted-fake",
            gate_reader=FakeGateReader(),
            document_writer=writer,
            validator=FakeValidator(),
        )
        runner = build_runner(agent)

        result = asyncio.run(
            run_case(case, agent, runner, session, session_path, output_dir)
        )

        # Tool call sequence contains expected tools in order
        assert is_subsequence(case.expect_tool_calls, result.tool_calls_seen), (
            f"Expected tool subsequence {case.expect_tool_calls}\n"
            f"Got: {result.tool_calls_seen}"
        )

        # Document was written to disk
        assert result.document_written, (
            f"Expected {case.document}.md to exist in {output_dir}"
        )

        # Written content reflects user's answers
        for needle, present in result.content_checks.items():
            assert present, f"Expected '{needle}' in written document"

        # Session state reflects completed document
        assert session.documents[case.document].written is True
        assert session.documents[case.document].valid is True
        assert session.documents[case.document].gates["name"].answer == "Acme Platform."
        assert session.documents[case.document].gates["summary"].answer == "Modernise the legacy ETL stack."

        # All scripted responses were consumed (no leftover)
        assert ScriptedModel.remaining() == 0, (
            f"{ScriptedModel.remaining()} scripted responses were not consumed"
        )

        # Agent produced at least one text event per turn
        assert len(result.text_events) >= len(case.turns)
