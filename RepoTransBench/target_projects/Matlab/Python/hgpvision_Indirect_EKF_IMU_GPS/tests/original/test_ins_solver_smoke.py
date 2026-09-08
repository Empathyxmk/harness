import pytest
import numpy as np
from hgpvision.ins_solver import InsSolver
from hgpvision.attitude import AttitudeBase

class TestInsSolverSmoke:
    def test_constructor_and_basic_methods(self):
        try:
            s = InsSolver()
            assert s is not None
            if hasattr(s, 'AttitudeUpdate'):
                ab = AttitudeBase()
                cnb = ab.a2cnb([0, 0, 0])
                gyro = np.array([0, 0, 0])
                dt = 0.01
                s.AttitudeUpdate(cnb, gyro, dt)
        except Exception as e:
            pytest.fail(f"Unexpected error: {e}")