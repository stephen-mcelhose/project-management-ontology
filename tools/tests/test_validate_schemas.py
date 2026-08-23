"""Tests for tools/validate/validate_schemas.py.

Covers:
  _gate_ids_for()             — helper unit tests.
  validate_project_manifest() — all 6 checks, happy path + each failure mode.
  validate_all()              — cross-reference checks that JSON Schema cannot
                                enforce (duplicate gate ids, bad required_gates).

Strategy
--------
validate_project_manifest() reads from the module-level TEMPLATES_DIR constant.
Each test uses ``monkeypatch.setattr(vs, "TEMPLATES_DIR", tmp_path)`` to
redirect all filesystem access to an isolated temp directory.

validate_all() takes schema/graph/prefixes as parameters, so no monkeypatching
is needed — the real JSON schema is loaded from disk; an empty rdflib.Graph()
(with empty prefix map) suppresses CURIE resolution so test fixtures can omit
maps_to without triggering ontology warnings.
"""

import json
from pathlib import Path

import pytest
import rdflib
import yaml

import tools.validate.validate_schemas as vs

# Load the real schema once — tests for validate_all() need it.
_SCHEMA_PATH = Path(__file__).resolve().parents[2] / "tools" / "schemas" / "instructions-schema.json"
SCHEMA = json.loads(_SCHEMA_PATH.read_text())


# ── Write helpers ─────────────────────────────────────────────────────────────


def _write_project_manifest(templates_dir: Path, *, phases=None, cross_phase_context=None) -> None:
    data = {
        "type": "project-manifest",
        "phases": phases or [],
        "cross_phase_context": cross_phase_context or [],
    }
    (templates_dir / "_project-manifest.yaml").write_text(yaml.dump(data))


def _write_phase_manifest(phase_dir: Path, *, with_transition: bool = True) -> None:
    data: dict = {
        "type": "phase-manifest",
        "completion": {"required_documents": [], "output_status": "draft"},
    }
    if with_transition:
        data["completion"]["transition_condition"] = "all docs done"
    (phase_dir / "_manifest.yaml").write_text(yaml.dump(data))


def _write_instructions(doc_dir: Path, gate_ids: list[str], *, required_gates: list[str] | None = None) -> None:
    """Write a schema-valid instructions.yaml with the given gate ids."""
    doc_dir.mkdir(parents=True, exist_ok=True)
    gates = [
        {
            "id": gid,
            "order": i + 1,
            "type": "string",
            "prompt": f"What is {gid}?",
            "fills": f"## {gid}",
            "required": True,
        }
        for i, gid in enumerate(gate_ids)
    ]
    data = {
        "version": 1,
        "document": doc_dir.name,
        "gates": gates,
        "completion": {
            "required_gates": required_gates or [gate_ids[0]],
            "output_status": "draft",
            "next_document": None,
        },
    }
    (doc_dir / "instructions.yaml").write_text(yaml.dump(data))


# ── Shared fixtures ───────────────────────────────────────────────────────────


@pytest.fixture()
def td(tmp_path, monkeypatch):
    """Temp directory wired as TEMPLATES_DIR for the duration of each test.

    REPO_ROOT is set to tmp_path.parent so that path.relative_to(REPO_ROOT)
    succeeds for any path under TEMPLATES_DIR (= tmp_path).
    """
    monkeypatch.setattr(vs, "TEMPLATES_DIR", tmp_path)
    monkeypatch.setattr(vs, "REPO_ROOT", tmp_path.parent)
    return tmp_path


@pytest.fixture()
def empty_ontology():
    """Empty RDF graph + empty prefix map — suppresses all CURIE checks."""
    return rdflib.Graph(), {}


# ── _gate_ids_for ─────────────────────────────────────────────────────────────


class TestGateIdsFor:
    def test_returns_ids_from_valid_file(self, tmp_path):
        _write_instructions(tmp_path / "doc", ["sponsor", "title"])
        result = vs._gate_ids_for(tmp_path / "doc" / "instructions.yaml")
        assert result == {"sponsor", "title"}

    def test_returns_none_on_invalid_yaml(self, tmp_path):
        bad = tmp_path / "bad.yaml"
        bad.write_text(": invalid: yaml: [")
        assert vs._gate_ids_for(bad) is None

    def test_returns_empty_set_for_no_gates(self, tmp_path):
        f = tmp_path / "empty.yaml"
        f.write_text(yaml.dump({"gates": []}))
        assert vs._gate_ids_for(f) == set()

    def test_skips_non_dict_gate_entries(self, tmp_path):
        f = tmp_path / "mixed.yaml"
        f.write_text(yaml.dump({"gates": [{"id": "real_gate"}, "not_a_dict", None]}))
        assert vs._gate_ids_for(f) == {"real_gate"}


