import pytest
import numpy as np

from src.lips.invalidateintersections import invalidateintersections

def test_typical_input():
    arr = np.array([1, 2, 3, 4, 5], dtype=float)
    invalid = [2, 4]
    expected = np.array([1, np.nan, 3, np.nan, 5], dtype=float)
    out = invalidateintersections(arr.copy(), invalid)
    np.testing.assert_array_equal(out, expected)

def test_no_invalid():
    arr = np.arange(1, 6, dtype=float)
    out = invalidateintersections(arr.copy(), [])
    np.testing.assert_array_equal(out, arr)

def test_all_invalid():
    arr = np.arange(4, 9, dtype=float)
    invalid = [1, 2, 3, 4, 5]
    out = invalidateintersections(arr.copy(), invalid)
    assert np.all(np.isnan(out))

def test_empty_list():
    out = invalidateintersections(np.array([], dtype=float), [])
    assert out.size == 0