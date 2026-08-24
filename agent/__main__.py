"""PM Process Agent — CLI entry point.

Usage:
    python -m agent [OPTIONS]

Options:
    --templates-dir DIR   Root of template artifact layer (default: domains/pm/templates/)
    --output-dir DIR      Where filled documents are written (default: output/)
    --session PATH        Session file path (default: {output-dir}/.session.json)
    --one-shot TEXT       Non-interactive: run one prompt then exit
    --fake-model          Use scripted fake model (CI / testing)
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

from google.genai import types


def _parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="python -m agent",
        description="PM Process Agent — drive artifacts through the lifecycle.",
    )
    parser.add_argument(
        "--templates-dir", default="domains/pm/templates/", metavar="DIR",
        help="Root of the template artifact layer (default: domains/pm/templates/)",
    )
    parser.add_argument(
        "--output-dir", default="output/", metavar="DIR",
        help="Where filled documents are written (default: output/)",
    )
    parser.add_argument(
        "--session", default=None, metavar="PATH",
        help="Session file path (default: {output-dir}/.session.json)",
    )
    parser.add_argument(
        "--one-shot", default=None, metavar="TEXT",
        help="Non-interactive: run one prompt then exit",
    )
    parser.add_argument(
        "--fake-model", action="store_true",
        help="Use a scripted fake model (CI / testing — no real LLM calls)",
    )
    return parser.parse_args(argv)


async def _run_interactive(runner, user_id: str, session_id: str) -> None:
    print("PM Process Agent ready. Type your message, or Ctrl+C to exit.\n",
          file=sys.stderr)
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.", file=sys.stderr)
            break
        if not user_input:
            continue
        message = types.Content(
            parts=[types.Part(text=user_input)], role="user"
        )
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=message,
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print(f"Agent: {part.text}")


async def _run_one_shot(runner, user_id: str, session_id: str, prompt: str) -> None:
    message = types.Content(parts=[types.Part(text=prompt)], role="user")
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=message,
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(part.text)


def main(argv=None) -> None:
    args = _parse_args(argv)

    # Settings must be imported here (not at module level) so env vars set
    # by tests via monkeypatch are picked up at instantiation time.
    from agent.settings import Settings
    settings = Settings()

    if not settings.use_vertexai and not settings.api_key:
        print(
            "Error: GOOGLE_GENAI_USE_VERTEXAI=false but no GOOGLE_API_KEY or "
            "GEMINI_API_KEY is set. Provide a key or switch to Vertex AI.",
            file=sys.stderr,
        )
        sys.exit(1)

    output_dir = args.output_dir
    session_path = Path(args.session) if args.session else Path(output_dir) / ".session.json"

    # Startup log (stderr — no credential values)
    print(f"Model:        {settings.model}", file=sys.stderr)
    print(f"Vertex AI:    {settings.use_vertexai}", file=sys.stderr)
    print(f"Session file: {session_path}", file=sys.stderr)
    print(f"Templates:    {args.templates_dir}", file=sys.stderr)
    print(f"Output:       {output_dir}", file=sys.stderr)

    from agent.agent import build_agent, build_runner
    from agent.lifecycle.manifest import load_phase_manifest, load_project_manifest
    from agent.lifecycle.state import SessionState

    session = SessionState.load(session_path)

    # Load domain instructions from _project-manifest.yaml if it exists.
    # Gracefully absent until issue #50 authors the file (ADR-007).
    domain_instructions = ""
    try:
        project_manifest = load_project_manifest(args.templates_dir)
        domain_instructions = project_manifest.agent_instructions

        # Seed a fresh session with the first phase/document so get_progress()
        # always returns a valid document_id — without this the model hallucinates
        # a document_id when calling get_next_gate() on first run.
        if not session.current_phase and project_manifest.phases:
            first_phase = project_manifest.phases[0]
            session.current_phase = first_phase.id
            phase_manifest = load_phase_manifest(args.templates_dir, first_phase.id)
            if phase_manifest.documents:
                session.current_document = phase_manifest.documents[0].id
            print(
                f"New session: starting at {session.current_phase}/{session.current_document}",
                file=sys.stderr,
            )
        if domain_instructions:
            print("Domain instructions: loaded from _project-manifest.yaml", file=sys.stderr)
        else:
            print("Domain instructions: none (agent_instructions not set in _project-manifest.yaml)", file=sys.stderr)
    except FileNotFoundError:
        print("Domain instructions: none (_project-manifest.yaml not found)", file=sys.stderr)

    model = "__fake__" if args.fake_model else settings.model

    agent = build_agent(
        session=session,
        session_path=session_path,
        templates_dir=args.templates_dir,
        output_dir=output_dir,
        model=model,
        domain_instructions=domain_instructions,
    )
    runner = build_runner(agent)

    async def _main():
        adk_session = await runner.session_service.create_session(
            app_name=runner.app_name, user_id="local-user"
        )
        if args.one_shot:
            await _run_one_shot(runner, "local-user", adk_session.id, args.one_shot)
        else:
            await _run_interactive(runner, "local-user", adk_session.id)

    asyncio.run(_main())


if __name__ == "__main__":
    main()
