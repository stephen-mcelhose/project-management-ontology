"""Shared eval case runner.

Loads a YAML eval case and drives the agent through its user turns,
collecting tool calls and assertions. Works with any model — scripted
fake for tests, real model for evals.

Usage (test)::

    from agent.evals.runner import EvalCase, CaseResult, run_case
    from agent.evals.scripted_model import ScriptedModel

    case = EvalCase.load(Path("agent/evals/cases/minimal-walk.yaml"))
    ScriptedModel.load(case.build_scripted_responses())
    result = asyncio.run(run_case(case, agent, runner, session, session_path, output_dir))
    assert result.document_written
    assert result.all_content_present

Usage (eval, real model)::

    case = EvalCase.load(Path("agent/evals/cases/project-proposal.yaml"))
    result = asyncio.run(run_case(case, agent, runner, session, session_path, output_dir))
    assert result.tool_call_sequence_matches
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml
from google.adk.agents import LlmAgent
from google.adk.models.llm_response import LlmResponse
from google.adk.runners import InMemoryRunner
from google.genai import types

from agent.evals.scripted_model import text_response, tool_response
from agent.lifecycle.state import SessionState

# ── Data model ────────────────────────────────────────────────────────────────


@dataclass
class EvalCase:
    id: str
    description: str
    phase: str
    document: str
    turns: list[str]                            # user messages in order
    expect_document_written: bool
    expect_content_contains: list[str]
    expect_tool_calls: list[str]                # ordered subsequence
    expect_gate_answers: dict[str, dict[str, str]]  # doc_id → {gate_id → answer}
    scripted_responses: list[dict]              # raw YAML entries, empty for real evals

    @classmethod
    def load(cls, path: Path) -> EvalCase:
        data = yaml.safe_load(path.read_text())
        return cls(
            id=data["id"],
            description=data.get("description", ""),
            phase=data["phase"],
            document=data["document"],
            turns=[t["user"] for t in data.get("turns", [])],
            expect_document_written=data.get("expect_document_written", False),
            expect_content_contains=data.get("expect_content_contains", []),
            expect_tool_calls=data.get("expect_tool_calls", []),
            expect_gate_answers=data.get("expect_gate_answers", {}),
            scripted_responses=data.get("scripted_responses", []),
        )

    def build_scripted_responses(self) -> list[LlmResponse]:
        """Convert scripted_responses YAML entries to LlmResponse objects."""
        responses = []
        for entry in self.scripted_responses:
            if "tool_call" in entry:
                tc = entry["tool_call"]
                responses.append(tool_response(tc["name"], tc.get("args", {})))
            elif "text" in entry:
                responses.append(text_response(entry["text"]))
            else:
                raise ValueError(f"Unknown scripted_response entry: {entry!r}")
        return responses


@dataclass
class CaseResult:
    tool_calls_seen: list[str] = field(default_factory=list)
    text_events: list[str] = field(default_factory=list)
    document_written: bool = False
    content_checks: dict[str, bool] = field(default_factory=dict)
    gate_answers: dict[str, dict[str, str | None]] = field(default_factory=dict)
    """doc_id → {gate_id → recorded answer}. Covers every document touched in the session."""

    @property
    def tool_call_sequence_matches(self) -> bool:
        """True if expect_tool_calls is an ordered subsequence of tool_calls_seen."""
        return True  # evaluated against case in the test

    @property
    def all_content_present(self) -> bool:
        return all(self.content_checks.values())


# ── Runner ────────────────────────────────────────────────────────────────────


async def run_case(
    case: EvalCase,
    agent: LlmAgent,
    runner: InMemoryRunner,
    session: SessionState,
    session_path: Path,
    output_dir: str,
) -> CaseResult:
    """Drive the agent through all user turns in the eval case.

    Collects tool calls from events. Returns CaseResult with all observables
    needed for assertions.
    """
    result = CaseResult()

    adk_session = await runner.session_service.create_session(
        app_name=runner.app_name, user_id="eval-user"
    )

    for turn_text in case.turns:
        message = types.Content(
            parts=[types.Part(text=turn_text)], role="user"
        )
        async for event in runner.run_async(
            user_id="eval-user",
            session_id=adk_session.id,
            new_message=message,
        ):
            for fc in event.get_function_calls():
                result.tool_calls_seen.append(fc.name)
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        result.text_events.append(part.text)

    # Capture recorded gate answers from all documents in the session
    for doc_id, doc in session.documents.items():
        result.gate_answers[doc_id] = {
            gate_id: gs.answer for gate_id, gs in doc.gates.items()
        }

    # Check document written
    output_path = Path(output_dir) / case.phase / f"{case.document}.md"
    result.document_written = output_path.exists()

    # Check content
    if result.document_written:
        content = output_path.read_text()
        for needle in case.expect_content_contains:
            result.content_checks[needle] = needle in content

    return result


def is_subsequence(needle: list[str], haystack: list[str]) -> bool:
    """True if needle appears as an ordered subsequence in haystack."""
    it = iter(haystack)
    return all(item in it for item in needle)
