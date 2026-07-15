"""Domain models for the Mini ReAct agent."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Literal


class TerminationReason(StrEnum):
    """Why an agent run stopped."""

    COMPLETED = "completed"
    MAX_STEPS = "max_steps"
    INVALID_ACTION = "invalid_action"


@dataclass(frozen=True)
class Message:
    """A single chat message exchanged with the language model."""

    role: Literal["system", "user", "assistant"]
    content: str


@dataclass(frozen=True)
class StepRecord:
    """One observed model step and its tool outcome, if any."""

    step: int
    model_output: str
    action: str
    argument: str | None
    observation: str | None


@dataclass(frozen=True)
class AgentResult:
    """Structured result of a Mini ReAct run."""

    question: str
    steps: tuple[StepRecord, ...]
    final_answer: str | None
    termination_reason: TerminationReason
    steps_used: int
