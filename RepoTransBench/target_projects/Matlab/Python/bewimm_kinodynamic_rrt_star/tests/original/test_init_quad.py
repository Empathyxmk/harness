import numpy as np
import importlib
import pytest

# For this test to function, the user must implement the "init_quad" function in src/bewimm_kinodynamic_rrt_star/init_quad.py

def test_init_quad_variables():
    # Assumes init_quad returns the variables as dictionary or a tuple
    from bewimm_kinodynamic_rrt_star.init_quad import init_quad

    # The init_quad function should return all variables used in the quadrotor equations/model:
    # prop_diameter, rotor_dist, w, h, d, m, rotor_to_com, g, state_dims, input_dims, A, B, c, R, I_w, I_d

    out = init_quad()
    if isinstance(out, dict):
        _ = lambda k: out[k]
    else:
        # Unpack as tuple
        (prop_diameter, rotor_dist, w, h, d, m, rotor_to_com, g, state_dims, input_dims, A, B, c, R, I_w, I_d) = out
        _ = lambda k: locals()[k]

    # Types and sizes
    A = _('A')
    B = _('B')
    c = _('c')
    R = _('R')
    g = _('g')
    m = _('m')
    state_dims = _('state_dims')
    input_dims = _('input_dims')
    w = _('w')
    h = _('h')
    d = _('d')
    rotor_to_com = _('rotor_to_com')
    I_w = _('I_w')
    I_d = _('I_d')
    prop_diameter = _('prop_diameter')
    rotor_dist = _('rotor_dist')

    assert A.shape == (state_dims, state_dims), f"A shape: {A.shape}"
    assert B.shape == (state_dims, input_dims), f"B shape: {B.shape}"
    assert c.shape == (state_dims, 1)
    assert R.shape == (input_dims, input_dims)

    assert g == pytest.approx(9.81)
    assert m == pytest.approx(0.26)
    assert state_dims == 10
    assert input_dims == 3

    # Check blocks in A
    assert np.allclose(A[0:3,3:6], np.eye(3)), "A[0:3,3:6] not identity"
    block = np.zeros((3,2))
    block[0,1] = g
    block[1,0] = -g
    # (In MATLAB: A[4:6,7:8] = [0,g;-g,0;0,0]; 0-based in Python is A[3:6,6:8])
    assert np.allclose(A[3:6,6:8], block), f"A[3:6,6:8]={A[3:6,6:8]}"
    assert np.allclose(A[6:8,8:10], np.eye(2))

    # B check (force input)
    assert np.allclose(B[3:6,0].reshape(3,1), np.array([[0],[0],[1/m]])), "B[3:6,0]"

    # Inertia
    I_w_expected = 1/12*m*(h**2 + d**2)
    I_d_expected = 1/12*m*(h**2 + w**2)
    assert I_w == pytest.approx(I_w_expected)
    assert I_d == pytest.approx(I_d_expected)

    # Check torque block (B[8:10,1:3])
    B_torque = np.diag([rotor_to_com/I_w_expected, rotor_to_com/I_d_expected])
    assert np.allclose(B[8:10,1:3], B_torque)

    assert np.allclose(R, np.diag([1/4,1/2,1/2]))