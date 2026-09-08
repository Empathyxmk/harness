import numpy as np
import pytest

from src.rating_check_recola import rating_check_recola

def test_all_below_range():
    # All values below 1, expect all changed to 1
    input_ = np.array([-1.5, 0, 0.8, -5])
    expected = np.array([1, 1, 1, 1])
    result = rating_check_recola(input_)
    assert np.allclose(result, expected, atol=1e-12)

def test_all_above_range():
    # All values above 5, expect all changed to 5
    input_ = np.array([5.5, 10, 6, 8.2])
    expected = np.array([5, 5, 5, 5])
    result = rating_check_recola(input_)
    assert np.allclose(result, expected, atol=1e-12)

def test_in_range_values():
    # All values in range [1, 5], expect unchanged
    input_ = np.array([1, 2.3, 2.7, 5, 3.9])
    result = rating_check_recola(input_)
    # Shape and values should be unchanged
    assert np.allclose(result, input_, atol=1e-12)

def test_mixed_values():
    # Values: below, in range, and above
    input_ = np.array([-2, 1, 1.5, 4, 6])
    expected = np.array([1, 1, 1.5, 4, 5])
    result = rating_check_recola(input_)
    assert np.allclose(result, expected, atol=1e-12)

def test_nan_and_out_of_bounds():
    # Input containing NaNs, below, in-range, and above
    input_ = np.array([np.nan, 2.5, -7, 12, np.nan, 4.9])
    expected = np.array([np.nan, 2.5, 1, 5, np.nan, 4.9])
    result = rating_check_recola(input_)
    comp = (np.isnan(input_) & np.isnan(result)) | (np.abs(result - expected) < 1e-12)
    assert np.all(comp)

def test_empty_input():
    # Empty input, expect empty output
    input_ = np.array([])
    result = rating_check_recola(input_)
    assert result.size == 0

def test_column_vector():
    # Test column vector shape preserved
    input_ = np.array([[2.5], [-3], [5.2]])
    expected = np.array([[2.5], [1], [5]])
    result = rating_check_recola(input_)
    assert np.allclose(result, expected, atol=1e-12)
    assert result.shape == input_.shape

def test_matrix_input():
    # Test on matrix input
    input_ = np.array([[0, 2, 10], [1, 5, 6]])
    expected = np.array([[1, 2, 5], [1, 5, 5]])
    result = rating_check_recola(input_)
    assert np.allclose(result, expected, atol=1e-12)
    assert result.shape == input_.shape

def test_logical_type_error():
    # Should error for non-numeric arrays (e.g., boolean array)
    input_ = np.array([True, False, False, True], dtype=bool)
    with pytest.raises(TypeError):
        rating_check_recola(input_)