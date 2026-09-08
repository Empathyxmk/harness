import numpy as np
from src.mcyeh_mstamp.mstamp_stamp import mstamp_par

def test_public_demo_simple():
    t = np.arange(0, 20.25, 0.25)
    y1 = np.sin(t) + np.random.randn(len(t))*0.1
    y2 = np.cos(t+1) + np.random.randn(len(t))*0.1
    data = np.column_stack([y1, y2])
    sub_len = 10
    pro_mul, pro_idx = mstamp_par(data, sub_len, 2)
    assert pro_mul.shape == (data.shape[0]-sub_len+1, 2)
    assert pro_idx.shape == (data.shape[0]-sub_len+1, 2)
    assert np.min(pro_mul) >= 0