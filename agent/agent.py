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
from agent.tools.get_phase_gates import get_phase_gates as _get_phase_gates
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
2. Call get_phase_gates() to load the full map of gate ids and prompts for
   every document in the current phase. Keep this map for the session.
3. Call get_next_gate(document_id) to find the next question to ask.
4. Before asking the question, scan the user's most recent message against
   the phase gate map. For every piece of information that clearly matches a
   gate — in any document in the phase — call record_answer(document_id,
   gate_id, answer). Only use gate ids that appear in the map.
5. Ask the user for the next unfilled gate. Wait for their answer.
6. Call record_answer for their response, then repeat from step 3.
7. When get_next_gate returns null, call write_document(document_id).
8. Call validate_document(document_id) and report any issues to the user.
9. Advance to the next document or phase.

Rules:
- Ask one gate at a time. Do not ask multiple questions in one turn.
- When a gate has a guidance field, use it to challenge vague or incomplete answers.
- Never invent answers — always ask the user.
- Only record against gate ids returned by get_phase_gates — never guess an id.
- If the user mentions something that does not match any gate in the phase,
  acknowledge it briefly and move on. Do not record it.
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

    def get_phase_gates() -> dict[str, dict[str, str]]:
        """Return {document_id: {gate_id: prompt}} for every document in the current phase."""
        return _get_phase_gates(
            phase=session.current_phase,
            templates_dir=templates_dir,
            gate_reader=gate_reader,
        )

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
            FunctionTool(get_phase_gates),
            FunctionTool(get_next_gate),
            FunctionTool(record_answer),
            FunctionTool(write_document),
            FunctionTool(validate_document),
        ],
    )


def build_runner(agent: LlmAgent) -> InMemoryRunner:
    """Wrap the agent in an InMemoryRunner for local / test use."""
    return InMemoryRunner(agent=agent, app_name="pm_process_agent")
