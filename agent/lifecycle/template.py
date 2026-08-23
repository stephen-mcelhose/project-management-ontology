"""Template rendering — substitute {{gate_id}} placeholders with recorded answers."""

from __future__ import annotations

import re

_PLACEHOLDER = re.compile(r"\{\{(\w+)\}\}")


def render_template(template_text: str, answers: dict[str, str]) -> str:
    """Replace every {{gate_id}} in template_text with answers[gate_id].

    Missing keys (optional gates with no answer) are replaced with "".
    No placeholder syntax is left in the output.
    """
    def _replace(m: re.Match) -> str:
        return answers.get(m.group(1), "")

    return _PLACEHOLDER.sub(_replace, template_text)


def check_required_placeholders(
    template_text: str,
    required_gate_ids: list[str],
    answers: dict[str, str],
) -> list[str]:
    """Return required gate IDs that appear as {{gate_id}} in the template but
    are missing from answers. An empty list means it is safe to write.
    """
    in_template = {m.group(1) for m in _PLACEHOLDER.finditer(template_text)}
    return [
        gate_id
        for gate_id in required_gate_ids
        if gate_id in in_template and gate_id not in answers
    ]
