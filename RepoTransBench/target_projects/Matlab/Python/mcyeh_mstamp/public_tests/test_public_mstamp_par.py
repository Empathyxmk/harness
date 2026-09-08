import numpy as np
from src.mcyeh_mstamp.mstamp_stamp import mstamp_par

def test_mstamp_par_public():
    np.random.seed(1234)
    data = np.zeros((61,2))
    data[:,0] = np.sin(np.arange(0, 30.5, 0.5)) + 0.5*np.random.randn(61)
    data[:,1] = np.cos(np.arange(0, 30.5, 0.5)) + 0.5*np.random.randn(61)
    sub_len = 15
    n_work = 2
    pro_mul, pro_idx = mstamp_par(data, sub_len, n_work)
    assert pro_mul.shape == (data.shape[0]-sub_len+1, data.shape[1])
    assert pro_idx.shape == (data.shape[0]-sub_len+1, data.shape[1])
    assert np.min(pro_mul) >= 0
    assert np.max(pro_idx) <= data.shape[0]-sub_len+1