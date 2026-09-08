import pytest
import numpy as np
from src.eeg_kaggle.zscore2 import zscore2

def test_basic_zscore():
    x = np.array([1, 2, 3, 4, 5])
    expected_z = (x - np.mean(x)) / np.std(x, ddof=0)
    z = zscore2(x)
    np.testing.assert_allclose(z, expected_z, atol=1e-9)

def test_matrix_zscore():
    x = np.array([[1, 2], [3, 4], [5, 6]])
    expected_z = (x - x.mean(axis=0)) / x.std(axis=0, ddof=0)
    z = zscore2(x)
    np.testing.assert_allclose(z, expected_z, atol=1e-9)

def test_constant_vector():
    x = np.array([5, 5, 5, 5])
    z = zscore2(x)
    assert np.all(np.isnan(z)), "Z-score of constant vector should result in NaNs"

def test_empty_input():
    x = np.array([])
    z = zscore2(x)
    assert z.size == 0

def test_nan_input():
    x = np.array([1, np.nan, 3, 4])
    z = zscore2(x)
    assert np.isnan(z[1])
    assert not np.any(np.isnan(z[[0,2,3]]))

def test_large_numbers():
    x = np.array([1e6, 2e6, 3e6, 4e6, 5e6])
    expected_z = (x - x.mean()) / x.std(ddof=0)
    z = zscore2(x)
    np.testing.assert_allclose(z, expected_z, atol=1e-9)

def test_zero_input():
    x = np.array([0, 0, 0])
    z = zscore2(x)
    assert np.all(np.isnan(z)), "Z-score of all zeros should result in NaNs"