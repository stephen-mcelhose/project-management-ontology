# Issue #39 — Task Breakdown

**Process agent: drive and transition artifacts through an ontology-encoded lifecycle**  
**Spec:** `docs/specs/process-agent.md`  
**ADR:** `docs/adrs/adr-006-process-agent-architecture.md`  
**Spike filed:** #65 (LangGraph evaluation — start when #49 is picked up)

---

## Rules

- Each task MUST have a `### Verify` section — tests must be written BEFORE
  or alongside the implementation code (TDD).
- Mark a task complete only when all verify checks are green.
- Each task is a separate commit; commit messages follow Conventional Commits.
- Branch: `feat/process-agent`

---

## Task 0 — Branch and dependency additions

**Commit type:** `chore`

- Create branch `feat/process-agent` from `main`
- Add to `requirements.txt`:
  ```
  google-adk>=1.0.0
  python-dotenv>=1.0.0
  pytest>=8.0.0
  ```
- Run `make install` (or `pip install -r requirements.txt`) and confirm no
  conflicts with existing `pyshacl` / `rdflib`
- Add `.env` and `output/` to `.gitignore`
- Create `.env.example` at repo root

### Verify
```bash
pip install -r requirements.txt
python -c "import google.adk; import dotenv; print('ok')"
# .env must not appear in git status
```

---

## Task 1 — `agent/settings.py` + tests

**Commit type:** `test` then `chore`  
**Spec:** §3

Write tests FIRST in `agent/tests/test_settings.py`, then implement.

**Implementation contract:**
- `Settings.__init__` calls `load_dotenv()` (non-override), reads the six env
  vars, writes `GOOGLE_GENAI_USE_VERTEXAI` back to `os.environ`
- `Settings.project` resolves lazily via `google.auth.default()` if not set
- Never logs or returns credential values

**Tests to write:**
- `test_use_vertexai_default_is_true` — unset → `True`
- `test_use_vertexai_false_parsing` — `"false"`, `"0"`, `"off"` → `False`
- `test_api_key_fallback` — `GEMINI_API_KEY` used when `GOOGLE_API_KEY` absent
- `test_no_api_key_does_not_raise_on_vertex_path` — Vertex path never requires key
- `test_dotenv_does_not_override_existing_env` — pre-set env var survives
- `test_settings_instantiation_does_not_import_google_auth` — import `agent.settings` without credentials present; no exception at import time

### Verify
```bash
pytest agent/tests/test_settings.py -v
# All 6 tests green, no network calls
```

---

## Task 2 — `agent/lifecycle/manifest.py` + tests

**Commit type:** `test` then `chore`  
**Spec:** §4.1, §4.2

**Implementation contract:**
- `load_project_manifest(templates_dir) -> ProjectManifest` — reads
  `templates/_project-manifest.yaml`; raises `FileNotFoundError` with
  descriptive message if missing
- `load_phase_manifest(templates_dir, phase_id) -> PhaseManifest` — reads
  `templates/{phase_id}/_manifest.yaml`
- Both return typed dataclasses (not raw dicts)
- `PhaseManifest.documents` sorted by `phase_local_order`

**Tests to write (all use `tmp_path` fixture, no filesystem mocking):**
- `test_load_project_manifest_returns_phases_in_order`
- `test_load_project_manifest_missing_file_raises_with_path`
- `test_load_phase_manifest_documents_sorted_by_order`
- `test_load_phase_manifest_missing_file_raises`

### Verify
```bash
pytest agent/tests/test_manifest.py -v
# Also run against real templates dir to sanity check
python -c "from agent.lifecycle.manifest import load_project_manifest; print(load_project_manifest('templates/'))"
```

---

## Task 3 — `agent/lifecycle/gates.py` + tests

**Commit type:** `test` then `chore`  
**Spec:** §4.3, §5.2

**Implementation contract:**
- `load_gates(templates_dir, phase_id, document_id) -> list[Gate]` — reads
  `instructions.yaml`, returns gates sorted by `order`
- `Gate` dataclass: `id`, `order`, `type`, `prompt`, `fills`, `maps_to`,
  `required`, `validation`, `guidance`
- `next_unfilled_required(gates, answers) -> Gate | None` — returns the next
  gate with `required=True` and no recorded answer; returns `None` if all done

**Tests to write:**
- `test_load_gates_sorted_by_order`
- `test_load_gates_includes_optional_gates`
- `test_next_unfilled_required_skips_answered`
- `test_next_unfilled_required_returns_none_when_all_done`
- `test_next_unfilled_required_ignores_optional_gaps`

