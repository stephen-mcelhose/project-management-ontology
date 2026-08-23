"""ADK web entry point — exports root_agent for `adk web`.

Configuration via environment variables (set in .env or shell):
  TEMPLATES_DIR   Path to the templates directory  (default: templates/)
  OUTPUT_DIR      Path to the output directory      (default: output/)

Session state is persisted to {OUTPUT_DIR}/.session.json so a conversation
can be resumed across adk web restarts.

For multi-user / multi-session support see issue #75 (migrate SessionState
into ADK tool_context.state).
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(override=False)

from agent.agent import build_agent  # noqa: E402
from agent.lifecycle.manifest import load_project_manifest  # noqa: E402
from agent.lifecycle.state import SessionState  # noqa: E402
from agent.settings import Settings  # noqa: E402

_settings = Settings()
_templates_dir = os.environ.get("TEMPLATES_DIR", "templates/")
_output_dir = os.environ.get("OUTPUT_DIR", "output/")
_session_path = Path(_output_dir) / ".session.json"

_session = SessionState.load(_session_path)

# Seed phase/document on a fresh session
if not _session.current_phase:
    try:
        _pm = load_project_manifest(_templates_dir)
        if _pm.phases:
            from agent.lifecycle.manifest import load_phase_manifest
            _session.current_phase = _pm.phases[0].id
            _phase = load_phase_manifest(_templates_dir, _pm.phases[0].id)
            if _phase.documents:
                _session.current_document = _phase.documents[0].id
    except FileNotFoundError:
        pass

_domain_instructions = ""
try:
    _domain_instructions = load_project_manifest(_templates_dir).agent_instructions
except FileNotFoundError:
    pass

root_agent = build_agent(
    session=_session,
    session_path=_session_path,
    templates_dir=_templates_dir,
    output_dir=_output_dir,
    model=_settings.model,
    domain_instructions=_domain_instructions,
)
