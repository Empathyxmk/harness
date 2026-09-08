import numpy as np
from hgpvision.attitude import AttitudeBase

class TestAttitudeBasePublic:
    def test_a2cnb_basic_public(self):
        ab = AttitudeBase()
        angles = [0.1, 0.2, 0.3]
        cnb = ab.a2cnb(angles)
        assert cnb.shape == (3, 3)

    def test_quat2cnb_basic_public(self):
        ab = AttitudeBase()
        # Rotation about x by pi/4
        q = [np.cos(np.pi/8), np.sin(np.pi/8), 0, 0]
        cnb = ab.quat2cnb(q)
        assert cnb.shape == (3, 3)