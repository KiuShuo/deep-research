"""Scripted language model for deterministic demos and tests."""

from __future__ import annotations

from collections.abc import Sequence

from deep_research.core.models import Message


class ScriptedLLM:
    """Returns prewritten responses in order; ignores message content."""

    def __init__(self, responses: Sequence[str]) -> None:
        if not responses:
            raise ValueError("responses must not be empty")
        self._responses = list(responses)
        self._index = 0
        self.call_count = 0

    def complete(self, messages: Sequence[Message]) -> str:
        """Return the next scripted response."""
        _ = messages  # Scripted responses are independent of prompt content.
        if self._index >= len(self._responses):
            raise RuntimeError(f"ScriptedLLM exhausted after {len(self._responses)} response(s)")
        response = self._responses[self._index]
        self._index += 1
        self.call_count += 1
        return response
