import numpy as np
from ukfmanifold.quaternions import qnorm

def test_unit_quaternion_remains_unit():
    q = np.array([0.5, -0.2, 0.3, 0.8])
    qn = qnorm(q)
    assert np.isclose(np.linalg.norm(qn), 1.0, rtol=1e-10)

def test_nonunit_quaternion():
    q = np.array([2.0, 0.0, 0.0, 0.0])
    qn = qnorm(q)
    assert np.isclose(np.linalg.norm(qn), 1.0, rtol=1e-10)

def test_matrix_of_quaternions():
    Q = np.random.randn(10,4)
    Qn = qnorm(Q)
    for q in Qn:
        assert np.isclose(np.linalg.norm(q), 1.0, rtol=1e-10)