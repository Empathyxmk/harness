import pytest
from protofuzz import protofuzz
from types import SimpleNamespace

def test_message_strategy_smoke():
    strat = protofuzz.message_strategy(SimpleNamespace, {"x": lambda t, f=None: iter([1])})
    g = strat()
    # Must return an instance of SimpleNamespace
    msg = next(g)
    assert isinstance(msg, SimpleNamespace)

def test_fuzz_smoke(monkeypatch):
    # Create dummy generator
    def dummy_generator(*a, **k):
        yield "A"
        yield "B"
        yield "C"
    strat = lambda: dummy_generator()
    results = []
    def collect(msg):
        results.append(msg)
    protofuzz.fuzz(strat, collect, max_tests=3)
    assert results == ["A", "B", "C"]