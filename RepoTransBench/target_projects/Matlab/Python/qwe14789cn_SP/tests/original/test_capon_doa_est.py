import pytest
import numpy as np
from src.sp import capon_doa_est

def test_identity_input():
    X = np.eye(4)
    DOAs = capon_doa_est(X, 2, np.arange(1, 5), 2)
    assert len(DOAs) > 0

def test_random_input():
    X = np.random.randn(4, 20) + 1j * np.random.randn(4, 20)
    DOAs = capon_doa_est(X, 5, np.linspace(-90, 90, 5), 4)
    assert len(DOAs) > 0