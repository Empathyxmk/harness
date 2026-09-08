import pytest
from src.sp import lms
import numpy as np

def test_simple_lms():
    d = np.array([0.2, 0.4, 0.8, 1.0])
    x = np.array([0, 1, 1, 0])
    _, e = lms(x, d, 0.2, 1)
    assert len(e) == 4