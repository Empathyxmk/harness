import numpy as np
import pytest

from src.enigmahuang_poisson_fdm_multigrid.gs_iter import GS_Iter

def assert_vectors_almost_equal(x, y, tol=1e-6):
    np.testing.assert_allclose(x, y, atol=tol)

def test_gs_iter_basic():
    A = np.array([[2, 1], [1, 2]], dtype=float)
    b = np.array([3, 3], dtype=float)
    x, iter_cnt = GS_Iter(A, b)
    assert_vectors_almost_equal(x, [1, 1], tol=1e-6)
    assert iter_cnt > 0

def test_gs_iter_no_x0():
    A = np.array([[4, -1, 0],
                  [-1, 4, -1],
                  [0, -1, 4]], dtype=float)
    b = np.array([10, 0, 10], dtype=float)
    x, iter_cnt = GS_Iter(A, b)
    assert_vectors_almost_equal(x, [3, 2, 3], tol=1e-6)
    assert iter_cnt > 0

def test_gs_iter_with_x0():
    A = np.array([[2, 1], [1, 2]], dtype=float)
    b = np.array([3, 3], dtype=float)
    x0 = np.array([0, 0], dtype=float)
    x, iter_cnt = GS_Iter(A, b, tol=1e-6, max_iter=100, x0=x0)
    assert_vectors_almost_equal(x, [1, 1], tol=1e-6)
    assert iter_cnt > 0

def test_gs_iter_max_iter():
    A = np.array([[2, 1], [1, 2]], dtype=float)
    b = np.array([3, 3], dtype=float)
    x, iter_cnt = GS_Iter(A, b, tol=1e-10, max_iter=5)
    assert iter_cnt <= 5

def test_gs_iter_non_square_a():
    A = np.array([[1, 2, 3],
                  [4, 5, 6]], dtype=float)
    b = np.array([1, 1], dtype=float)
    x, iter_cnt = GS_Iter(A, b)
    assert x == -1
    assert iter_cnt == 0

def test_gs_iter_large_system():
    n = 50
    A = np.diag(np.ones(n)*2) + np.diag(np.ones(n-1)*-1, 1) + np.diag(np.ones(n-1)*-1, -1)
    b = np.ones(n)
    x, iter_cnt = GS_Iter(A, b)
    assert len(x) == n
    assert iter_cnt > 0