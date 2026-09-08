import numpy as np
import pytest
from src.mcyeh_mstamp.mstamp_stamp import mstamp_par

def load_toy():
    try:
        toy = np.load('src/mcyeh_mstamp/toy_data.npy', allow_pickle=True).item()
        data = toy['data']
        sub_len = int(toy['sub_len'])
        return data, sub_len
    except Exception:
        np.random.seed(10)
        return np.random.randn(64,3), 14

def test_mstamp_par_basic():
    data, sub_len = load_toy()
    n_work = 2
    pro_mul, pro_idx = mstamp_par(data, sub_len, n_work)
    assert pro_mul.shape == pro_idx.shape

def test_mstamp_par_errors():
    data, sub_len = load_toy()
    sz = data.shape[0]
    n_work = 2
    with pytest.raises(Exception):
        mstamp_par(data, sz, n_work)
    with pytest.raises(Exception):
        mstamp_par(data, 2, n_work)