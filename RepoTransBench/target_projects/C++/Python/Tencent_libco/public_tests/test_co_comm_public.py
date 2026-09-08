"""
Test macro wrappers like co_align, co_min, co_max, co_swap.

Corresponds to C++: tests/test_co_comm_public.cpp
"""

import pytest

def co_align(v, a):
    return ((v + a - 1) & ~(a - 1))

def co_min(a, b):
    return a if a < b else b

def co_max(a, b):
    return a if a > b else b

def co_swap(a, b):
    return b, a

def test_alignment():
    # Use the same test inputs as in C++
    v1, a1 = 21, 8
    assert co_align(v1, a1) == 24

    v2, a2 = 113, 32
    assert co_align(v2, a2) == 128

    v3, a3 = 0, 8
    assert co_align(v3, a3) == 0

    v4, a4 = 71, 9
    assert co_align(v4, a4) == 72

def test_min_max():
    assert co_min(40, 100) == 40
    assert co_min(-70, -41) == -70

    assert co_max(10, 8) == 10
    assert co_max(-22, -18) == -18

def test_swap():
    x, y = 321, 123
    x, y = co_swap(x, y)
    assert x == 123
    assert y == 321

    a, b = 5.5, -3.3
    a, b = co_swap(a, b)
    assert a == -3.3
    assert b == 5.5