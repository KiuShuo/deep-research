"""In-memory stub Search tool for local demos and unit tests."""

from __future__ import annotations

from collections.abc import Mapping


class StubSearch:
    """Deterministic search tool backed by an in-memory knowledge map.

    Unknown queries return a stable, explainable fallback instead of raising.
    """

    def __init__(self, knowledge: Mapping[str, str] | None = None) -> None:
        self._knowledge = dict(knowledge or {})

    def search(self, query: str) -> str:
        """Return the mapped answer for ``query``, or a stable fallback."""
        normalized = query.strip()
        if normalized in self._knowledge:
            return self._knowledge[normalized]
        return (
            f'No stub result for query="{normalized}". '
            "Try a known topic from the demo knowledge base."
        )
