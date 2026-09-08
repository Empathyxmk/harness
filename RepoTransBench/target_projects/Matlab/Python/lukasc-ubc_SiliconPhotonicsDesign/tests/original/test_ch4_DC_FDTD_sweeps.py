import pytest

def dummy_sweep(a, b):
    if len(a) == 0 or len(b) == 0:
        return 0
    else:
        return sum([i + j for i, j in zip(a, b)])

def test_sweep_success():
    x = [1, 2, 3]
    y = [4, 5, 6]
    res = dummy_sweep(x, y)
    assert res == sum([i + j for i, j in zip(x, y)])

def test_empty_input():
    res = dummy_sweep([], [])
    assert res == 0