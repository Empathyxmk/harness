import numpy as np
from src.logsumexp import logsumexp

def test_all_neginf_row_different():
    x = np.array([-np.inf, -np.inf, -np.inf, -np.inf])
    res = logsumexp(x)
    assert res == -np.inf

def test_multidim_inf_columns_different():
    x = np.array([[-np.inf, -1], [-np.inf, -1]])
    res = logsumexp(x, axis=1)
    expected = np.array([-1, -1])
    assert np.allclose(res, expected, atol=1e-10)

def test_zero_rows_different():
    x = np.ones((0,2))
    res = logsumexp(x, axis=0)
    assert (res.shape == (2,) and res.size == 2) or res.size == 0

def test_nan_inputs_different():
    x = np.array([np.nan, 3])
    res = logsumexp(x)
    assert np.isnan(res)