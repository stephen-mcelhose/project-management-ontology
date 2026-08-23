"""ScriptedModel — a BaseLlm subclass for deterministic testing.

Registered as "scripted-.*" so LlmAgent(model="scripted-fake") resolves it.
Uses a class-level queue so responses survive the LLMRegistry singleton dance.

Usage::

    from agent.evals.scripted_model import ScriptedModel, tool_response, text_response
    from google.adk.models.registry import LLMRegistry

    LLMRegistry.register(ScriptedModel)
    ScriptedModel.load([
        tool_response("get_progress", {}),
        text_response("What is the project name?"),
    ])
    # Then build_agent(..., model="scripted-fake")
"""

from __future__ import annotations

from collections import deque
from typing import AsyncGenerator

from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types


# ── Helpers ───────────────────────────────────────────────────────────────────


def tool_response(name: str, args: dict) -> LlmResponse:
    """Build an LlmResponse that invokes a tool."""
    fc = types.FunctionCall(name=name, args=args)
    content = types.Content(parts=[types.Part(function_call=fc)], role="model")
    return LlmResponse(content=content)


def text_response(text: str) -> LlmResponse:
    """Build an LlmResponse with plain text (signals end of turn)."""
    content = types.Content(parts=[types.Part(text=text)], role="model")
    return LlmResponse(content=content, turn_complete=True)


# ── ScriptedModel ─────────────────────────────────────────────────────────────

_QUEUE: deque[LlmResponse] = deque()


class ScriptedModel(BaseLlm):
    """Fake LLM that pops scripted responses from a shared class-level queue.

    Each generate_content_async call pops exactly one response.
    IndexError on empty queue makes script exhaustion obvious in test output.
    """

    @classmethod
    def supported_models(cls) -> list[str]:
        return ["scripted-.*"]

    @classmethod
    def load(cls, responses: list[LlmResponse]) -> None:
        """Replace the queue with a fresh list of scripted responses."""
        _QUEUE.clear()
        _QUEUE.extend(responses)

    @classmethod
    def remaining(cls) -> int:
        return len(_QUEUE)

    async def generate_content_async(
        self, llm_request: LlmRequest, stream: bool = False
    ) -> AsyncGenerator[LlmResponse, None]:
        if not _QUEUE:
            raise IndexError(
                "ScriptedModel queue is empty — the agent made more model "
                "invocations than were scripted. Check scripted_responses in "
                "the eval case YAML."
            )
        yield _QUEUE.popleft()
