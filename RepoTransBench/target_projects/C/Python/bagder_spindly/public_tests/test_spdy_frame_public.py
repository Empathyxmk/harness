# public_tests/test_spdy_frame_public.py
import pytest

def sample_sum(a: int, b: int) -> int:
    """Simulate a simple sum function."""
    return a + b

def test_spdy_frame_public_sample_sum():
    """
    Corresponds to tests/test_spdy_frame_public.c.
    Tests sample_sum with different values.
    """
    assert sample_sum(11, 29) == 40
    assert sample_sum(-21, 20) == -1
    assert sample_sum(100, -75) == 25