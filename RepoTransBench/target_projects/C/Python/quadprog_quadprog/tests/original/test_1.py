import numpy as np
import pytest

# Assume quadprog module is available in the environment
# The sys.path.insert is removed as per standard Python packaging practices.
# The `quadprog` module is expected to be installed as a dependency.
from quadprog import solve_qp

def test_simple_qp():
    # Minimize (1/2)x^T P x + q^T x subject to Gx <= h
    P = np.array([[1., 0.], [0., 1.]])
    q = np.array([3., 4.])
    G = np.array([[1., 1.], [-1., 2.], [2., 1.]])
    h = np.array([1., 2., 3.])

    sol = solve_qp(P, q, G, h)
    assert sol.shape == (2,)
    # Checking KKT conditions approximately
    # Px + q + G.T * lambda = 0
    # lambda >= 0
    # lambda_i * (G_i x - h_i) = 0
    # Gx - h <= 0
    # The original test checked P @ sol + q + G.T.dot(np.maximum(0, G @ sol - h)) approx 0.
    # This term `np.maximum(0, G @ sol - h)` implicitly assumes the dual variables (lambda)
    # are proportional to the constraint violations. While it's an heuristic,
    # it's maintained to match the original test's logic.
    assert np.allclose(P @ sol + q + G.T.dot(np.maximum(0, G @ sol - h)), 0, atol=1e-4)

def test_unconstrained_qp():
    P = np.eye(2)
    q = np.array([-2., -5.])
    G = np.empty((0, 2))
    h = np.empty((0,))

    sol = solve_qp(P, q, G, h)
    expected_sol = np.array([2., 5.])
    np.testing.assert_allclose(sol, expected_sol)

def test_redundant_constraints():
    P = np.eye(2)
    q = np.array([1., 2.])
    G = np.array([[1., 0.], [-1., 0.], [0., 1.]])
    h = np.array([100., 100., 100.])

    sol = solve_qp(P, q, G, h)
    expected_sol = np.array([-1., -2.])
    np.testing.assert_allclose(sol, expected_sol)