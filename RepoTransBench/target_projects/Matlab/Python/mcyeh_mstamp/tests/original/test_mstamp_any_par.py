import numpy as np
import pytest
from src.mcyeh_mstamp.mstamp_stamp import mstamp_any_par

def load_toy():
    try:
        toy = np.load('src/mcyeh_mstamp/toy_data.npy', allow_pickle=True).item()
        data = toy['data']
        sub_len = int(toy['sub_len'])
        return data, sub_len
    except Exception:
        np.random.seed(10)
        return np.random.randn(70,3), 17

def test_mstamp_any_par_basic():
    data, sub_len = load_toy()
    pct = 0.7
    n_work = 2
    pro_mul, pro_idx = mstamp_any_par(data, sub_len, pct, n_work)
    assert pro_mul.size >= 1

def test_mstamp_any_par_error_pct():
    data, sub_len = load_toy()
    n_work = 2
    with pytest.raises(Exception):
        mstamp_any_par(data, sub_len, -0.3, n_work)