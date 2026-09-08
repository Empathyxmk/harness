import numpy as np
from src.logsumexp import logsumexp

def test_simple_case_different():
    x = np.log([4,5,6])
    actual = logsumexp(x)
    expected = np.log(np.sum(np.exp(x)))
    assert np.allclose(actual, expected, atol=1e-10)

def test_dim2_sum_different():
    np.random.seed(101)
    x = np.random.rand(4,3)
    res1 = logsumexp(x, axis=0)
    expected1 = np.log(np.sum(np.exp(x), axis=0))
    assert np.allclose(res1, expected1, atol=1e-10)
    res2 = logsumexp(x, axis=1)
    expected2 = np.log(np.sum(np.exp(x), axis=1))
    assert np.allclose(res2, expected2, atol=1e-10)

def test_vector_default_dim_different():
    x = np.array([4,5,6])
    res = logsumexp(x)
    assert np.allclose(res, np.log(np.sum(np.exp(x))), atol=1e-10)

def test_inf_inputs_different():
    x = np.array([-np.inf, 2, 3])
    res = logsumexp(x)
    expected = np.log(np.sum(np.exp(x)))
    assert np.allclose(res, expected, atol=1e-10)