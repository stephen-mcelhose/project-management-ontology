"""Unit tests for agent/agent.py — no LLM calls, no network."""

import pytest

from agent.agent import build_agent, build_runner
from agent.lifecycle.state import SessionState


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
