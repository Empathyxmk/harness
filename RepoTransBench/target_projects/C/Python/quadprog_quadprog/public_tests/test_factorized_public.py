import numpy as np
import pytest

# Assume quadprog module is available in the environment
# The sys.path.insert is removed as per standard Python packaging practices.
# The `quadprog` module is expected to be installed as a dependency.
try:
    from quadprog import solve_qp_factorized
except ImportError:
    solve_qp_factorized = None

pytestmark = pytest.mark.skipif(solve_qp_factorized is None, reason="solve_qp_factorized not available for import")

def test_qp_factorized_diff_data_public():
    # Slightly different matrix data than main test
    P = np.array([[6., 2.], [2., 3.]])
    q = np.array([-4., -1.])
    G = np.array([[-1., 0.], [0., -1.], [1., 2.]])
    h = np.array([0., 0., 4.0])
    sol, obj, active, status = solve_qp_factorized(P, q, G, h)
    # Boundaries are at x>=0,y>=0, x+2y<=4. Minimum should be at (0,2)
    np.testing.assert_allclose(sol, [0., 2.], rtol=1e-3, atol=1e-6)
    assert status == 0

def test_qp_factorized_interesting_constraint_public():
    P = np.array([[2., 0.5], [0.5, 1.]])
    q = np.array([0., 0.])
    G = np.array([[-1., 0.], [0., -1.], [1., 1.], [-1., 2.]])
    h = np.array([0., 0., 2.2, 1.5])
    sol, obj, active, status = solve_qp_factorized(P, q, G, h)
    assert sol[0] >= -1e-8
    assert sol[1] >= -1e-8
    assert sol[0] + sol[1] - 2.2 <= 1e-6
    assert -sol[0] + 2 * sol[1] - 1.5 <= 1e-6
    assert status == 0