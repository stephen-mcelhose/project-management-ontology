"""Tests for agent/lifecycle/template.py."""


from agent.lifecycle.template import check_required_placeholders, render_template


class TestRenderTemplate:
    def test_replaces_all_placeholders(self):
        tmpl = "# {{project_name}}\n\n{{problem_statement}}"
        result = render_template(tmpl, {"project_name": "Acme", "problem_statement": "Things break."})
        assert result == "# Acme\n\nThings break."

    def test_optional_missing_becomes_empty_string(self):
        tmpl = "Required: {{req}}\nOptional: {{opt}}"
        result = render_template(tmpl, {"req": "yes"})
        assert result == "Required: yes\nOptional: "

    def test_no_leftover_placeholder_syntax(self):
        tmpl = "{{a}} and {{b}}"
        result = render_template(tmpl, {"a": "A"})
        assert "{{" not in result
        assert "}}" not in result

    def test_multiple_occurrences_of_same_placeholder(self):
        tmpl = "{{name}} is {{name}}"
        result = render_template(tmpl, {"name": "Echo"})
        assert result == "Echo is Echo"

    def test_empty_template_returns_empty(self):
        assert render_template("", {}) == ""

    def test_no_placeholders_returns_unchanged(self):
        tmpl = "No placeholders here."
        assert render_template(tmpl, {"x": "y"}) == tmpl

    def test_answer_with_special_chars(self):
        tmpl = "{{value}}"
        result = render_template(tmpl, {"value": "a & b < c > d"})
        assert result == "a & b < c > d"


class TestCheckRequiredPlaceholders:
    def test_returns_empty_when_all_answered(self):
        tmpl = "{{a}} {{b}}"
        missing = check_required_placeholders(tmpl, required_gate_ids=["a", "b"], answers={"a": "x", "b": "y"})
        assert missing == []

    def test_returns_missing_gate_ids(self):
        tmpl = "{{a}} {{b}} {{c}}"
        missing = check_required_placeholders(tmpl, required_gate_ids=["a", "b"], answers={"a": "x"})
        assert missing == ["b"]

    def test_required_gate_not_in_template_not_flagged(self):
        # If a required gate ID doesn't appear in the template at all, it's fine
        tmpl = "{{a}}"
        missing = check_required_placeholders(tmpl, required_gate_ids=["a", "z"], answers={"a": "x"})
        assert missing == []

    def test_empty_answers_returns_all_required_in_template(self):
        tmpl = "{{a}} {{b}}"
        missing = check_required_placeholders(tmpl, required_gate_ids=["a", "b"], answers={})
        assert set(missing) == {"a", "b"}
