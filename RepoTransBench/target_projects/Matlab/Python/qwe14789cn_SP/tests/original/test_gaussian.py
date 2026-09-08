import pytest
import numpy as np
from src.sp import gaussian

def test_shape():
    x = np.arange(-5, 5.1, 0.1)
    y = gaussian(x, 1, 0)
    assert len(y) == len(x) and all(yi >= 0 for yi in y)

def test_sigma_variation():
    x = np.linspace(-3, 3, 100)
    y1 = gaussian(x, 1, 0)
    y2 = gaussian(x, 0.5, 0)
    assert max(y2) > max(y1)

def test_offsets():
    x = np.linspace(-3, 3, 100)
    y = gaussian(x, 1, 2)
    idx = np.argmax(y)
    assert abs(x[idx] - 2) < 0.2