import numpy as np
import pytest

from src.eemd_project.extrema import extrema

def test_flat():
    y = np.array([4, 4, 4, 4])
    max_inds, min_inds = extrema(y)
    assert len(max_inds) == 0
    assert len(min_inds) == 0

def test_end_peak():
    y = np.array([2, 3, 4, 5, 6, 5])
    max_inds, min_inds = extrema(y)
    assert np.array_equal(max_inds, np.array([]))
    assert np.array_equal(min_inds, np.array([]))

def test_two_peaks():
    y = np.array([2, 5, 2, 5, 2])
    max_inds, min_inds = extrema(y)
    assert np.array_equal(max_inds, np.array([1, 3]))
    assert len(min_inds) == 0

def test_two_valleys():
    y = np.array([5, 2, 5, 2, 5])
    max_inds, min_inds = extrema(y)
    assert len(max_inds) == 0
    assert np.array_equal(min_inds, np.array([1, 3]))

def test_peak_and_valley():
    y = np.array([2, 7, 2, 8, 2, 3, 2])
    max_inds, min_inds = extrema(y)
    assert np.array_equal(max_inds, np.array([1, 3]))
    assert np.array_equal(min_inds, np.array([2, 6]))