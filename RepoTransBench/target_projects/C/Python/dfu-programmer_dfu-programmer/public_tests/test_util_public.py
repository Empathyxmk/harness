import pytest
from src import util

def test_min_different_values():
    """
    Corresponds to C's test_min_different_values in test_util_public.c.
    Tests the min utility function with various integer inputs.
    """
    assert util.min(10, 8) == 8
    assert util.min(8, 10) == 8
    assert util.min(-10, 10) == -10
    assert util.min(5, 5) == 5 # Added case for equal values

def test_max_different_values():
    """
    Corresponds to C's test_max_different_values in test_util_public.c.
    Tests the max utility function with various integer inputs.
    """
    assert util.max(-15, 4) == 4
    assert util.max(4, -15) == 4
    assert util.max(-20, -7) == -7
    assert util.max(5, 5) == 5 # Added case for equal values

def test_clamp_different_cases():
    """
    Corresponds to C's test_clamp_different_cases in test_util_public.c.
    Tests the clamp utility function with values inside, below, above, and at boundaries.
    """
    assert util.clamp(7, 3, 9) == 7      # inside
    assert util.clamp(-5, 0, 12) == 0    # below
    assert util.clamp(30, 6, 26) == 26   # above
    assert util.clamp(6, 6, 6) == 6      # all equal
    assert util.clamp(17, 12, 16) == 16  # just above
    assert util.clamp(11, 12, 16) == 12  # just below