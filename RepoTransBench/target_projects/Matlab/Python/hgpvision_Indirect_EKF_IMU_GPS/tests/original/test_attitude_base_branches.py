import pytest
import numpy as np
from hgpvision.attitude import AttitudeBase

class TestAttitudeBaseBranches:
    def test_cnb2atti_branch_psi_positive(self):
        ab = AttitudeBase()
        atti = [np.pi/6, np.pi/4, np.pi/3]
        cnb = ab.a2cnb(atti)
        cnb[1,0] = -abs(cnb[1,0])  # force psi calculation to positive branch
        att_rec = ab.cnb2atti(cnb)
        assert len(att_rec) == 3

    def test_cnb2atti_branch_psi_negative(self):
        ab = AttitudeBase()
        atti = [np.pi/6, np.pi/4, np.pi/3]
        cnb = ab.a2cnb(atti)
        cnb[1,0] = abs(cnb[1,0])  # triggers psi=-psi branch
        att_rec = ab.cnb2atti(cnb)
        assert len(att_rec) == 3

    def test_a2cnb_zero(self):
        ab = AttitudeBase()
        atti = [0, 0, 0]
        cnb = ab.a2cnb(atti)
        assert np.allclose(cnb, np.eye(3), atol=1e-12)

    def test_quat2cnb_error_branch(self):
        ab = AttitudeBase()
        with pytest.raises(IndexError):
            ab.quat2cnb([1, 2])