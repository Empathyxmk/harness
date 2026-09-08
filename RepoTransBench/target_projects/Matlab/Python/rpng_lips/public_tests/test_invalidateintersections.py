import pytest
import numpy as np

from src.lips.invalidateintersections import invalidateintersections

def test_all_false_public():
    valid = [False, False, False]
    arr = np.array([100, 101, 102], dtype=float)
    arr_out = invalidateintersections(arr.copy(), valid)
    assert np.all(np.isnan(arr_out))

def test_mixed_valid_public():
    valid = [True, False, True, False]
    arr = np.array([12, 14, 15, 99], dtype=float)
    arr_out = invalidateintersections(arr.copy(), valid)
    assert np.all(np.isnan(arr_out) == np.array([False, True, False, True]))
    assert np.all(arr_out[[0, 2]] == arr[[0, 2]])