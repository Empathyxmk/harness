import pytest
from src.sp import lms2
import numpy as np

def test_lms2():
    d = np.array([0.1, 0.2, 0.3, 0.5])
    x = np.array([1, 0, 1, 0])
    _, e = lms2(x, d, 0.3, 1)
    assert len(e) == 4