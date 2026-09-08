"""
Stub test for public visibility; use different, simple numbers.

Corresponds to C++: tests/test_stub_co_routine_public.cpp
"""

import pytest

def test_basic_arithmetic():
    assert 6 + 7 == 13
    assert 16 > 5
    assert not (3 * 3 == 8)