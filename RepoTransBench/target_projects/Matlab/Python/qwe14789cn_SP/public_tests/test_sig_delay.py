import pytest
from src.sp import sig_delay
import numpy as np

def test_int_delay():
    x = np.array([1, 2, 3, 4])
    y = sig_delay(x, 2)
    assert len(y) == 4
    assert y[0] == 0

def test_frac_delay():
    x = np.array([1, 1, 0, 0])
    y = sig_delay(x, 0.5)
    assert len(y) == 4