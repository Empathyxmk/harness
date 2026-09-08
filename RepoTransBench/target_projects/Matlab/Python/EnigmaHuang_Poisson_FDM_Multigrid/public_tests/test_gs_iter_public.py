import numpy as np
import pytest

from src.enigmahuang_poisson_fdm_multigrid.gs_iter import GS_Iter

def assert_vectors_almost_equal(x, y, tol=1e-6):
    np.testing.assert_allclose(x, y, atol=tol)

def test_gs_iter_basic_public():
    A = np.array([[4, 2], [2, 4]], dtype=float)
    b = np.array([12, 12], dtype=float)
    x, iter_cnt = GS_Iter(A, b)
    assert_vectors_almost_equal(x, [2, 2], tol=1e-6)
    assert iter_cnt > 0

def test_gs_iter_no_x0_public():
    A = np.array([
        [5, -2, 0],
        [-2, 5, -2],
        [0, -2, 5]
    ], dtype=float)
    b = np.array([11, 6, 11], dtype=float)
    x, iter_cnt = GS_Iter(A, b)
    assert_vectors_almost_equal(x, [3,2,3], tol=1e-6)
    assert iter_cnt > 0

def test_gs_iter_with_x0_public():
    A = np.array([[3,2],[2,3]], dtype=float)
    b = np.array([10,10], dtype=float)
    x0 = np.array([0,0], dtype=float)
    x, iter_cnt = GS_Iter(A, b, tol=1e-6, max_iter=100, x0=x0)
    assert_vectors_almost_equal(x, [2,2], tol=1e-6)
    assert iter_cnt > 0

def test_gs_iter_max_iter_public():
    A = np.array([[4,1],[1,4]], dtype=float)
    b = np.array([10,10], dtype=float)
    x, iter_cnt = GS_Iter(A, b, tol=1e-10, max_iter=3)
    assert iter_cnt <= 3

def test_gs_iter_non_square_a_public():
    A = np.array([[1,3,2],[5,8,6]], dtype=float)
    b = np.array([2,3], dtype=float)
    x, iter_cnt = GS_Iter(A, b)
    assert x == -1
    assert iter_cnt == 0

def test_gs_iter_large_system_public():
    n = 40
    A = np.diag(np.ones(n)*3) + np.diag(np.ones(n-1)*-2, 1) + np.diag(np.ones(n-1)*-2, -1)
    b = np.ones(n)*2
    x, iter_cnt = GS_Iter(A, b)
    assert len(x) == n
    assert iter_cnt > 0