### Verify
```bash
pytest agent/tests/test_gates.py -v
```

---

## Task 4 — `agent/lifecycle/template.py` + tests

**Commit type:** `test` then `chore`  
**Spec:** §7

**Implementation contract:**
- `render_template(template_text: str, answers: dict[str, str]) -> str`
  - Replaces `{{gate_id}}` with `answers[gate_id]`
  - Missing key (optional gate with no answer) → replace with `""`
  - Returns rendered string; never writes to disk
- `check_required_placeholders(template_text, required_gate_ids, answers) -> list[str]`
  - Returns list of required gate IDs that are present as `{{gate_id}}` in
    the template but missing from `answers`; empty list = ok to write

**Tests to write:**
- `test_render_replaces_all_placeholders`
- `test_render_optional_missing_becomes_empty_string`
- `test_render_no_leftover_placeholder_syntax`
- `test_check_required_returns_empty_when_all_answered`
- `test_check_required_returns_missing_gate_ids`

### Verify
```bash
pytest agent/tests/test_template.py -v
```

---

## Task 5 — `agent/lifecycle/state.py` + tests

**Commit type:** `test` then `chore`  
**Spec:** §6

**Implementation contract:**
- Dataclasses: `GateState`, `DocumentState`, `SessionState`
- `SessionState.load(path) -> SessionState` — loads from JSON; returns fresh
  `SessionState` if file missing
- `SessionState.save(path)` — writes to disk atomically (write tmp then rename)
- `SessionState.document(doc_id) -> DocumentState` — creates on first access
- `SessionState.is_document_complete(doc_id, required_gate_ids) -> bool`
- `SessionState.is_phase_complete(phase_manifest) -> bool`

**Tests to write:**
- `test_load_missing_file_returns_fresh_state`
- `test_save_and_reload_roundtrip`
- `test_save_is_atomic` — verify no partial write visible (rename swap)
- `test_is_document_complete_false_when_gate_missing`
- `test_is_document_complete_true_when_all_required_answered`
- `test_is_phase_complete_requires_written_and_valid`

### Verify
```bash
pytest agent/tests/test_state.py -v
```

---

## Task 6 — `agent/lifecycle/validator.py` + tests

**Commit type:** `test` then `chore`  
**Spec:** §8

**Implementation contract:**
- `validate(document_path: Path, shape_path: Path) -> ValidationResult`
  - Wraps `pyshacl.validate()`
  - Returns `ValidationResult(passed: bool, messages: list[str])`
  - MUST NOT raise on validation failure; wraps exceptions as `passed=False`
  - Returns `passed=False, messages=["shape file not found: {path}"]` if
    the shape file is missing

**Tests to write:**
- `test_validate_passes_valid_document` — use a minimal turtle doc + shape
- `test_validate_fails_invalid_document` — missing required property
- `test_validate_missing_shape_returns_failure_not_exception`
- `test_validate_result_not_raised` — failure is data, not exception

### Verify
```bash
pytest agent/tests/test_validator.py -v
# These tests write tiny tmp .ttl files; no network required
```

---

## Task 7 — `agent/tools/*.py` + tests

**Commit type:** `test` then `chore`  
**Spec:** §5

Implement all five ADK `FunctionTool` wrappers. Each tool takes its
dependencies via constructor injection (not global state), enabling Protocol
fakes in tests.

**Tools and their dependency interfaces:**

| Tool                | Dependencies (Protocol)                        |
| ------------------- | ---------------------------------------------- |
| `get_progress`      | `SessionStore`, `PhaseManifestReader`          |
| `get_next_gate`     | `SessionStore`, `GateReader`                   |
| `record_answer`     | `SessionStore`, `GateReader`                   |
| `write_document`    | `SessionStore`, `GateReader`, `TemplateReader`, `DocumentWriter` |
| `validate_document` | `SessionStore`, `Validator`                    |

**Tests to write per tool (use Protocol fakes, no filesystem, no LLM):**
- Happy path with expected return value
- Error case: unknown `gate_id` → structured error, not exception
- Idempotency: calling `record_answer` twice with same gate_id → second answer wins
- `write_document` with missing required gate → error, no file written
- `validate_document` failure → `passed=False` returned, `session.valid=False`

### Verify
```bash
pytest agent/tests/test_tools.py -v
# Zero network calls, zero LLM calls
```

---

