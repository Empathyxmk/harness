import pytest
from protofuzz import protofuzz
from types import SimpleNamespace

def test_message_strategy_public():
    # Use different field name and value than in the original test
    strat = protofuzz.message_strategy(SimpleNamespace, {"y": lambda t, f=None: iter([42])})
    g = strat()
    msg = next(g)
    assert isinstance(msg, SimpleNamespace)
    assert hasattr(msg, "y")
    assert msg.y == 42

def test_fuzz_public(monkeypatch):
    # Create dummy generator that yields new unique values
    def dummy_generator(*a, **k):
        yield "D"
        yield "E"
        yield "F"
    strat = lambda: dummy_generator()
    results = []
    def collect(msg):
        results.append(msg)
    protofuzz.fuzz(strat, collect, max_tests=3)
    assert results == ["D", "E", "F"]