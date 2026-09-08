import numpy as np
import pytest

from src.eemd_project.extrema import extrema

def test_increasing():
    x = np.arange(1, 6)
    max_inds, min_inds = extrema(x)
    assert len(max_inds) == 0
    assert len(min_inds) == 0

def test_decreasing():
    x = np.arange(5, 0, -1)
    max_inds, min_inds = extrema(x)
    assert len(max_inds) == 0
    assert len(min_inds) == 0

def test_middle_peak():
    x = np.array([1, 2, 3, 2, 1])
    max_inds, min_inds = extrema(x)
    assert np.array_equal(max_inds, np.array([2]))
    assert len(min_inds) == 0

def test_middle_valley():
    x = np.array([3, 2, 1, 2, 3])
    max_inds, min_inds = extrema(x)
    assert len(max_inds) == 0
    assert np.array_equal(min_inds, np.array([2]))

def test_multiple_peaks_and_valleys():
    x = np.array([1, 3, 1, 3, 1, 3, 1])
    max_inds, min_inds = extrema(x)
    assert np.array_equal(max_inds, np.array([1, 3, 5]))
    assert np.array_equal(min_inds, np.array([2, 4]))