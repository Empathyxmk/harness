import pytest
import numpy as np
from hgpvision.ins_solver import InsSolver
from hgpvision.attitude import AttitudeBase

class TestInsSolverSmokePublic:
    def test_constructor_and_basic_methods_public(self):
        try:
            s = InsSolver()
            assert s is not None
            if hasattr(s, 'AttitudeUpdate'):
                ab = AttitudeBase()
                cnb = ab.a2cnb([0.1, -0.2, 0.3])
                gyro = np.array([0.01, -0.02, 0.03])
                dt = 0.02
                s.AttitudeUpdate(cnb, gyro, dt)
        except Exception as e:
            pytest.fail(f"Unexpected error [public]: {e}")