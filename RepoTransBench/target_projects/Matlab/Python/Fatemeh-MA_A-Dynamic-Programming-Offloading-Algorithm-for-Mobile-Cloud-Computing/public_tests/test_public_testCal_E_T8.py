import numpy as np
from src.Cal_E_T8 import Cal_E_T8

def test_public_Cal_E_T8():
    T_rate = 2.5e6
    tasks = np.array([715e3, 960e3, 1580e3, 2220e3, 1490e3])
    N = len(tasks)
    EL, EC, TL, TC, Cci = Cal_E_T8(T_rate, tasks, N)

    assert len(EL) == N, 'EL size mismatch'
    assert len(EC) == N, 'EC size mismatch'
    assert len(TL) == N, 'TL size mismatch'
    assert len(TC) == N, 'TC size mismatch'
    assert len(Cci) == N, 'Cci size mismatch'
    assert np.all(EL >= 0), 'All EL should be non-negative'
    assert np.all(EC >= 0), 'All EC should be non-negative'