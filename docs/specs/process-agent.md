---
type: spec
title: "Process Agent — Normative Specification"
description: >
  RFC 2119 behavioural specification for the PM Process Agent (issue #39).
  The agent drives a user through the ontology-encoded project lifecycle,
  gate by gate, document by document, phase by phase.
status: draft
issue: "https://github.com/stephen-mcelhose/process-assistant/issues/39"
timestamp: 2026-08-23T00:00:00Z
tags: [spec, agent, process-agent, adk]
---

# Process Agent — Normative Specification

**Status:** Draft  
**Issue:** [#39](https://github.com/stephen-mcelhose/process-assistant/issues/39)  
**RFC 2119 keywords apply throughout:** MUST, MUST NOT, SHOULD, MAY

---

## 1. Purpose

The Process Agent assists a user in producing a complete set of PM documents
for a single project. It reads the ontology-encoded artifact layer
(`_manifest.yaml`, `instructions.yaml`, `template.md`, SHACL shapes) and
drives a structured, gate-by-gate conversation to fill each document.

This specification covers the base agent (issue #39). Advanced features —
out-of-order navigation, human sponsor review gates, multi-project state —
are deferred to issue #49 and spike #65 (LangGraph evaluation).

---

## 2. Definitions

| Term            | Definition                                                                 |
| --------------- | -------------------------------------------------------------------------- |
| **Gate**        | One entry in `instructions.yaml`'s `gates` array; one question/answer unit |
| **Document**    | A PM artifact defined by a template pack (entry + instructions + template + SHACL) |
| **Phase**       | A lifecycle stage (Initiation → Planning → Execution → Monitoring & Control → Closure) |
| **Session**     | Persisted state of one user's run through the lifecycle for one project    |
| **Output dir**  | Filesystem path where filled documents are written                         |
| **Session file**| `{output_dir}/.session.json` — machine-readable session state              |

---

## 3. Configuration

### 3.1 Environment variables

The agent MUST read all configuration from environment variables. It MUST NOT
hardcode credentials, project IDs, or API keys anywhere in source code.

| Variable                    | Default            | Notes                                      |
| --------------------------- | ------------------ | ------------------------------------------ |
| `GOOGLE_GENAI_USE_VERTEXAI` | `true`             |                                            |
| `GOOGLE_CLOUD_PROJECT`      | ADC-resolved       | Resolved lazily via `google.auth.default()` |
| `GOOGLE_CLOUD_LOCATION`     | `global`           |                                            |
| `AGENT_MODEL`               | `gemini-2.0-flash` |                                            |
| `GOOGLE_API_KEY`            | —                  | Required when `USE_VERTEXAI=false`         |
| `GEMINI_API_KEY`            | —                  | Fallback for `GOOGLE_API_KEY`              |

### 3.2 `.env` file

The agent MUST call `load_dotenv()` at startup. Existing shell environment
variables MUST take precedence over `.env` values (non-override semantics).
A missing `.env` file MUST be a no-op.

The repository MUST provide `.env.example` containing no real credentials.
`.env` MUST be listed in `.gitignore`.

### 3.3 Vertex AI path (default)

When `GOOGLE_GENAI_USE_VERTEXAI` is truthy, the agent MUST authenticate via
Application Default Credentials. No API key is required.
`GOOGLE_CLOUD_PROJECT` MAY be resolved lazily via `google.auth.default()`.

### 3.4 AI Studio path

When `GOOGLE_GENAI_USE_VERTEXAI` is falsy, at least one of `GOOGLE_API_KEY`
or `GEMINI_API_KEY` MUST be set. The agent MUST fail at startup — before any
tool call — with a descriptive error if neither is present.

### 3.5 Settings instantiation

The `Settings` class MUST be instantiated in `__main__.py`, not at module
import time, so that tests can exercise it via `monkeypatch.setenv` without
side effects at collection time.

---

## 4. Lifecycle Navigation

### 4.1 Phase ordering

The agent MUST navigate phases in the order declared by
`{templates_dir}/_project-manifest.yaml`. If that file does not exist, the agent
MUST fail with a descriptive error listing the expected path.

### 4.2 Document ordering

Within a phase the agent MUST navigate documents in ascending `phase_local_order`
as declared in the phase `_manifest.yaml`. It MUST NOT advance to a document
whose `dependencies` list contains a document that is not yet complete.

### 4.3 Gate ordering

Within a document the agent MUST present gates in ascending `order` as declared
in `instructions.yaml`. A gate with `required: true` MUST be answered before
the document is considered complete. A gate with `required: false` MAY be
skipped by the user on request.

### 4.4 Shared context

Fields listed under `shared_context` in a phase manifest MUST be collected
once per phase and carried forward automatically into subsequent documents.
The agent MUST NOT ask for a shared context field again once it is recorded in
the session.

### 4.5 Phase completion

A phase is complete when every document listed as required in the phase
manifest has `written: true` and `valid: true` in the session state. The
agent MUST announce phase completion and prompt the user before advancing to
the next phase.

---

## 5. Tools

The agent MUST expose the following five tools to the LLM. Each tool MUST be
a pure function: no side effects beyond its declared contract.

### 5.1 `get_progress() → ProgressReport`

Returns the current phase, document, gate index, and counts of completed vs.
total required gates across all documents in the current phase.
MUST NOT modify session state.

### 5.2 `get_next_gate(document_id: str) → GateSpec | None`

Returns the next unfilled required gate for `document_id`: its `id`, `prompt`,
`fills`, `maps_to`, `type`, `validation`, and `guidance` fields.
Returns `None` when all required gates for that document are filled.
MUST NOT modify session state.

### 5.3 `record_answer(document_id: str, gate_id: str, answer: str) → RecordResult`

Persists `answer` for `gate_id` in the session file on disk before returning.
MUST validate that `gate_id` exists in `instructions.yaml` for `document_id`;
returns an error if not.
MUST return whether all required gates for `document_id` are now filled.
MUST be idempotent: a second call with the same `gate_id` overwrites the
previous answer.

### 5.4 `write_document(document_id: str) → WriteResult`

Renders `template.md` by substituting every `{{gate_id}}` placeholder with the
recorded answer for that gate. Writes the result to
`{output_dir}/{phase}/{document_id}.md`.
MUST return an error (not raise) if any `required: true` gate has no recorded
answer; MUST NOT write a partial document.
MUST be idempotent: writing the same document twice overwrites the first file.

### 5.5 `validate_document(document_id: str) → ValidationResult`

Runs `pyshacl` against the filled document and its SHACL shape.
Returns `passed: bool` and `messages: list[str]`.
MUST update `DocumentState.valid` in the session file.
MUST NOT raise on validation failure — returns failure details as data.

---

## 6. Session State

### 6.1 Location

Session state MUST be stored at `{output_dir}/.session.json`.

### 6.2 Schema

```json
{
  "project_name": "string",
  "current_phase": "string",
  "current_document": "string",
  "shared_context": { "field_id": "value" },
  "documents": {
    "document_id": {
      "gates": {
        "gate_id": { "answer": "string | null", "skipped": false }
      },
      "written": false,
      "valid": false
    }
  }
}
```

### 6.3 Resumability

On startup the agent MUST load an existing session file if present and resume
from the recorded `current_phase` / `current_document` position.
A missing session file MUST be treated as a fresh session.

### 6.4 Durability

`record_answer` MUST write the session file to disk before returning.
The agent MUST NOT buffer session state in memory only across turns.

---

## 7. Document Output

### 7.1 Path

`write_document` MUST write to `{output_dir}/{phase}/{document_id}.md`.
Parent directories MUST be created if they do not exist.

### 7.2 Placeholder substitution

Every `{{gate_id}}` in `template.md` MUST be replaced with the recorded answer.
Placeholders for optional gates with no answer MUST be replaced with an empty
string — MUST NOT be left as `{{…}}` in the output.

### 7.3 Unfilled required gates

`write_document` MUST return a structured error if any `required: true` gate
has no recorded answer. MUST NOT write the document in this case.

---

## 8. Validation

The agent SHOULD call `validate_document` immediately after a successful
`write_document`. A validation failure MUST NOT prevent the document from
being written; it MUST surface the failure messages so the user can correct
their answers.

---

## 9. CLI

### 9.1 Invocation

```
python -m agent [OPTIONS]
```

| Flag              | Default                      | Description                              |
| ----------------- | ---------------------------- | ---------------------------------------- |
| `--templates-dir` | `domains/pm/templates/`      | Root of the template artifact layer      |
| `--output-dir`    | `output/`                    | Where filled documents are written       |
| `--session`       | `{output_dir}/.session.json` | Override session file path               |
| `--one-shot`      | —                            | Non-interactive: single prompt then exit |
| `--fake-model`    | —                            | Scripted fake model (CI / testing)       |

### 9.2 Interactive loop

Without `--one-shot` the agent MUST run an interactive stdin/stdout loop,
preserving session context across turns in the same invocation.

### 9.3 Startup log

On startup the agent MUST log to stderr: model name, Vertex AI mode, and
session file path. It MUST NOT log any credential value.

---

## 10. Testing

### 10.1 Unit tests — lifecycle modules

`manifest.py`, `gates.py`, `template.py`, `state.py`, and `validator.py` MUST
each have pytest unit tests. Tests MUST use `tmp_path` fixtures and MUST NOT
make network calls or require live credentials. Env-dependent code MUST be
tested via `monkeypatch.setenv`; `Settings` MUST be instantiated inside each
test, not at module import time.

### 10.2 Unit tests — tools

Each tool function MUST be tested against Protocol-based fakes for its
dependencies (state store, filesystem, validator). Tests MUST cover the happy
path, required-gate-missing error, and idempotent re-call.

### 10.3 Integration tests — ADK runner

At minimum two integration tests MUST exercise the full agent via the ADK
`InMemoryRunner` with `--fake-model` scripted responses:

1. **Fresh session:** walk the required gates on `project-proposal`, assert
   the written document contains the expected answers.
2. **Resume session:** load a pre-populated session JSON, assert the agent
   skips completed gates and presents the correct next gate.

These tests MUST NOT make real LLM or network calls.

### 10.4 Evals (opt-in, real model)

YAML eval cases MUST live in `agent/evals/cases/`. Each case declares: one or
more user prompts, expected tool call sequence, and expected content in the
written document. Evals MUST run only under `pytest -m eval` and MUST NOT
execute during standard `make test`.

---

## 11. Out of scope (deferred)

| Feature                                | Deferred to      |
| -------------------------------------- | ---------------- |
| Out-of-order gate navigation           | Issue #49        |
| Human sponsor review gate              | Issue #49        |
| Multi-project session management       | Issue #49        |
| LangGraph orchestration layer          | Spike #65        |
| ADK persistent session service         | Issue #49        |
| RDF triple emission alongside Markdown | Future           |
| Streaming output                       | Future           |
| Cross-phase shared context propagation | Future           |
