import pytest
import numpy as np
from src.logsumexp import logsumexp

def test_all_neginf_row():
    x = np.array([-np.inf, -np.inf, -np.inf])
    res = logsumexp(x)
    assert res == -np.inf

def test_multidim_inf_columns():
    x = np.array([[-np.inf, 0],[-np.inf,0]])
    res = logsumexp(x, axis=1)
    expected = np.array([0,0])
    assert np.allclose(res, expected, atol=1e-10)

def test_zero_rows():
    x = np.ones((0,3))
    res = logsumexp(x, axis=0)
    assert (res.shape == (3,) and res.size == 3) or res.size==0

def test_nan_inputs():
    x = np.array([np.nan, np.nan])
    res = logsumexp(x)
    assert np.isnan(res)