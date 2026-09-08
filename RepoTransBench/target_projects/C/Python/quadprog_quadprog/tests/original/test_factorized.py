import numpy as np
import pytest

# Assume quadprog module is available in the environment
# The sys.path.insert is removed as per standard Python packaging practices.
# The `quadprog` module is expected to be installed as a dependency.
from quadprog import solve_qp_factorized

def test_factorized_qp():
    P = np.array([[2., 1.], [1., 2.]])
    q = np.array([-2., -6.])
    G = np.array([[1., 1.], [-1., 2.], [2., 1.]])
    h = np.array([2., 2., 3.])

    sol = solve_qp_factorized(P, q, G, h)
    assert sol.shape == (2,)
    # Checking KKT conditions approximately (same as test_1.py)
    assert np.allclose(P @ sol + q + G.T.dot(np.maximum(0, G @ sol - h)), 0, atol=1e-4)

def test_unconstrained_factorized():
    P = np.array([[4., 2.], [2., 2.]])
    q = np.array([-8., -6.])
    G = np.empty((0, 2))
    h = np.empty((0,))

    sol = solve_qp_factorized(P, q, G, h)
    expected_sol = np.linalg.solve(P, -q)
    np.testing.assert_allclose(sol, expected_sol)