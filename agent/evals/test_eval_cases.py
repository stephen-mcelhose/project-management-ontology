"""Eval tests — parametrised over every YAML case in agent/evals/cases/.

Default (no flags): scripted/deterministic model.
  Cases with ``scripted_responses`` run without any network call.
  Cases without ``scripted_responses`` are skipped with a clear message.

With --run-evals: real model from Settings (requires Vertex AI credentials).
  All cases run. Cases without scripted_responses are exercised for the first time.
"""

from __future__ import annotations

import asyncio
from pathlib import Path

import pytest
from google.adk.models.registry import LLMRegistry

from agent.agent import build_agent, build_runner
from agent.evals.runner import EvalCase, is_subsequence, run_case
from agent.evals.scripted_model import ScriptedModel
from agent.lifecycle.state import SessionState

LLMRegistry.register(ScriptedModel)

CASES_DIR = Path(__file__).parent / "cases"
_CASE_PATHS = sorted(CASES_DIR.glob("*.yaml"))


@pytest.fixture(params=_CASE_PATHS, ids=[p.stem for p in _CASE_PATHS])
def case_path(request):
    return request.param


def test_eval_case(case_path, request, tmp_path):
    use_real = request.config.getoption("--run-evals", default=False)
    case = EvalCase.load(case_path)

    # Skip cases whose document path doesn't exist in templates (e.g. minimal-walk
    # which uses a fake document and is covered by test_agent_loop.py instead).
    template_path = Path("templates") / case.phase / case.document / "instructions.yaml"
    if not template_path.exists():
        pytest.skip(f"No real template at {template_path} — unit-test fixture only")

    if use_real:
        from agent.settings import Settings
        model = Settings().model
    else:
        if not case.scripted_responses:
            pytest.skip(
                f"{case_path.name} has no scripted_responses — pass --run-evals to run against the real model"
            )
        ScriptedModel.load(case.build_scripted_responses())
        model = "scripted-fake"

    session_path = tmp_path / ".session.json"
    session = SessionState(
        current_phase=case.phase,
        current_document=case.document,
    )

    agent = build_agent(
        session=session,
        session_path=session_path,
        templates_dir="templates/",
        output_dir=str(tmp_path),
        model=model,
    )
    runner = build_runner(agent)

    result = asyncio.run(
        run_case(case, agent, runner, session, session_path, str(tmp_path))
    )

    # Tool call sequence
    assert is_subsequence(case.expect_tool_calls, result.tool_calls_seen), (
        f"Expected tool call subsequence: {case.expect_tool_calls}\n"
        f"Got: {result.tool_calls_seen}"
    )

    # Gate answers — doc_id → gate_id → expected value.
    # Failure here means capture broke (agent dropped or mis-routed the answer).
    # If this passes but content_contains fails, the template/renderer is the culprit.
    for doc_id, gates in case.expect_gate_answers.items():
        for gate_id, expected in gates.items():
            actual = result.gate_answers.get(doc_id, {}).get(gate_id)
            assert actual == expected, (
                f"Gate '{doc_id}.{gate_id}': expected {expected!r}, got {actual!r}\n"
                f"Recorded gates for '{doc_id}': {list(result.gate_answers.get(doc_id, {}))}"
            )

    # Document written
    if case.expect_document_written:
        assert result.document_written, (
            f"Expected {case.phase}/{case.document}.md to exist in {tmp_path}"
        )

    # Rendered content
    for needle, present in result.content_checks.items():
        assert present, f"Expected '{needle}' in written document"
