"""Build the PM Process Agent and its InMemoryRunner.

The agent is an LlmAgent with five tools. Dependencies are passed in
so tests can inject fakes without touching the filesystem or network.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner
from google.adk.tools import FunctionTool

from agent.lifecycle.document_writer import FileDocumentWriter
from agent.lifecycle.gate_reader import FileGateReader
from agent.lifecycle.state import SessionState
from agent.lifecycle.validator import validate as _validate
from agent.tools.get_next_gate import get_next_gate as _get_next_gate
from agent.tools.get_progress import get_progress as _get_progress
from agent.tools.record_answer import record_answer as _record_answer
from agent.tools.validate_document import validate_document as _validate_document
from agent.tools.write_document import write_document as _write_document

# ── Layer 1: base mechanics (ADR-007) ────────────────────────────────────────
# Describes only the tool loop. Never changes regardless of domain.
# Domain expertise lives in _project-manifest.yaml agent_instructions (Layer 2)
# and gate guidance returned by get_next_gate() (Layer 3).
_BASE_INSTRUCTION = """\
Your workflow for each document:
1. Call get_progress() to orient yourself.
2. Call get_next_gate(document_id) to find the next question to ask.
3. Ask the user the gate's prompt in plain language. Wait for their answer.
4. Call record_answer(document_id, gate_id, answer) with their response.
5. Repeat until get_next_gate returns null (all required gates answered).
6. Call write_document(document_id) to produce the filled Markdown document.
7. Call validate_document(document_id) and report any issues to the user.
8. Advance to the next document or phase.

Rules:
- Ask one gate at a time. Do not ask multiple questions in one turn.
- When a gate has a guidance field, use it to challenge vague or incomplete answers.
- Never invent answers — always ask the user.
- When all required documents in a phase are complete, announce this and
  ask before advancing to the next phase.
"""


def compose_instruction(domain_instructions: str = "") -> str:
    """Compose the full system instruction from domain + base layers (ADR-007).

    If domain_instructions is non-empty it is prepended to the base mechanics,
    giving the model its domain identity before it reads the loop rules.
    """
    if domain_instructions.strip():
        return domain_instructions.strip() + "\n\n" + _BASE_INSTRUCTION
    return _BASE_INSTRUCTION


def build_agent(
    session: SessionState,
    session_path: Path | None,
    templates_dir: str,
    output_dir: str,
    model: str = "gemini-2.0-flash",
    domain_instructions: str = "",
    gate_reader=None,
    document_writer=None,
    validator=None,
) -> LlmAgent:
    """Construct the LlmAgent with all five tools wired to session/filesystem.

    domain_instructions is prepended to the base system instruction (ADR-007).
    Loaded from _project-manifest.yaml agent_instructions by the caller;
    defaults to "" so the agent is functional before that file exists.

    gate_reader, document_writer, and validator can be injected for testing.
    """
    gate_reader = gate_reader or FileGateReader()
    document_writer = document_writer or FileDocumentWriter()

    class _FileValidator:
        def validate(self, document_path, shape_path):
            return _validate(document_path, shape_path)

    validator = validator or _FileValidator()

    def get_progress() -> dict[str, Any]:
        """Return current phase, document, and answered gate count."""
        return _get_progress(session)

    def get_next_gate(document_id: str) -> dict[str, Any] | None:
        """Return the next unfilled required gate for document_id, or null."""
        return _get_next_gate(
            session=session,
            document_id=document_id,
            templates_dir=templates_dir,
            gate_reader=gate_reader,
        )

    def record_answer(document_id: str, gate_id: str, answer: str) -> dict[str, Any]:
        """Persist an answer for gate_id in document_id."""
        return _record_answer(
            session=session,
            session_path=session_path,
            document_id=document_id,
            gate_id=gate_id,
            answer=answer,
            templates_dir=templates_dir,
            gate_reader=gate_reader,
        )

    def write_document(document_id: str) -> dict[str, Any]:
        """Render template and write the filled document to the output directory."""
        return _write_document(
            session=session,
            session_path=session_path,
            document_id=document_id,
            templates_dir=templates_dir,
            output_dir=output_dir,
            gate_reader=gate_reader,
            document_writer=document_writer,
        )

    def validate_document(document_id: str) -> dict[str, Any]:
        """Run SHACL validation on the written document."""
        return _validate_document(
            session=session,
            session_path=session_path,
            document_id=document_id,
            templates_dir=templates_dir,
            output_dir=output_dir,
            validator=validator,
        )

    return LlmAgent(
        name="pm_process_agent",
        model=model,
        instruction=compose_instruction(domain_instructions),
        tools=[
            FunctionTool(get_progress),
            FunctionTool(get_next_gate),
            FunctionTool(record_answer),
            FunctionTool(write_document),
            FunctionTool(validate_document),
        ],
    )


def build_runner(agent: LlmAgent) -> InMemoryRunner:
    """Wrap the agent in an InMemoryRunner for local / test use."""
    return InMemoryRunner(agent=agent, app_name="pm_process_agent")
