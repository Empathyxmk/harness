import numpy as np
from tests.original.calOptPower_helper import calOptPower

def test_calOptPower_typical():
    PL = [100, 120]
    N0 = 1e-10
    Pmax = 1
    targetSINR = 8
    gamma = 2
    K = len(PL)
    try:
        power, flag = calOptPower(PL, N0, Pmax, targetSINR, gamma, K)
        assert isinstance(power, (list, np.ndarray, float))
        if isinstance(power, np.ndarray):
            assert np.all(power >= 0)
        else:
            assert all(p >= 0 for p in power)
    except Exception:
        power = calOptPower(PL, N0, Pmax, targetSINR, gamma, K)
        assert isinstance(power, (list, np.ndarray, float))
        if isinstance(power, np.ndarray):
            assert np.all(power >= 0)
        else:
            assert all(p >= 0 for p in power)