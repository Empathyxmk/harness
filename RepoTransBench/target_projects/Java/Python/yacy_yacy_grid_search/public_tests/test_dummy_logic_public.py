from yacy_grid_search.dummy_logic import DummyLogic

def test_add_different_numbers():
    d = DummyLogic()
    assert d.add(8, 7) == 15
    assert d.add(-2, -3) == -5
    assert d.add(15, -10) == 5
    assert d.add(10, -10) == 0
    assert d.add(-8, 8) == 0
    assert d.add(10, 4) == 14

def test_is_positive_different():
    d = DummyLogic()
    assert d.is_positive(1)
    assert not d.is_positive(-1)
    assert not d.is_positive(0)

def test_describe_different_data():
    d = DummyLogic()
    assert d.describe(-3, -3) == "equal"
    assert d.describe(12, 5) == "greater"
    assert d.describe(-10, 0) == "less"