# ── validate_project_manifest — check 1: file existence ──────────────────────


class TestCheck1FileExistence:
    def test_missing_manifest_returns_one_failure(self, td):
        passed, failed = vs.validate_project_manifest()
        assert (passed, failed) == (0, 1)

    def test_invalid_yaml_returns_one_failure(self, td):
        (td / "_project-manifest.yaml").write_text(": bad: yaml: [")
        passed, failed = vs.validate_project_manifest()
        assert (passed, failed) == (0, 1)

    def test_empty_file_treated_as_empty_manifest(self, td):
        # Empty file → `or {}` guard → no phases, no cross_phase_context → passes.
        # Check 6 finds no phase manifests on disk → no additional files.
        (td / "_project-manifest.yaml").write_text("")
        passed, failed = vs.validate_project_manifest()
        assert failed == 0


# ── validate_project_manifest — check 2: declared phases on disk ──────────────


class TestCheck2DeclaredPhasesOnDisk:
    def test_declared_phase_without_manifest_on_disk_fails(self, td):
        _write_project_manifest(td, phases=[{"id": "initiation"}])
        # No initiation/_manifest.yaml created.
        passed, failed = vs.validate_project_manifest()
        assert failed == 1  # project manifest ✗

    def test_declared_phase_with_manifest_passes(self, td):
        phase_dir = td / "initiation"
        phase_dir.mkdir()
        _write_phase_manifest(phase_dir)
        _write_project_manifest(td, phases=[{"id": "initiation"}])
        passed, failed = vs.validate_project_manifest()
        assert failed == 0

    def test_multiple_phases_one_missing_fails(self, td):
        (td / "initiation").mkdir()
        _write_phase_manifest(td / "initiation")
        # planning declared but no manifest on disk
        _write_project_manifest(td, phases=[{"id": "initiation"}, {"id": "planning"}])
        passed, failed = vs.validate_project_manifest()
        assert failed == 1  # project manifest ✗ (one error inside it)


# ── validate_project_manifest — check 3: undeclared phases on disk ────────────


class TestCheck3UndeclaredPhasesOnDisk:
    def test_phase_on_disk_not_listed_fails(self, td):
        phase_dir = td / "initiation"
        phase_dir.mkdir()
        _write_phase_manifest(phase_dir)
        _write_project_manifest(td, phases=[])  # initiation not listed
        passed, failed = vs.validate_project_manifest()
        # project manifest ✗ (check 3) + initiation phase ✓ (check 6)
        assert failed >= 1

    def test_all_disk_phases_declared_passes(self, td):
        for phase in ("initiation", "planning"):
            d = td / phase
            d.mkdir()
            _write_phase_manifest(d)
        _write_project_manifest(td, phases=[{"id": "initiation"}, {"id": "planning"}])
        passed, failed = vs.validate_project_manifest()
        assert failed == 0


# ── validate_project_manifest — check 4: first_captured_in resolves ──────────


class TestCheck4FirstCapturedInResolves:
    def test_path_not_found_fails(self, td):
        _write_project_manifest(
            td,
            cross_phase_context=[{"field": "sponsor", "first_captured_in": "initiation/proposal"}],
        )
        # instructions.yaml not created
        passed, failed = vs.validate_project_manifest()
        assert failed == 1

    def test_missing_slash_in_first_captured_in_fails(self, td):
        _write_project_manifest(
            td,
            cross_phase_context=[{"field": "sponsor", "first_captured_in": "no-slash-here"}],
        )
        passed, failed = vs.validate_project_manifest()
        assert failed == 1

    def test_valid_path_passes(self, td):
        _write_instructions(td / "initiation" / "proposal", ["sponsor"])
        _write_project_manifest(
            td,
            cross_phase_context=[{"field": "sponsor", "first_captured_in": "initiation/proposal"}],
        )
        passed, failed = vs.validate_project_manifest()
        assert failed == 0


# ── validate_project_manifest — check 5: field is a real gate id ─────────────


