import pytest
from src.sp import complex2vector
import numpy as np

def test_length():
    z = np.array([1+2j, 3+4j])
    v = complex2vector(z)
    assert len(v) == 4

def test_known_value():
    z = np.array([1+1j])
    v = complex2vector(z)
    assert v[0] == 1 and v[1] == 1