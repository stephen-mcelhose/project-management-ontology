"""LLM-as-judge for eval assertions.

Used in --run-evals mode to evaluate whether a recorded gate answer faithfully
captures the relevant information from the user's messages. Exact string match
is wrong for this — the model always paraphrases free-text gates.

The phase gate map (same structure returned by get_phase_gates) defines what
each gate owns. The judge uses that map — not ad-hoc rules — to decide whether
recorded content belongs to the gate under test.
"""

from __future__ import annotations

from dataclasses import dataclass

from google import genai
from google.genai import types

_JUDGE_PROMPT = """\
You are evaluating whether an AI assistant correctly captured user information \
for one gate in a document workflow.

Phase gate map (from get_phase_gates — defines what each gate owns):
{phase_gates}

Gate under evaluation:
  document: {doc_id}
  gate id: {gate_id}
  prompt: {gate_prompt}

User messages (all turns, in order):
{user_turns}

What the assistant recorded for this gate:
{recorded_answer}

Did the assistant faithfully capture the user-stated facts that answer THIS \
gate's prompt, without hallucinating facts not in the user's messages? Use the \
phase gate map to determine which facts belong to this gate versus other gates.

Respond with exactly one line: PASS or FAIL, a colon, then one sentence of reasoning.
Example: PASS: The recorded answer accurately reflects the user's stated timeline.
"""


def _format_phase_gates(phase_gates: dict[str, dict[str, str]]) -> str:
    lines: list[str] = []
    for doc_id in sorted(phase_gates):
        lines.append(f"  {doc_id}:")
        for gate_id, prompt in phase_gates[doc_id].items():
            lines.append(f"    {gate_id}: {prompt}")
    return "\n".join(lines)


@dataclass
class JudgeVerdict:
    passed: bool
    reasoning: str
    gate_id: str
    doc_id: str


def judge_gate_answer(
    *,
    doc_id: str,
    gate_id: str,
    gate_prompt: str,
    phase_gates: dict[str, dict[str, str]],
    user_turns: list[str],
    recorded_answer: str | None,
    model: str | None = None,
) -> JudgeVerdict:
    """Call an LLM to assess whether recorded_answer faithfully captures the gate.

    Returns a JudgeVerdict with passed=True if the judge says PASS.
    A None recorded_answer is an automatic FAIL.
    Uses Settings().model when model is not supplied (same as the agent).
    """
    if recorded_answer is None:
        return JudgeVerdict(
            passed=False,
            reasoning="Gate was never recorded (answer is None).",
            gate_id=gate_id,
            doc_id=doc_id,
        )

    if model is None:
        from agent.settings import Settings

        model = Settings().model

    turns_text = "\n".join(f"  Turn {i + 1}: {t.strip()}" for i, t in enumerate(user_turns))
    prompt = _JUDGE_PROMPT.format(
        phase_gates=_format_phase_gates(phase_gates),
        doc_id=doc_id,
        gate_id=gate_id,
        gate_prompt=gate_prompt,
        user_turns=turns_text,
        recorded_answer=recorded_answer,
    )

    client = genai.Client()
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0),
    )
    raw = response.text.strip()
    passed = raw.upper().startswith("PASS")
    reasoning = raw.split(":", 1)[-1].strip() if ":" in raw else raw

    return JudgeVerdict(passed=passed, reasoning=reasoning, gate_id=gate_id, doc_id=doc_id)
