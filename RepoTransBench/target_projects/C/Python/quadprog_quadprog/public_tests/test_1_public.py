import numpy as np
import pytest

# Assume quadprog module is available in the environment
# The sys.path.insert is removed as per standard Python packaging practices.
# The `quadprog` module is expected to be installed as a dependency.
try:
    from quadprog import solve_qp
except ImportError:
    solve_qp = None

pytestmark = pytest.mark.skipif(solve_qp is None, reason="solve_qp not available for import")

def test_qp_simple_public():
    # min 0.5 * x^T P x + q^T x s.t.  Gx <= h
    # Data changed from original tests
    P = np.array([[2.5, 1.0], [1.0, 2.0]])
    q = np.array([-2, -5])
    G = np.array([[-1, 0], [0, -1], [2, 1]])
    h = np.array([0, 0, 4])
    # The original C test signature had (P, q, G, h, meq, factorized_P, ...)
    # For Python's solve_qp, we often get (sol, obj, active, status)
    sol, obj, active, status = solve_qp(P, q, G, h)
    
    # For these values, the minimum is at (1.2, 1.6)
    np.testing.assert_allclose(sol, [1.2, 1.6], rtol=1e-3, atol=1e-5)
    assert status == 0

def test_qp_nontrivial_constraints_public():
    P = np.array([[1, .2], [.2, 1]])
    q = np.array([-1., -2.])
    G = np.array([[-1., 0.], [0., -1.], [2., 1.]])
    h = np.array([0., 0., 3.5])
    sol, obj, active, status = solve_qp(P, q, G, h)
    
    # These constraints limit the solution, so test for sum close to bound
    assert sol[0] >= -1e-8
    assert sol[1] >= -1e-8
    # 2*sol[0]+sol[1] <= 3.5. Check if it's close to the bound or less.
    assert (2*sol[0]+sol[1] - 3.5) <= 1e-6
    assert status == 0