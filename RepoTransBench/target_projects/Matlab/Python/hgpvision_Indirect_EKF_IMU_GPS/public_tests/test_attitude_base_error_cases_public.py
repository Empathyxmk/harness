import pytest
import numpy as np
from hgpvision.attitude import AttitudeBase

class TestAttitudeBaseErrorCasesPublic:
    def test_a2cnb_invalid_input_public(self):
        ab = AttitudeBase()
        with pytest.raises(IndexError):
            ab.a2cnb([1, 2, 3, 4])

    def test_quat2cnb_unit(self):
        ab = AttitudeBase()
        # Use an all-ones quaternion (not normalized), should still return a matrix
        cnb = ab.quat2cnb([1, 1, 1, 1])
        assert isinstance(cnb, np.ndarray)
        assert cnb.shape == (3, 3)