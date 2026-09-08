from py_linq.py_linq import Enumerable

def test_public_select_many_branch():
    source = Enumerable([[1, 2], [3]])
    r = list(source.select_many(lambda x: [y*2 for y in x]))
    assert r == [2, 4, 6]

def test_public_select_branch():
    source = Enumerable([3, 6, 9])
    r = list(source.select(lambda x: x * 4))
    assert r == [12, 24, 36]