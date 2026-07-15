"""Versioned prompts for agent loops.

Keep model instructions here so business code only references constants.
"""

MINI_REACT_SYSTEM_PROMPT = (
    "You are a research agent. Reply with exactly one action per turn: "
    'search("query") or final("answer").'
)