class TestCheck5FieldIsRealGateId:
    def test_field_not_in_gate_ids_fails(self, td):
        _write_instructions(td / "initiation" / "proposal", ["project_name", "objectives"])
        _write_project_manifest(
            td,
            cross_phase_context=[{"field": "sponsor", "first_captured_in": "initiation/proposal"}],
        )
        passed, failed = vs.validate_project_manifest()
        assert failed == 1

    def test_field_matches_gate_id_passes(self, td):
        _write_instructions(td / "initiation" / "proposal", ["project_name", "sponsor"])
        _write_project_manifest(
            td,
            cross_phase_context=[{"field": "sponsor", "first_captured_in": "initiation/proposal"}],
        )
        passed, failed = vs.validate_project_manifest()
        assert failed == 0

    def test_multiple_context_entries_one_bad_fails(self, td):
        _write_instructions(td / "initiation" / "proposal", ["project_name", "sponsor"])
        _write_project_manifest(
            td,
            cross_phase_context=[
                {"field": "project_name", "first_captured_in": "initiation/proposal"},
                {"field": "nonexistent", "first_captured_in": "initiation/proposal"},
            ],
        )
        passed, failed = vs.validate_project_manifest()
        assert failed == 1


# ── validate_project_manifest — check 6: transition_condition ────────────────


class TestCheck6TransitionCondition:
    def test_missing_transition_condition_fails(self, td):
        phase_dir = td / "initiation"
        phase_dir.mkdir()
        _write_phase_manifest(phase_dir, with_transition=False)
        _write_project_manifest(td, phases=[{"id": "initiation"}])
        passed, failed = vs.validate_project_manifest()
        assert failed == 1  # initiation phase manifest ✗

    def test_empty_phase_manifest_file_fails(self, td):
        # Empty file → `or {}` guard → no completion block → check fails.
        phase_dir = td / "initiation"
        phase_dir.mkdir()
        (phase_dir / "_manifest.yaml").write_text("")
        _write_project_manifest(td, phases=[{"id": "initiation"}])
        passed, failed = vs.validate_project_manifest()
        assert failed == 1

    def test_present_transition_condition_passes(self, td):
        phase_dir = td / "initiation"
        phase_dir.mkdir()
        _write_phase_manifest(phase_dir, with_transition=True)
        _write_project_manifest(td, phases=[{"id": "initiation"}])
        passed, failed = vs.validate_project_manifest()
        assert failed == 0

    def test_multiple_phases_one_missing_transition_fails(self, td):
        for phase, has_tc in (("initiation", True), ("planning", False)):
            d = td / phase
            d.mkdir()
            _write_phase_manifest(d, with_transition=has_tc)
        _write_project_manifest(td, phases=[{"id": "initiation"}, {"id": "planning"}])
        passed, failed = vs.validate_project_manifest()
        assert failed == 1  # only planning ✗


# ── validate_all — cross-reference checks ────────────────────────────────────


class TestValidateAllCrossRefChecks:
    """Cross-reference checks that JSON Schema draft-07 cannot enforce."""

    def _gate(self, gate_id: str, order: int = 1) -> dict:
        return {
            "id": gate_id,
            "order": order,
            "type": "string",
            "prompt": "Describe it.",
            "fills": f"## {gate_id}",
            "required": True,
        }

    def _doc(self, gate_ids: list[str], *, required_gates: list[str] | None = None) -> dict:
        return {
            "version": 1,
            "document": "test-doc",
            "gates": [self._gate(gid, i + 1) for i, gid in enumerate(gate_ids)],
            "completion": {
                "required_gates": required_gates or [gate_ids[0]],
                "output_status": "draft",
                "next_document": None,
            },
        }

    def _write(self, td: Path, data: dict) -> None:
        p = td / "phase" / "doc" / "instructions.yaml"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(yaml.dump(data))

    def test_valid_instructions_passes(self, td, empty_ontology):
        self._write(td, self._doc(["sponsor"]))
        graph, prefixes = empty_ontology
        passed, failed = vs.validate_all(SCHEMA, graph, prefixes)
        assert failed == 0
        assert passed == 1

    def test_duplicate_gate_ids_fails(self, td, empty_ontology):
        doc = self._doc(["sponsor"])
        doc["gates"].append(self._gate("sponsor", order=2))  # duplicate id
        self._write(td, doc)
        graph, prefixes = empty_ontology
        passed, failed = vs.validate_all(SCHEMA, graph, prefixes)
        assert failed == 1

    def test_required_gates_references_nonexistent_gate_fails(self, td, empty_ontology):
        doc = self._doc(["sponsor"], required_gates=["ghost_gate"])
        self._write(td, doc)
        graph, prefixes = empty_ontology
        passed, failed = vs.validate_all(SCHEMA, graph, prefixes)
        assert failed == 1

    def test_no_instructions_files_raises_systemexit(self, td, empty_ontology):
        # Empty TEMPLATES_DIR → validate_all calls sys.exit(1).
        graph, prefixes = empty_ontology
        with pytest.raises(SystemExit):
            vs.validate_all(SCHEMA, graph, prefixes)
