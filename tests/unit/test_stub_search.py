"""Unit tests for the in-memory stub Search tool."""

from deep_research.tools.stub_search import StubSearch


def test_stub_search_returns_known_result() -> None:
    search = StubSearch({"alpha papers": "AlphaFold related papers."})

    assert search.search("alpha papers") == "AlphaFold related papers."


def test_stub_search_returns_stable_fallback_for_unknown_query() -> None:
    search = StubSearch({"known": "value"})

    first = search.search("missing topic")
    second = search.search("missing topic")

    assert first == second
    assert 'query="missing topic"' in first
    assert "No stub result" in first


def test_stub_search_strips_query_whitespace_for_lookup() -> None:
    search = StubSearch({"exact": "matched"})

    assert search.search("  exact  ") == "matched"
