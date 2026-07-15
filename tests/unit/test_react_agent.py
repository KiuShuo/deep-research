"""Unit tests for the Mini ReAct agent."""

from __future__ import annotations

import pytest

from deep_research.agents.react import MiniReActAgent, parse_action
from deep_research.core.models import TerminationReason
from deep_research.llms.scripted import ScriptedLLM
from deep_research.tools.stub_search import StubSearch


def _knowledge() -> StubSearch:
    return StubSearch(
        {
            "deep research": "Deep Research combines planning, multi-step search, and synthesis.",
            "react loop": "ReAct alternates reasoning traces with tool actions.",
        }
    )


def test_completed_path_runs_two_searches_then_final() -> None:
    llm = ScriptedLLM(
        [
            'search("deep research")',
            'search("react loop")',
            'final("Plan, search repeatedly, then synthesize with citations.")',
        ]
    )
    agent = MiniReActAgent(llm, _knowledge(), max_steps=5)

    result = agent.run("What is Deep Research?")

    assert result.termination_reason == TerminationReason.COMPLETED
    assert result.steps_used == 3
    assert result.final_answer == "Plan, search repeatedly, then synthesize with citations."
    assert [step.action for step in result.steps] == ["search", "search", "final"]
    assert [step.argument for step in result.steps[:2]] == ["deep research", "react loop"]
    assert result.steps[0].observation is not None
    assert "planning" in result.steps[0].observation
    assert result.steps[1].observation is not None
    assert "ReAct" in result.steps[1].observation
    assert llm.call_count == 3


def test_max_steps_stops_without_extra_model_or_search_calls() -> None:
    class CountingSearch:
        def __init__(self) -> None:
            self.calls: list[str] = []

        def search(self, query: str) -> str:
            self.calls.append(query)
            return f"hit:{query}"

    llm = ScriptedLLM(
        [
            'search("q1")',
            'search("q2")',
            'search("q3")',
            'search("should-not-run")',
        ]
    )
    search = CountingSearch()
    agent = MiniReActAgent(llm, search, max_steps=3)

    result = agent.run("Keep searching")

    assert result.termination_reason == TerminationReason.MAX_STEPS
    assert result.final_answer is None
    assert result.steps_used == 3
    assert llm.call_count == 3
    assert search.calls == ["q1", "q2", "q3"]
    assert all(step.action == "search" for step in result.steps)


def test_final_on_last_budgeted_step_completes() -> None:
    llm = ScriptedLLM(
        [
            'search("deep research")',
            'final("Answer on the last allowed step.")',
        ]
    )
    agent = MiniReActAgent(llm, _knowledge(), max_steps=2)

    result = agent.run("Finish on the budget edge")

    assert result.termination_reason == TerminationReason.COMPLETED
    assert result.steps_used == 2
    assert result.final_answer == "Answer on the last allowed step."


def test_invalid_max_steps_rejected() -> None:
    llm = ScriptedLLM(['final("x")'])
    search = _knowledge()

    with pytest.raises(ValueError, match="positive integer"):
        MiniReActAgent(llm, search, max_steps=0)
    with pytest.raises(ValueError, match="positive integer"):
        MiniReActAgent(llm, search, max_steps=-1)


def test_empty_and_unknown_actions_terminate_as_invalid() -> None:
    cases = [
        'search("")',
        'final("")',
        "not-an-action",
        'browse("url")',
        'search("q"); import os',
    ]
    for output in cases:
        llm = ScriptedLLM([output])
        agent = MiniReActAgent(llm, _knowledge(), max_steps=3)
        result = agent.run("bad action")
        assert result.termination_reason == TerminationReason.INVALID_ACTION
        assert result.final_answer is None
        assert result.steps[0].action == "invalid"


def test_whitespace_only_search_terminates_invalid_without_search_calls() -> None:
    """Whitespace-only search args must be rejected and never reach the tool."""

    class CountingSearch:
        def __init__(self) -> None:
            self.calls: list[str] = []

        def search(self, query: str) -> str:
            self.calls.append(query)
            return f"hit:{query}"

    cases = [
        'search("   ")',
        'search("\t")',
        'search(" \n ")',
    ]
    for output in cases:
        llm = ScriptedLLM([output])
        search = CountingSearch()
        agent = MiniReActAgent(llm, search, max_steps=3)

        result = agent.run("blank query")

        assert result.termination_reason == TerminationReason.INVALID_ACTION
        assert result.final_answer is None
        assert result.steps_used == 1
        assert result.steps[0].action == "invalid"
        assert result.steps[0].argument is None
        assert search.calls == []


def test_whitespace_only_final_terminates_invalid() -> None:
    """Whitespace-only final answers must be invalid, not spurious completions."""

    class CountingSearch:
        def __init__(self) -> None:
            self.calls: list[str] = []

        def search(self, query: str) -> str:
            self.calls.append(query)
            return f"hit:{query}"

    cases = [
        'final("   ")',
        'final("\t")',
        'final(" \n ")',
    ]
    for output in cases:
        llm = ScriptedLLM([output])
        search = CountingSearch()
        agent = MiniReActAgent(llm, search, max_steps=3)

        result = agent.run("blank answer")

        assert result.termination_reason == TerminationReason.INVALID_ACTION
        assert result.final_answer is None
        assert result.steps_used == 1
        assert result.steps[0].action == "invalid"
        assert search.calls == []


def test_observation_is_appended_to_next_model_context() -> None:
    from collections.abc import Sequence

    from deep_research.core.models import Message

    captured: list[list[str]] = []

    class CapturingLLM:
        def __init__(self) -> None:
            self._responses = [
                'search("deep research")',
                'final("done")',
            ]
            self.call_count = 0

        def complete(self, messages: Sequence[Message]) -> str:
            captured.append([message.content for message in messages])
            response = self._responses[self.call_count]
            self.call_count += 1
            return response

    llm = CapturingLLM()
    agent = MiniReActAgent(llm, _knowledge(), max_steps=3)
    agent.run("trace observations")

    assert len(captured) == 2
    assert any(
        content.startswith("Observation:") and "planning" in content for content in captured[1]
    )


def test_parse_action_rejects_executable_payloads() -> None:
    assert parse_action('search("safe")') == ("search", "safe")
    assert parse_action('final("答案")') == ("final", "答案")
    assert parse_action('final("say \\"hi\\"")') == ("final", 'say "hi"')
    assert parse_action("__import__('os').system('rm -rf /')") is None
    assert parse_action("search(query)") is None
