import numpy as np
import pytest
import lafan1.utils as utils

def test_quat_inv_unit_identity():
    x = np.array([1., 0., 0., 0.])
    inv = utils.quat_inv_unit(x)
    q_mult = utils.quat_mult_unit(x, inv)
    # Identity quaternion
    assert np.allclose(q_mult, [1., 0., 0., 0.])

def test_quat_mult_unit_basic():
    x = np.array([1., 0., 0., 0.])
    y = np.array([1., 0., 0., 0.])
    z = utils.quat_mult_unit(x, y)
    assert np.allclose(z, [1., 0., 0., 0.])

def test_quat_mult_unit_nontrivial():
    x = np.array([0., 1., 0., 0.])
    y = np.array([0., 0., 1., 0.])
    z = utils.quat_mult_unit(x, y)
    # Should be [0,-0,0,1], but sign may differ (unit quaternions cover double cover)
    assert np.allclose(sorted(np.abs(z)), sorted([0., 0., 0., 1.]))

def test_quat_mult_unit_broadcast():
    q1 = np.array([[1.,0.,0.,0.],[0.,1.,0.,0.]])
    q2 = np.array([[1.,0.,0.,0.],[0.,1.,0.,0.]])
    z = utils.quat_mult_unit(q1, q2)
    assert z.shape == (2,4)

def test_quat_mult_unit_badshape():
    x = np.array([1.,0.,0.])
    y = np.array([1.,0.,0.,0.])
    with pytest.raises(ValueError):
        utils.quat_mult_unit(x, y)

def test_quat_fk_wrong_shape():
    lrot = np.zeros((2,4))
    lpos = np.zeros((3,3))
    parents = [-1, 0]
    with pytest.raises(ValueError):
        utils.quat_fk(lrot, lpos, parents)

def test_quat_fk_bad_num_parents():
    lrot = np.zeros((2,4))
    lpos = np.zeros((2,3))
    parents = [-1, 1, 5]
    with pytest.raises(ValueError):
        utils.quat_fk(lrot, lpos, parents)

def test_quat_fk_root_linked():
    lrot = np.zeros((2,4))
    lpos = np.ones((2,3))
    parents = [-1, 0]
    grot, gpos = utils.quat_fk(lrot, lpos, parents)
    assert grot.shape == (2,4) and gpos.shape == (2,3)