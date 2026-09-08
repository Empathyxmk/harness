import numpy as np
import pytest

from src.eemd_project.eemd import eemd

def test_simple_sinusoid():
    x = np.sin(2 * np.pi * np.arange(0, 1.01, 0.01))
    Nstd = 0.2
    NE = 10
    imfs = eemd(x, Nstd, NE)
    assert isinstance(imfs, np.ndarray)
    assert imfs.shape[1] == len(x)

def test_random_signal():
    x = np.random.randn(100)
    Nstd = 0.1
    NE = 5
    imfs = eemd(x, Nstd, NE)
    assert isinstance(imfs, np.ndarray)
    assert imfs.shape[1] == len(x)

def test_short_signal():
    x = np.sin(2 * np.pi * np.arange(0, 1.01, 0.25))
    Nstd = 0.3
    NE = 8
    imfs = eemd(x, Nstd, NE)
    assert isinstance(imfs, np.ndarray)
    assert imfs.shape[1] == len(x)