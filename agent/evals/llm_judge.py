"""LLM-as-judge for eval assertions.

Used in --run-evals mode to evaluate whether a recorded gate answer faithfully
captures the relevant information from the user's messages. Exact string match
is wrong for this — the model always paraphrases free-text gates.

Usage::

    from agent.evals.llm_judge import judge_gate_answer

    verdict = judge_gate_answer(
        gate_id="problem_statement",
        gate_prompt="What problem does this project solve?",
        user_turns=["We have a 15-year-old ERP..."],
        recorded_answer="A 15-year-old ERP integration causes 3-4h downtime monthly.",
    )
    assert verdict.passed, verdict.reasoning
"""

from __future__ import annotations

from dataclasses import dataclass

from google import genai
from google.genai import types

_JUDGE_PROMPT = """\
You are evaluating whether an AI assistant correctly captured information from a \
user's messages.

Gate id: {gate_id}
Gate question: {gate_prompt}

User messages (all turns, in order):
{user_turns}

What the assistant recorded:
{recorded_answer}

Did the assistant faithfully and completely capture the information relevant to \
this gate, without hallucinating facts not present in the user's messages?

Respond with exactly one line: PASS or FAIL, a colon, then one sentence of reasoning.
Example: PASS: The recorded answer accurately reflects the user's stated timeline.
"""


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
    user_turns: list[str],
    recorded_answer: str | None,
    model: str = "gemini-2.0-flash",
) -> JudgeVerdict:
    """Call an LLM to assess whether recorded_answer faithfully captures the gate.

    Returns a JudgeVerdict with passed=True if the judge says PASS.
    A None recorded_answer is an automatic FAIL.
    """
    if recorded_answer is None:
        return JudgeVerdict(
            passed=False,
            reasoning="Gate was never recorded (answer is None).",
            gate_id=gate_id,
            doc_id=doc_id,
        )

    turns_text = "\n".join(f"  Turn {i + 1}: {t.strip()}" for i, t in enumerate(user_turns))
    prompt = _JUDGE_PROMPT.format(
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
