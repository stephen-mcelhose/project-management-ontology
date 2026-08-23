---
type: decision
title: "ADR-006: Process Agent Architecture"
description: >
  Establishes the technology choices for the process agent (issue #39):
  Python, google-adk LlmAgent with function tools, env-file-driven auth,
  file-based session state, and pyshacl validation. Records the deferral of
  LangGraph and the conditions under which that decision must be revisited.
timestamp: 2026-08-23T00:00:00Z
status: accepted
tags: [adr, agent, process-agent, architecture, adk, python]
---

# ADR-006: Process Agent Architecture

**Status:** Accepted  
**Date:** 2026-08-23  
**Deciders:** Stephen McElhose

---

## Context

Issue #39 requires a process agent that drives a user through the PM lifecycle
gate by gate. The artifact layer is complete — every document has an
`instructions.yaml` (gate sequence), `template.md` (output scaffold), and a
SHACL shape (validation contract). The agent's job is to read those files,
ask the right questions, record answers, fill templates, and track progress.

Four decisions needed:

1. **Language** — the existing tooling is Python; introducing a second runtime
   adds coordination cost.
2. **Agent framework** — the Python ADK ecosystem offers both a vanilla
   `LlmAgent` and, via LangGraph integration, graph-structured orchestration.
3. **Auth / credential management** — credentials must never appear in source
   code; local development must work without cloud infrastructure.
4. **Session state** — progress must survive process restarts; the right
   storage layer depends on the complexity of the state machine.

---

## Decision

### 1. Language: Python

The repository already has a Python virtual environment (`requirements.txt`,
`.venv`), and `pyshacl` / `rdflib` (required for document validation) are
already installed. Adding the process agent as a Python package under `agent/`
reuses this toolchain directly.

Go was considered — the Go ADK SDK (`google.golang.org/adk/v2`) is mature and
has strong interface-based testability. It was rejected for this repo because
it would introduce a second language runtime for what is fundamentally a
Python-native project, and there is no other Go code here to justify the
infrastructure cost.

### 2. Agent framework: google-adk `LlmAgent` + function tools

The process agent in issue #39 is **sequential**: walk phase → walk document
→ walk gates in order → write → validate → advance. This maps cleanly onto a
single `LlmAgent` with a small set of `FunctionTool`s:

| Tool                | Contract                                                  |
| ------------------- | --------------------------------------------------------- |
| `get_progress`      | Return current phase / document / gate position           |
| `get_next_gate`     | Return next unfilled required gate for a document         |
| `record_answer`     | Persist a gate answer; return completion status           |
| `write_document`    | Render template + write filled Markdown to output dir     |
| `validate_document` | Run pyshacl; return pass/fail + messages                  |

The LLM calls these tools; the tools are pure functions with no side effects
beyond their declared contracts. This is the simplest architecture that
satisfies the issue #39 requirements.

**LangGraph deferred** — see §4 below.

### 3. Auth / credential management: Settings class + `.env` file

All configuration is read from environment variables. A `Settings` class
(in `agent/settings.py`) follows this pattern:

- Calls `load_dotenv()` at construction time so that a local `.env` file
  populates missing variables without overriding anything already set in the
  shell. This is the standard pattern for Python ADK deployments.
- Reads `GOOGLE_GENAI_USE_VERTEXAI` (default `true`), `GOOGLE_CLOUD_PROJECT`
  (resolved lazily via `google.auth.default()` if not set),
  `GOOGLE_CLOUD_LOCATION` (default `global`), `AGENT_MODEL`
  (default `gemini-2.0-flash`), and `GOOGLE_API_KEY` / `GEMINI_API_KEY`
  (required only when Vertex AI is disabled).
- Writes `GOOGLE_GENAI_USE_VERTEXAI` back to `os.environ` so the `google-genai`
  SDK picks it up without the caller needing to set it.
- Never logs or returns credential values.

A `.env.example` file is committed to the repository with no real credentials.
`.env` is listed in `.gitignore`. The `Settings` class is instantiated at
process start (in `__main__.py`), not at module import time, so tests can
exercise it without live credentials by using `monkeypatch.setenv`.

**Vertex AI path (default):** Application Default Credentials — no API key
required. Intended for CI and cloud deployment.

**AI Studio path (local alt):** `GOOGLE_GENAI_USE_VERTEXAI=false` +
`GOOGLE_API_KEY`. Intended for developers without Vertex access.

### 4. Session state: JSON file on disk

Session state (current phase, current document, gate answers, written /
validated flags) is serialized to `{output_dir}/.session.json`. On startup the
agent loads the file if present and resumes from the recorded position.
A missing file starts a fresh session.

This is the simplest durable store for a single-user CLI agent. It requires no
database, no external service, and no infrastructure. The schema is a plain
Python dataclass serialized via `dataclasses.asdict` + `json.dumps`.

A persistent session service (e.g. Firestore, ADK's built-in session backends)
is deferred to issue #49, which introduces multi-project state.

---

## LangGraph deferral (decision #2 expanded)

### Why LangGraph was considered

LangGraph models agents as directed graphs where nodes are processing steps and
edges encode routing logic. It offers:

- Explicit conditional branching (natural fit for issue #62 — conditional gate
  branching)
- First-class human-in-the-loop interrupts (natural fit for issue #49)
- Built-in checkpointing (eliminates the hand-rolled JSON session file)

### Why it is deferred

For the sequential gate-walking of issue #39, LangGraph is unnecessary
complexity. The gate sequence is already encoded in `instructions.yaml`
(ordered, dependency-checked); there is no conditional routing, no parallel
execution, and no branching. Adding graph infrastructure at this stage would
obscure the simpler structure rather than clarify it.

### Revisit trigger

**Issue #65 (Spike: evaluate LangGraph)** MUST be started when issue #49
(out-of-order navigation, conditional branching, human-in-the-loop review) is
picked up, or when issue #62 (conditional gate branching) produces a
recommendation that requires routing logic the vanilla agent cannot express.

The spike MUST produce a written go/no-go recommendation. If the outcome is
"go", this ADR MUST be superseded by a new ADR that documents the migration
path. If "no-go", this ADR remains the authoritative decision and #65 is
closed with rationale.

**Do not start the spike before issue #39 is merged.** The base agent must be
stable before evaluating a framework change.

---

## Consequences

### Positive

- Minimal new dependencies (`google-adk`, `python-dotenv`); everything else
  already in `requirements.txt`.
- No credentials ever appear in source code.
- `.env` pattern is immediately useful for local development without setup.
- Unit tests can run without any cloud credentials by patching env vars.
- JSON session file is human-readable — easy to inspect and debug.
- Clear upgrade path: if the spike recommends LangGraph, the `tools/` and
  `lifecycle/` modules are framework-agnostic and can be reused.

### Negative / risks

- JSON session file is not concurrent-safe (acceptable for a single-user CLI).
- If issue #49 requirements are broader than expected, the vanilla LlmAgent
  may need to be replaced earlier than the spike revisit trigger assumes.
- `google-adk` Python SDK API stability — pin to a minor version in
  `requirements.txt`.

---

## Alternatives rejected

| Alternative                        | Reason rejected                                                  |
| ---------------------------------- | ---------------------------------------------------------------- |
| Go ADK                             | Second runtime in a Python-only repo; no existing Go code        |
| LangGraph (now)                    | Unnecessary for sequential flow; deferred to spike #65           |
| Hardcoded Vertex project in code   | Security violation; all config must be env-driven                |
| SQLite for session state           | No advantage over JSON for single-user CLI; adds a dependency    |
| ADK persistent session service     | Deferred to #49 (multi-project state)                            |

---

## Related

- Issue #39 — Process agent implementation
- Issue #49 — Process agent: advanced control (out-of-order, multi-project)
- Issue #62 — Spike: conditional gate branching in `instructions.yaml`
- Issue #65 — Spike: evaluate LangGraph as orchestration layer (revisit trigger)
- ADR-002 — Phase agent prompts as scaffolds (deferred agent spec, now resolved)
- ADR-003 — Phase manifest pattern (artifact layer the agent reads)
- `docs/specs/process-agent.md` — Normative behavioural specification
