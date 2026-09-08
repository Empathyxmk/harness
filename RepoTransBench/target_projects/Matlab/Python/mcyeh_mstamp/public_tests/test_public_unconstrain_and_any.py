import numpy as np
from src.mcyeh_mstamp.mstamp_stamp import unconstrain_search, mstamp_any

def test_public_unconstrain_and_any():
    t = np.linspace(0, 5*np.pi, 55)
    from scipy.signal import sawtooth
    y1 = sawtooth(t)
    y2 = np.cos(t) + np.random.randn(len(t))*0.06
    data = np.column_stack([y1, y2])
    sub_len = 8
    p1, idx1 = unconstrain_search(data, sub_len)
    p2, idx2 = mstamp_any(data, sub_len)
    sz = data.shape[0]-sub_len+1
    assert p1.shape == (sz, 2)
    assert idx1.shape == (sz, 2)
    assert p2.shape == (sz, 2)
    assert idx2.shape == (sz, 2)