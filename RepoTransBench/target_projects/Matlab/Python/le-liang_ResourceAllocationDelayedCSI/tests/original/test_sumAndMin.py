import numpy as np
from tests.original.sumAndMin_helper import sumAndMin

def test_sumAndMin_simple_vector():
    s, m = sumAndMin([1, 2, 3])
    assert s == 6 and m == 1

def test_sumAndMin_negative_elements():
    s, m = sumAndMin([-2, 0, 4])
    assert s == 2 and m == -2

def test_sumAndMin_single_element():
    s, m = sumAndMin([4])
    assert s == 4 and m == 4

def test_sumAndMin_empty_input():
    s, m = sumAndMin([])
    assert s == 0 and m is None