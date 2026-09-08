import pytest

def increment_by_five(x):
    return x + 5

def test_PublicAwaitersTest_IncrementSmall():
    assert increment_by_five(3) == 8
    assert increment_by_five(0) == 5

def test_PublicAwaitersTest_IncrementNegative():
    assert increment_by_five(-10) == -5
    assert increment_by_five(-7) == -2

def test_PublicAwaitersTest_VectorInc():
    v = [2, 4, 6]
    v = [increment_by_five(x) for x in v]
    assert v[0] == 7
    assert v[1] == 9
    assert v[2] == 11