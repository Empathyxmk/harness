import numpy as np
import pytest

from src.eemd_project.eemd import eemd

def test_cosine():
    y = np.cos(2 * np.pi * np.arange(0, 1.01, 0.01))
    Nstd = 0.15
    NE = 7
    imfs = eemd(y, Nstd, NE)
    assert isinstance(imfs, np.ndarray)
    assert imfs.shape[1] == len(y)

def test_ramp():
    y = np.linspace(1, 10, 50)
    Nstd = 0.05
    NE = 6
    imfs = eemd(y, Nstd, NE)
    assert isinstance(imfs, np.ndarray)
    assert imfs.shape[1] == len(y)

def test_noisy_sine():
    n = np.arange(0, 1.01, 0.02)
    y = np.sin(2 * np.pi * n) + 0.2 * np.random.randn(len(n))
    Nstd = 0.25
    NE = 12
    imfs = eemd(y, Nstd, NE)
    assert isinstance(imfs, np.ndarray)
    assert imfs.shape[1] == len(y)