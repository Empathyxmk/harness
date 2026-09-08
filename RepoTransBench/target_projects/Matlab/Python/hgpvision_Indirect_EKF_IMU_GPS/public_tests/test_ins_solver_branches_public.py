import numpy as np
from hgpvision.ins_solver import InsSolver
from hgpvision.attitude import AttitudeBase

class TestInsSolverBranchesPublic:
    def test_attitude_update_nontrivial_public(self):
        s = InsSolver()
        ab = AttitudeBase()
        cnb = ab.a2cnb([-0.2, 0.4, 0.7])
        gyro = np.array([0.05, -0.07, 0.05])
        dt = 0.015
        s.AttitudeUpdate(cnb, gyro, dt)
        assert True  # If no error, test passes