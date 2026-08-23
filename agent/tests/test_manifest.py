"""Tests for agent/lifecycle/manifest.py."""

import pytest
import yaml

from agent.lifecycle.manifest import (
    DocumentEntry,
    PhaseManifest,
    ProjectManifest,
    load_phase_manifest,
    load_project_manifest,
)


# ── Fixtures ─────────────────────────────────────────────────────────────────


def write_phase_manifest(path, phase_id, docs, shared_context=None, next_phase=None):
    data = {
        "type": "phase-manifest",
        "phase": phase_id,
        "phase_label": phase_id.capitalize(),
        "documents": docs,
        "shared_context": shared_context or [],
        "completion": {
            "required_documents": [d["id"] for d in docs],
            "output_status": "draft",
            "next_phase": next_phase or "",
        },
    }
    (path / "_manifest.yaml").write_text(yaml.dump(data))


def write_project_manifest(templates_dir, phases):
    data = {
        "type": "project-manifest",
        "phases": phases,
    }
    (templates_dir / "_project-manifest.yaml").write_text(yaml.dump(data))


@pytest.fixture()
def templates_dir(tmp_path):
    td = tmp_path / "templates"
    td.mkdir()
    return td


# ── ProjectManifest ───────────────────────────────────────────────────────────


class TestLoadProjectManifest:
    def test_returns_phases_in_order(self, templates_dir):
        write_project_manifest(
            templates_dir,
            [{"id": "initiation"}, {"id": "planning"}, {"id": "closure"}],
        )
        pm = load_project_manifest(str(templates_dir))
        assert [p.id for p in pm.phases] == ["initiation", "planning", "closure"]

    def test_missing_file_raises_with_path(self, templates_dir):
        with pytest.raises(FileNotFoundError, match="_project-manifest.yaml"):
            load_project_manifest(str(templates_dir))

    def test_returns_project_manifest_type(self, templates_dir):
        write_project_manifest(templates_dir, [{"id": "initiation"}])
        pm = load_project_manifest(str(templates_dir))
        assert isinstance(pm, ProjectManifest)


# ── PhaseManifest ─────────────────────────────────────────────────────────────


class TestLoadPhaseManifest:
    def test_documents_sorted_by_phase_local_order(self, templates_dir):
        phase_dir = templates_dir / "initiation"
        phase_dir.mkdir()
        write_phase_manifest(
            phase_dir,
            "initiation",
            [
                {"id": "charter", "phase_local_order": 3, "title": "Charter",
                 "path": "templates/initiation/charter/", "dependencies": [], "required_before": []},
                {"id": "proposal", "phase_local_order": 1, "title": "Proposal",
                 "path": "templates/initiation/proposal/", "dependencies": [], "required_before": []},
                {"id": "business-case", "phase_local_order": 2, "title": "Business Case",
                 "path": "templates/initiation/business-case/", "dependencies": [], "required_before": []},
            ],
        )
        pm = load_phase_manifest(str(templates_dir), "initiation")
        assert [d.id for d in pm.documents] == ["proposal", "business-case", "charter"]

    def test_missing_file_raises(self, templates_dir):
        with pytest.raises(FileNotFoundError, match="initiation"):
            load_phase_manifest(str(templates_dir), "initiation")

    def test_returns_phase_manifest_type(self, templates_dir):
        phase_dir = templates_dir / "initiation"
        phase_dir.mkdir()
        write_phase_manifest(
            phase_dir,
            "initiation",
            [{"id": "proposal", "phase_local_order": 1, "title": "Proposal",
              "path": "templates/initiation/proposal/", "dependencies": [], "required_before": []}],
        )
        pm = load_phase_manifest(str(templates_dir), "initiation")
        assert isinstance(pm, PhaseManifest)

    def test_shared_context_loaded(self, templates_dir):
        phase_dir = templates_dir / "initiation"
        phase_dir.mkdir()
        write_phase_manifest(
            phase_dir,
            "initiation",
            [{"id": "proposal", "phase_local_order": 1, "title": "Proposal",
              "path": "templates/initiation/proposal/", "dependencies": [], "required_before": []}],
            shared_context=[{"field": "project_name", "maps_to": "dct:title",
                              "first_captured_in": "proposal"}],
        )
        pm = load_phase_manifest(str(templates_dir), "initiation")
        assert pm.shared_context[0]["field"] == "project_name"

    def test_completion_next_phase(self, templates_dir):
        phase_dir = templates_dir / "initiation"
        phase_dir.mkdir()
        write_phase_manifest(
            phase_dir,
            "initiation",
            [{"id": "proposal", "phase_local_order": 1, "title": "Proposal",
              "path": "templates/initiation/proposal/", "dependencies": [], "required_before": []}],
            next_phase="planning",
        )
        pm = load_phase_manifest(str(templates_dir), "initiation")
        assert pm.completion["next_phase"] == "planning"

    def test_document_entry_fields(self, templates_dir):
        phase_dir = templates_dir / "initiation"
        phase_dir.mkdir()
        write_phase_manifest(
            phase_dir,
            "initiation",
            [{"id": "proposal", "phase_local_order": 1, "title": "Proposal",
              "path": "templates/initiation/proposal/",
              "dependencies": ["dep-a"], "required_before": ["next-doc"]}],
        )
        pm = load_phase_manifest(str(templates_dir), "initiation")
        doc = pm.documents[0]
        assert isinstance(doc, DocumentEntry)
        assert doc.id == "proposal"
        assert doc.dependencies == ["dep-a"]
        assert doc.required_before == ["next-doc"]
