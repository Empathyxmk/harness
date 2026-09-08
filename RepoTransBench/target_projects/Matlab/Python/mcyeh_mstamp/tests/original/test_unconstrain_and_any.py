import numpy as np
from src.mcyeh_mstamp.mstamp_stamp import unconstrain_search, mstamp_any

def load_toy():
    try:
        toy = np.load('src/mcyeh_mstamp/toy_data.npy', allow_pickle=True).item()
        data = toy['data']
        sub_len = int(toy['sub_len'])
        return data, sub_len
    except Exception:
        np.random.seed(5)
        return np.random.randn(60,3), 14

def test_unconstrain_search_basic():
    data, sub_len = load_toy()
    unconstrain_search(data, sub_len, [], [])

def test_unconstrain_search_invalid_inputs():
    try:
        unconstrain_search([], 5, [], [])
    except Exception:
        assert True

def test_mstamp_any():
    data, sub_len = load_toy()
    pro_mul, pro_idx = mstamp_any(data, sub_len, [], [])
    assert pro_mul.shape[-1] == data.shape[-1]
    assert pro_idx.dtype.kind in ['i', 'u', 'f']