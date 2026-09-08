import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import lafan1.utils as utils
import numpy as np

def test_quaternion_inverse_identity_public():
    # Use nontrivial quaternion
    q = np.array([0.6,0.3,0.5,0.5])
    inv = utils.qinv(q)
    ident = utils.qmul(q, inv)
    np.testing.assert_allclose(ident, np.array([1,0,0,0]), rtol=1e-4)

def test_quaternion_mul_identity_left_public():
    q = np.array([2,-2,1,4])
    ident = np.array([1,0,0,0])
    product = utils.qmul(ident, q)
    np.testing.assert_allclose(product, q, rtol=1e-4)

def test_quaternion_mul_identity_right_public():
    q = np.array([-5,7,-1,0])
    ident = np.array([1,0,0,0])
    product = utils.qmul(q, ident)
    np.testing.assert_allclose(product, q, rtol=1e-4)

def test_quaternion_norm_public():
    q = np.array([3,1,4,1])
    norm = np.linalg.norm(q)
    n_q = utils.qnorm(q)
    assert np.allclose(n_q, q/norm)

def test_quaternion_slerp_self_public():
    q = np.array([0.8,0.2,0.1,0.5])
    out = utils.slerp(q, q, 0.8)
    np.testing.assert_allclose(out, q, rtol=1e-5)

def test_euler_to_quat_and_back_public():
    e = np.array([0.35, -0.18, 0.47])
    q = utils.euler_to_quat(e)
    e_back = utils.quat_to_euler(q)
    assert e_back.shape == e.shape

def test_quaternion_broadcast_public():
    qs = np.array([[2,0,0,0],[0.3,0.6,0.5,0.2]])
    norms = np.linalg.norm(qs, axis=1, keepdims=True)
    nqs = utils.qnorm(qs)
    np.testing.assert_allclose(nqs, qs/norms, rtol=1e-5)

def test_quaternion_shape_robustness_public():
    q = 4*np.ones((4,))
    inv = utils.qinv(q)
    assert inv.shape == (4,)
    qs = 2*np.ones((3,4))
    invs = utils.qinv(qs)
    assert invs.shape == (3,4)