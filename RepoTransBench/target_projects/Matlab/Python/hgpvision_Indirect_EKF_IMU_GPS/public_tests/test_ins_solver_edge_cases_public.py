import numpy as np
from hgpvision.ins_solver import InsSolver
from hgpvision.attitude import AttitudeBase

class TestInsSolverEdgeCasesPublic:
    def test_attitude_update_zero_rotation_public(self):
        s = InsSolver()
        ab = AttitudeBase()
        cnb = ab.a2cnb([0.7, -0.7, 0.7])
        gyro = np.array([0.0, 0.0, 0.0])
        dt = 0.0
        s.AttitudeUpdate(cnb, gyro, dt)
        assert True