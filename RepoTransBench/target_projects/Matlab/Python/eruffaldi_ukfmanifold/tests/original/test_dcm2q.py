import numpy as np
import pytest

from ukfmanifold.quaternions import dcm2q, q2dcm, qnorm

def test_single_matrix_to_quaternion_and_back():
    # Test round-trip from DCM to quaternion and back
    q0 = np.array([0.2, 0.4, 0.6, 0.7])
    q0 = qnorm(q0)
    dcm = q2dcm(q0)
    q1 = dcm2q(dcm)
    # Quaternions are sign-ambiguous; check both possible signs
    assert np.allclose(np.abs(q1), np.abs(q0), atol=1e-8)

def test_batch_dcm_to_quat_and_inverse():
    # Generate random quaternions, convert to DCM, then back
    Q = np.random.randn(10,4)
    Q = np.array([qnorm(q) for q in Q])
    for q in Q:
        dcm = q2dcm(q)
        q_back = dcm2q(dcm)
        # Check rotation equivalence
        assert np.allclose(np.abs(q_back), np.abs(q), atol=1e-7)