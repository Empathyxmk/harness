import numpy as np
from src.Cal_E_T7 import Cal_E_T7

def test_public_Cal_E_T7():
    T_rate = 5e6
    tasks = np.array([800e3, 2100e3, 1750e3, 2600e3, 3500e3, 900e3, 1300e3])
    N = tasks.shape[0]
    EL, EC, TL, TC, Cci = Cal_E_T7(T_rate, tasks, N)

    assert len(EL) == N, 'EL size mismatch'
    assert len(EC) == N, 'EC size mismatch'
    assert len(TL) == N, 'TL size mismatch'
    assert len(TC) == N, 'TC size mismatch'
    assert len(Cci) == N, 'Cci size mismatch'
    assert np.all(EL > 0), 'All EL should be positive'
    assert np.all(EC > 0), 'All EC should be positive'
    assert np.all(TL > 0), 'All TL should be positive'
    assert np.all(TC > 0), 'All TC should be positive'