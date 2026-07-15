"""Minimal ReAct agent with explicit search/final actions and step budget."""

from __future__ import annotations

import re
from collections.abc import Sequence
from typing import Protocol

from deep_research.agents.prompts import MINI_REACT_SYSTEM_PROMPT
from deep_research.core.models import AgentResult, Message, StepRecord, TerminationReason

_ACTION_PATTERN = re.compile(
    r'^(?P<name>search|final)\("(?P<arg>(?:[^"\\]|\\.)*)"\)$',
)


class LanguageModel(Protocol):
    """Model that turns a message list into one text response."""

    def complete(self, messages: Sequence[Message]) -> str:
        """Generate the next model output."""


class SearchTool(Protocol):
    """Search tool that returns a textual observation for a query."""

    def search(self, query: str) -> str:
        """Execute one search and return a structured observation string."""


def _unescape_argument(raw: str) -> str:
    """Unescape only ``\\\\`` and ``\\"`` sequences inside action arguments."""
    parts: list[str] = []
    index = 0
    while index < len(raw):
        char = raw[index]
        if char == "\\" and index + 1 < len(raw):
            parts.append(raw[index + 1])
            index += 2
            continue
        parts.append(char)
        index += 1
    return "".join(parts)


def parse_action(text: str) -> tuple[str, str] | None:
    """Parse ``search("...")`` or ``final("...")`` without evaluating code.

    Returns ``(name, argument)`` or ``None`` when the text is not a valid action.
    Empty or whitespace-only arguments after unescaping are rejected.
    """
    stripped = text.strip()
    match = _ACTION_PATTERN.fullmatch(stripped)
    if match is None:
        return None
    argument = _unescape_argument(match.group("arg"))
    if argument.strip() == "":
        return None
    return match.group("name"), argument


class MiniReActAgent:
    """Run a small Think → Act → Observe loop with a hard step limit."""

    def __init__(
        self,
        llm: LanguageModel,
        search: SearchTool,
        *,
        max_steps: int,
    ) -> None:
        if not isinstance(max_steps, int) or isinstance(max_steps, bool) or max_steps < 1:
            raise ValueError("max_steps must be a positive integer")
        self._llm = llm
        self._search = search
        self._max_steps = max_steps

    def run(self, question: str) -> AgentResult:
        """Execute the ReAct loop for ``question`` until completion or budget."""
        messages: list[Message] = [
            Message(role="system", content=MINI_REACT_SYSTEM_PROMPT),
            Message(role="user", content=question),
        ]
        steps: list[StepRecord] = []

        for step_number in range(1, self._max_steps + 1):
            model_output = self._llm.complete(messages)
            messages.append(Message(role="assistant", content=model_output))

            parsed = parse_action(model_output)
            if parsed is None:
                steps.append(
                    StepRecord(
                        step=step_number,
                        model_output=model_output,
                        action="invalid",
                        argument=None,
                        observation=None,
                    )
                )
                return AgentResult(
                    question=question,
                    steps=tuple(steps),
                    final_answer=None,
                    termination_reason=TerminationReason.INVALID_ACTION,
                    steps_used=step_number,
                )

            action_name, argument = parsed

            if action_name == "final":
                steps.append(
                    StepRecord(
                        step=step_number,
                        model_output=model_output,
                        action="final",
                        argument=argument,
                        observation=None,
                    )
                )
                return AgentResult(
                    question=question,
                    steps=tuple(steps),
                    final_answer=argument,
                    termination_reason=TerminationReason.COMPLETED,
                    steps_used=step_number,
                )

            observation = self._search.search(argument)
            steps.append(
                StepRecord(
                    step=step_number,
                    model_output=model_output,
                    action="search",
                    argument=argument,
                    observation=observation,
                )
            )
            messages.append(
                Message(
                    role="user",
                    content=f"Observation: {observation}",
                )
            )

            if step_number == self._max_steps:
                return AgentResult(
                    question=question,
                    steps=tuple(steps),
                    final_answer=None,
                    termination_reason=TerminationReason.MAX_STEPS,
                    steps_used=step_number,
                )

        # Unreachable: the loop always returns on the final budgeted step.
        raise RuntimeError("MiniReActAgent exited without a termination reason")
