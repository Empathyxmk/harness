import pytest
import numpy as np
from hgpvision.attitude import AttitudeBase

class TestAttitudeBase:
    def test_a2cnb_nominal(self):
        ab = AttitudeBase()
        atti = [0.1, -0.2, 0.3]  # pitch, roll, yaw
        cnb = ab.a2cnb(atti)
        assert cnb.shape == (3, 3)
        # Should be orthogonal: cnb * cnb' = eye(3) (approximately)
        assert np.linalg.norm(cnb @ cnb.T - np.eye(3)) < 1e-10

    def test_cnb2atti_inversion(self):
        ab = AttitudeBase()
        atti = np.array([0.2, 0.1, -0.4])
        cnb = ab.a2cnb(atti)
        atti2 = ab.cnb2atti(cnb)
        # Since not all conventions are exactly invertible, allow small error
        assert np.linalg.norm(atti - atti2) < 1e-1

    def test_quat2cnb_identity(self):
        ab = AttitudeBase()
        quat = [1, 0, 0, 0]  # Identity quaternion
        cnb = ab.quat2cnb(quat)
        assert np.allclose(cnb, np.eye(3), atol=1e-12)

    def test_quat2cnb_general(self):
        ab = AttitudeBase()
        # 90 deg rotation around y axis
        theta = np.pi / 2
        quat = [np.cos(theta/2), 0, np.sin(theta/2), 0]
        cnb = ab.quat2cnb(quat)
        # Should rotate x onto z
        assert np.isclose(cnb[0, 2], -1, atol=1e-10)

    def test_quat2cnb_error(self):
        ab = AttitudeBase()
        with pytest.raises(IndexError):
            ab.quat2cnb([1, 2, 3])