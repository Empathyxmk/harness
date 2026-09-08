import numpy as np
from src.mcyeh_mstamp.mstamp_stamp import mstamp_any_par

def test_public_mstamp_any_par_basic():
    from scipy.signal import square
    n = 62
    t = np.arange(1, n+1)
    data = np.column_stack([square(2*np.pi*t/18), np.random.randn(n)*0.2+0.5])
    sub_len = 13
    pro_mul, pro_idx = mstamp_any_par(data, sub_len, 2)
    assert pro_mul.shape == (data.shape[0]-sub_len+1, 2)
    assert pro_idx.shape == (data.shape[0]-sub_len+1, 2)