import pytest
from yacy_grid_search.dummy_logic import DummyLogic

def test_add():
    d = DummyLogic()
    assert d.add(3, 4) == 7
    assert d.add(-3, -4) == -7
    assert d.add(-3, 3) == 0
    assert d.add(0, 0) == 0
    assert d.add(-3, 3) == 0
    assert d.add(3, -3) == 0

def test_is_positive():
    d = DummyLogic()
    assert d.is_positive(10)
    assert not d.is_positive(0)
    assert not d.is_positive(-4)

def test_describe():
    d = DummyLogic()
    assert d.describe(5, 5) == "equal"
    assert d.describe(7, 2) == "greater"
    assert d.describe(3, 7) == "less"