## Task 8 — `agent/agent.py` + unit tests

**Commit type:** `test` then `chore`  
**Spec:** §9 (agent construction), ADR-006 §2

**Implementation contract:**
- `build_agent(settings, tools) -> LlmAgent`
  - Constructs `google.adk.agents.LlmAgent` with the five tools
  - System instruction loaded from `docs/prompts/` or built-in string
  - Model resolved from `settings.model`
- `build_runner(agent) -> InMemoryRunner`

**Unit tests** (no LLM calls):
- `test_build_agent_name` — agent has expected name
- `test_build_agent_tools_registered` — all five tool names present
- `test_build_runner_constructs` — returns non-None runner

### Verify
```bash
# Unit
pytest agent/tests/test_agent.py -v -k "not integration"
# Construction test: fake API key, no real model call
GOOGLE_GENAI_USE_VERTEXAI=false GOOGLE_API_KEY=test-not-live \
  pytest agent/tests/test_agent.py -v
```

---

## Task 9 — Integration tests (ADK InMemoryRunner + fake model)

**Commit type:** `test`  
**Spec:** §10.3

Write two end-to-end integration tests that exercise the full stack (agent →
runner → tools → lifecycle → filesystem) with a scripted fake model that
returns deterministic gate answers.

**Test 1 — fresh session:**
1. Start with empty `tmp_path`
2. Fake model answers `project-proposal` gates 1–3 in order
3. Assert session file updated after each `record_answer`
4. Assert `write_document` writes to correct path
5. Assert rendered file contains the fake answers

**Test 2 — resume session:**
1. Write a pre-populated session JSON to `tmp_path` (all gates answered
   except the last one)
2. Start agent
3. Fake model answers the final gate
4. Assert agent did not re-ask completed gates
5. Assert document written and `valid` updated

### Verify
```bash
pytest agent/tests/test_agent_integration.py -v
# No real LLM calls; fake model injects deterministic responses
```

---

## Task 10 — `agent/__main__.py` (CLI)

**Commit type:** `chore`  
**Spec:** §9

**Implementation contract:**
- `argparse` CLI with flags from §9.1
- Loads `.env` via `Settings()` at startup
- Logs to stderr: model, vertex mode, session path
- `--fake-model` flag: injects scripted fake instead of real model
- Interactive stdin loop (§9.2)
- `--one-shot "prompt"` exits after one turn

### Verify
```bash
# Smoke test: fake model, one-shot
GOOGLE_GENAI_USE_VERTEXAI=false GOOGLE_API_KEY=test-not-live \
  python -m agent --fake-model --one-shot "hello" --templates-dir templates/ --output-dir /tmp/pm-test/
# Should print startup log and agent response; no error
```

---

## Task 11 — Eval scaffolding

**Commit type:** `chore`  
**Spec:** §10.4

- Create `agent/evals/cases/` directory
- Write one YAML eval case for `project-proposal` (full gate walk)
- Write `agent/evals/conftest.py` with `pytest.mark.eval` guard
- Document how to run: `pytest -m eval --run-evals` in `docs/processes/`

### Verify
```bash
# Evals must NOT run in standard test suite
pytest agent/tests/ -v  # no eval output
pytest -m eval  # skip with "no tests ran" or "eval marker requires --run-evals"
```

---

## Task 12 — Makefile targets + docs

**Commit type:** `chore`

- Add `agent-test` target: `$(PY) -m pytest agent/tests/ -v`
- Add `agent-run` target: `$(PY) -m agent --templates-dir templates/ --output-dir output/`
- Update `docs/wiki/index.md` to register `docs/specs/process-agent.md`
- Update `docs/processes/` with a brief how-to for running the agent
- Update `docs/adrs/README.md` (if present) with ADR-006 entry

### Verify
```bash
make agent-test
# All unit + integration tests green; no eval tests run
```

---

## Task 13 — PR

**Commit type:** N/A (PR description)

- Push `feat/process-agent`
- Open PR to `main`
- PR description references issue #39, ADR-006, spike #65
- Request 2 reviewers
- Close issue #39 via `Closes #39` in PR body

---

## Deferred explicitly

| Behaviour                       | Filed as    |
| ------------------------------- | ----------- |
| LangGraph evaluation            | Spike #65   |
| Out-of-order navigation         | Issue #49   |
| Human sponsor review gate       | Issue #49   |
| Multi-project session state     | Issue #49   |
| `_project-manifest.yaml` creation | Issue #50 |
