import pytest
import numpy as np
from hgpvision.attitude import AttitudeBase

class TestAttitudeBaseErrorCases:
    def test_a2cnb_invalid_input(self):
        ab = AttitudeBase()
        with pytest.raises(IndexError):
            ab.a2cnb([1, 2])

    def test_quat2cnb_zeros(self):
        ab = AttitudeBase()
        # All zeros quaternion is not valid; should just return identity with no error
        cnb = ab.quat2cnb([0, 0, 0, 0])
        assert np.allclose(cnb, np.eye(3), atol=1e-12)