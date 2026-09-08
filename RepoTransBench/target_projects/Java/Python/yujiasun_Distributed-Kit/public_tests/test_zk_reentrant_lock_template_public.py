def test_basic_locking_public():
    x = 42
    y = 58
    assert x + y == 100
    assert x != y