"""Unit tests for agent/agent.py — no LLM calls, no network."""


from agent.agent import (
    _BASE_INSTRUCTION,
    build_agent,
    build_runner,
    compose_instruction,
)
from agent.lifecycle.state import SessionState


class TestComposeInstruction:
    def test_no_domain_returns_base(self):
        result = compose_instruction("")
        assert result == _BASE_INSTRUCTION

    def test_whitespace_only_returns_base(self):
        result = compose_instruction("   \n  ")
        assert result == _BASE_INSTRUCTION

    def test_domain_prepended_to_base(self):
        domain = "You are a PM expert following ISO 21502."
        result = compose_instruction(domain)
        assert result.startswith(domain)
        assert _BASE_INSTRUCTION in result
        # Exactly one blank line between domain and base
        assert domain + "\n\n" + _BASE_INSTRUCTION == result

    def test_domain_stripped_before_prepend(self):
        domain = "  You are a PM expert.  \n"
        result = compose_instruction(domain)
        assert result.startswith("You are a PM expert.")

    def test_agent_uses_composed_instruction(self):
        domain = "You are an ISO 21502 PM assistant."
        session = SessionState(project_name="T", current_phase="initiation",
                               current_document="proposal")
        agent = build_agent(
            session=session, session_path=None,
            templates_dir="/fake", output_dir="/fake/out",
            model="fake-model", domain_instructions=domain,
        )
        assert agent.instruction.startswith(domain)
        assert _BASE_INSTRUCTION in agent.instruction

    def test_agent_without_domain_uses_base_only(self):
        session = SessionState(project_name="T", current_phase="initiation",
                               current_document="proposal")
        agent = build_agent(
            session=session, session_path=None,
            templates_dir="/fake", output_dir="/fake/out",
            model="fake-model",
        )
        assert agent.instruction == _BASE_INSTRUCTION


class TestBuildAgent:
    def test_agent_has_name(self):
        session = SessionState(project_name="Test", current_phase="initiation",
                               current_document="proposal")
        agent = build_agent(
            session=session,
            session_path=None,
            templates_dir="/fake",
            output_dir="/fake/output",
            model="fake-model",
        )
        assert agent.name is not None
        assert len(agent.name) > 0

    def test_all_five_tools_registered(self):
        session = SessionState(project_name="Test", current_phase="initiation",
                               current_document="proposal")
        agent = build_agent(
            session=session,
            session_path=None,
            templates_dir="/fake",
            output_dir="/fake/output",
            model="fake-model",
        )
        tool_names = {t.name for t in agent.tools}
        assert "get_progress" in tool_names
        assert "get_next_gate" in tool_names
        assert "record_answer" in tool_names
        assert "write_document" in tool_names
        assert "validate_document" in tool_names

    def test_model_assigned(self):
        session = SessionState(project_name="Test", current_phase="initiation",
                               current_document="proposal")
        agent = build_agent(
            session=session,
            session_path=None,
            templates_dir="/fake",
            output_dir="/fake/output",
            model="gemini-test-model",
        )
        assert agent.model == "gemini-test-model"


class TestBuildRunner:
    def test_returns_in_memory_runner(self):
        from google.adk.runners import InMemoryRunner
        session = SessionState(project_name="Test", current_phase="initiation",
                               current_document="proposal")
        agent = build_agent(
            session=session,
            session_path=None,
            templates_dir="/fake",
            output_dir="/fake/output",
            model="fake-model",
        )
        runner = build_runner(agent)
        assert isinstance(runner, InMemoryRunner)
