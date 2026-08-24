"""Eval tests — parametrised over every YAML case in agent/evals/cases/.

Default (no flags): scripted/deterministic model.
  Cases with ``scripted_responses`` run without any network call.
  Gate answer assertions use exact string match (responses are deterministic).
  Cases without ``scripted_responses`` are skipped with a clear message.

With --run-evals: real model from Settings (requires Vertex AI credentials).
  All cases run.
  Gate answer assertions use an LLM judge (semantic equivalence) instead of
  exact match — the real model always paraphrases free-text gates.
"""

from __future__ import annotations

import asyncio
from pathlib import Path

import pytest
from google.adk.models.registry import LLMRegistry

from agent.agent import build_agent, build_runner
from agent.evals.llm_judge import judge_gate_answer
from agent.evals.runner import EvalCase, is_subsequence, run_case
from agent.evals.scripted_model import ScriptedModel
from agent.lifecycle.gate_reader import FileGateReader
from agent.lifecycle.state import SessionState

LLMRegistry.register(ScriptedModel)

CASES_DIR = Path(__file__).parent / "cases"
TEMPLATES_DIR = Path("domains/pm/templates")
_CASE_PATHS = sorted(CASES_DIR.glob("*.yaml"))


@pytest.fixture(params=_CASE_PATHS, ids=[p.stem for p in _CASE_PATHS])
def case_path(request):
    return request.param


def _load_gate_prompts(phase: str) -> dict[str, dict[str, str]]:
    """Return {doc_id: {gate_id: prompt}} for all documents in the phase."""
    from agent.tools.get_phase_gates import get_phase_gates
    return get_phase_gates(phase=phase, templates_dir=str(TEMPLATES_DIR), gate_reader=FileGateReader())


def test_eval_case(case_path, request, tmp_path):
    use_real = request.config.getoption("--run-evals", default=False)
    case = EvalCase.load(case_path)

    # Skip cases whose document path doesn't exist in templates (e.g. minimal-walk
    # which uses a fake document and is covered by test_agent_loop.py instead).
    template_path = TEMPLATES_DIR / case.phase / case.document / "instructions.yaml"
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
        templates_dir=str(TEMPLATES_DIR) + "/",
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

    # Gate answer assertions.
    # Scripted mode: exact match (responses are deterministic).
    # Real-model mode: LLM judge (semantic equivalence handles paraphrase).
    if case.expect_gate_answers:
        phase_gates = _load_gate_prompts(case.phase) if use_real else {}

        for doc_id, gates in case.expect_gate_answers.items():
            for gate_id, expected in gates.items():
                actual = result.gate_answers.get(doc_id, {}).get(gate_id)

                if use_real:
                    prompt = phase_gates.get(doc_id, {}).get(gate_id, gate_id)
                    verdict = judge_gate_answer(
                        doc_id=doc_id,
                        gate_id=gate_id,
                        gate_prompt=prompt,
                        phase_gates=phase_gates,
                        user_turns=case.turns,
                        recorded_answer=actual,
                        model=model,
                    )
                    assert verdict.passed, (
                        f"Gate '{doc_id}.{gate_id}' failed judge: {verdict.reasoning}\n"
                        f"Recorded: {actual!r}"
                    )
                else:
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
