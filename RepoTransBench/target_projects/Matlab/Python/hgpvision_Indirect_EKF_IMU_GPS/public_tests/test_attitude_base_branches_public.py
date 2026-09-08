import numpy as np
from hgpvision.attitude import AttitudeBase

class TestAttitudeBaseBranchesPublic:
    def test_a2cnb_alt_public(self):
        ab = AttitudeBase()
        # Use negative Euler angles; exercise additional branches
        angles = [-0.4, 0.5, -0.6]
        cnb = ab.a2cnb(angles)
        assert isinstance(cnb, np.ndarray)

    def test_quat2cnb_90deg_yaw_public(self):
        ab = AttitudeBase()
        # Quaternion for 90deg about z axis
        theta = np.pi/2
        q = [np.cos(theta/2), 0, 0, np.sin(theta/2)]
        cnb = ab.quat2cnb(q)
        assert isinstance(cnb, np.ndarray)