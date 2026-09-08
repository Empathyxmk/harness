import numpy as np
from src.mcyeh_mstamp.mstamp_stamp import mstamp_par, mstamp_any_par

def load_toy():
    try:
        toy = np.load('src/mcyeh_mstamp/toy_data.npy', allow_pickle=True).item()
        data = toy['data']
        sub_len = int(toy['sub_len'])
        return data, sub_len
    except Exception:
        np.random.seed(11)
        return np.random.randn(63,3), 13

def test_mstamp_par_batch():
    data, sub_len = load_toy()
    pro_mul, pro_idx = mstamp_par(data, sub_len)
    assert isinstance(pro_mul, np.ndarray)
    assert isinstance(pro_idx, np.ndarray)

def test_mstamp_any_par_batch():
    data, sub_len = load_toy()
    pro_mul, pro_idx = mstamp_any_par(data, sub_len)
    assert isinstance(pro_mul, np.ndarray)
    assert isinstance(pro_idx, np.ndarray)