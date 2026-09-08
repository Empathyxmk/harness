import pytest
import numpy as np
from src.sp import randn_complex

def test_shape1():
    X = randn_complex(10, 1)
    assert X.shape == (10, 1)

def test_shape2():
    X = randn_complex(5, 3)
    assert X.shape == (5, 3)

def test_mean_std():
    X = randn_complex(5000, 1)
    meanX = np.mean(X.real)
    stdX = np.std(X.real)
    assert abs(meanX) < 0.1 and abs(stdX-1) < 0.1