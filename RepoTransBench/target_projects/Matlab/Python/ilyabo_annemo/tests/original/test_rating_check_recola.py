import numpy as np
import pytest

from src.rating_check_recola import rating_check_recola

def test_empty_input():
    # Test with empty input array
    actual = rating_check_recola([])
    expected = []
    assert actual == expected, "Empty input should return empty output."

def test_invalid_input_range_below_min():
    # Test with input below the valid range (1)
    actual = rating_check_recola([0, 1, 2])
    expected = [1, 1, 2]
    assert np.allclose(actual, expected, atol=1e-12), "Values below 1 should be clamped to 1."

def test_invalid_input_range_above_max():
    # Test with input above the valid range (5)
    actual = rating_check_recola([4, 5, 6])
    expected = [4, 5, 5]
    assert np.allclose(actual, expected, atol=1e-12), "Values above 5 should be clamped to 5."

def test_valid_input_range():
    # Test with all valid inputs (1 to 5)
    actual = rating_check_recola([1, 2, 3, 4, 5])
    expected = [1, 2, 3, 4, 5]
    assert np.allclose(actual, expected, atol=1e-12), "Valid inputs should remain unchanged."

def test_mixed_input():
    # Test with a mix of valid, too low, and too high inputs and NaN
    arr = np.array([0.5, 1, 3.5, 5, 5.5, np.nan])
    actual = rating_check_recola(arr)
    expected = np.array([1, 1, 3.5, 5, 5, np.nan])
    # NaN compare: match where both are NaN, else absolute diff < 1e-12
    matches = (np.isnan(actual) & np.isnan(expected)) | (np.abs(actual - expected) < 1e-12)
    assert np.all(matches), "Mixed inputs should be clamped correctly, NaN preserved."

def test_single_valid_input():
    actual = rating_check_recola(3)
    expected = 3
    assert np.allclose(actual, expected, atol=1e-12), "Single valid input should be correct."

def test_single_invalid_low_input():
    actual = rating_check_recola(0)
    expected = 1
    assert np.allclose(actual, expected, atol=1e-12), "Single invalid low input should be clamped."

def test_single_invalid_high_input():
    actual = rating_check_recola(10)
    expected = 5
    assert np.allclose(actual, expected, atol=1e-12), "Single invalid high input should be clamped."

def test_large_array_input():
    # Test with a larger array
    input_array = np.arange(0.1, 6.1, 0.5)
    actual = rating_check_recola(input_array)
    expected_array = np.copy(input_array)
    expected_array[expected_array < 1] = 1
    expected_array[expected_array > 5] = 5
    assert np.allclose(actual, expected_array, atol=1e-12), "Large array inputs should be clamped correctly."