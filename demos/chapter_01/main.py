"""Chapter 01 demo: Mini ReAct with a scripted model and stub Search."""

from __future__ import annotations

from deep_research.agents.react import MiniReActAgent
from deep_research.llms.scripted import ScriptedLLM
from deep_research.tools.stub_search import StubSearch

DEMO_KNOWLEDGE = {
    "deep research definition": (
        "Deep Research agents plan multi-step investigations, call tools repeatedly, "
        "and synthesize cited findings instead of answering from a single search."
    ),
    "why react is not enough": (
        "Plain ReAct can lose long-horizon context; later chapters add IterResearch, "
        "checkpoints, and evolving reports."
    ),
}


def build_demo_agent(*, max_steps: int = 5) -> MiniReActAgent:
    """Create the default offline demo agent."""
    llm = ScriptedLLM(
        [
            'search("deep research definition")',
            'search("why react is not enough")',
            (
                'final("Deep Research needs multi-step tool use and synthesis; '
                'Mini ReAct shows the loop before richer state management.")'
            ),
        ]
    )
    search = StubSearch(DEMO_KNOWLEDGE)
    return MiniReActAgent(llm, search, max_steps=max_steps)


def main() -> None:
    question = "Why do we need Deep Research agents instead of one-shot search?"
    agent = build_demo_agent()
    result = agent.run(question)

    print(f"Question: {result.question}")
    print(f"Steps used: {result.steps_used}")
    print(f"Termination: {result.termination_reason.value}")
    print()
    for step in result.steps:
        print(f"Step {step.step}")
        if step.argument is not None:
            print(f"  Action: {step.action}({step.argument!r})")
        else:
            print(f"  Action: {step.action}")
        if step.observation is not None:
            print(f"  Observation: {step.observation}")
        print()
    print(f"Final answer: {result.final_answer}")


if __name__ == "__main__":
    main()
