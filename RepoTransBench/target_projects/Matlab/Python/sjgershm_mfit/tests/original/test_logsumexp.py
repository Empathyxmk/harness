import pytest
import numpy as np
from src.logsumexp import logsumexp

def test_simple_case():
    x = np.log([1,2,3])
    actual = logsumexp(x)
    expected = np.log(np.sum(np.exp(x)))
    assert np.allclose(actual, expected, atol=1e-10)

def test_dim2_sum():
    np.random.seed(2)
    x = np.random.rand(3,4)
    res1 = logsumexp(x, axis=0)
    expected1 = np.log(np.sum(np.exp(x), axis=0))
    assert np.allclose(res1, expected1, atol=1e-10)
    res2 = logsumexp(x, axis=1)
    expected2 = np.log(np.sum(np.exp(x), axis=1))
    assert np.allclose(res2, expected2, atol=1e-10)

def test_vector_default_dim():
    x = np.array([1,2,3])
    res = logsumexp(x)
    assert np.allclose(res, np.log(np.sum(np.exp(x))), atol=1e-10)

def test_inf_inputs():
    x = np.array([-np.inf, 0, 1])
    res = logsumexp(x)
    expected = np.log(np.sum(np.exp(x)))
    assert np.allclose(res, expected, atol=1e-10)