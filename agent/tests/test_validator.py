"""Tests for agent/lifecycle/validator.py.

Uses minimal Turtle fixtures — no network, no external files.
"""

from pathlib import Path

import pytest

from agent.lifecycle.validator import ValidationResult, validate


# ── Turtle fixtures ───────────────────────────────────────────────────────────

# A minimal SHACL shape that requires ex:name on every ex:Thing
SHAPE_TTL = """\
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ex: <http://example.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:ThingShape
    a sh:NodeShape ;
    sh:targetClass ex:Thing ;
    sh:property [
        sh:path ex:name ;
        sh:minCount 1 ;
        sh:datatype xsd:string ;
    ] .
"""

VALID_DATA_TTL = """\
@prefix ex: <http://example.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:thing1 a ex:Thing ;
    ex:name "Widget"^^xsd:string .
"""

INVALID_DATA_TTL = """\
@prefix ex: <http://example.org/> .

ex:thing1 a ex:Thing .
"""


@pytest.fixture()
def shape_file(tmp_path):
    p = tmp_path / "shape.shacl.ttl"
    p.write_text(SHAPE_TTL)
    return p


@pytest.fixture()
def valid_doc(tmp_path):
    p = tmp_path / "valid.ttl"
    p.write_text(VALID_DATA_TTL)
    return p


@pytest.fixture()
def invalid_doc(tmp_path):
    p = tmp_path / "invalid.ttl"
    p.write_text(INVALID_DATA_TTL)
    return p


# ── Tests ─────────────────────────────────────────────────────────────────────


class TestValidate:
    def test_valid_document_passes(self, valid_doc, shape_file):
        result = validate(valid_doc, shape_file)
        assert isinstance(result, ValidationResult)
        assert result.passed is True
        assert result.messages == []

    def test_invalid_document_fails(self, invalid_doc, shape_file):
        result = validate(invalid_doc, shape_file)
        assert result.passed is False
        assert len(result.messages) > 0

    def test_missing_shape_returns_failure_not_exception(self, valid_doc, tmp_path):
        missing = tmp_path / "nonexistent.shacl.ttl"
        result = validate(valid_doc, missing)
        assert result.passed is False
        assert any("not found" in m.lower() or "nonexistent" in m for m in result.messages)

    def test_failure_is_data_not_exception(self, invalid_doc, shape_file):
        # Must NOT raise — returns ValidationResult
        result = validate(invalid_doc, shape_file)
        assert isinstance(result, ValidationResult)

    def test_missing_data_file_returns_failure(self, tmp_path, shape_file):
        missing = tmp_path / "missing.ttl"
        result = validate(missing, shape_file)
        assert result.passed is False
