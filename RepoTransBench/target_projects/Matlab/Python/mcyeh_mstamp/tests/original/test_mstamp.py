import numpy as np
import pytest
from src.mcyeh_mstamp.mstamp_stamp import mstamp, mstamp_any, extract_k_motif, guide_serach

def load_toy():
    try:
        toy = np.load('src/mcyeh_mstamp/toy_data.npy', allow_pickle=True).item()
        data = toy['data']
        sub_len = int(toy['sub_len'])
        return data, sub_len
    except Exception:
        np.random.seed(3)
        return np.random.randn(60,3), 13

def test_basic_mstamp():
    data, sub_len = load_toy()
    must_dim = []
    exc_dim = []
    pro_mul, pro_idx = mstamp(data, sub_len, must_dim, exc_dim)
    assert pro_mul.shape == pro_idx.shape
    assert np.all(~np.isnan(pro_mul) | np.isinf(pro_mul))

def test_mstamp_with_must_dim():
    data, sub_len = load_toy()
    must_dim = [1]
    exc_dim = []
    pro_mul, pro_idx = mstamp(data, sub_len, must_dim, exc_dim)
    assert pro_mul.shape[1] >= max(must_dim)

def test_mstamp_with_exc_dim():
    data, sub_len = load_toy()
    must_dim = []
    exc_dim = [2]
    pro_mul, pro_idx = mstamp(data, sub_len, must_dim, exc_dim)
    assert pro_mul.shape[1] >= max(exc_dim)

def test_mstamp_error_sub_len_too_large():
    data, sub_len = load_toy()
    must_dim = []
    exc_dim = []
    sl = data.shape[0]
    with pytest.raises(Exception):
        mstamp(data, sl, must_dim, exc_dim)

def test_mstamp_error_sub_len_too_small():
    data, sub_len = load_toy()
    must_dim = []
    exc_dim = []
    with pytest.raises(Exception):
        mstamp(data, 2, must_dim, exc_dim)

def test_mstamp_error_must_exc_overlap():
    data, sub_len = load_toy()
    must_dim = [1]
    exc_dim = [1]
    with pytest.raises(Exception):
        mstamp(data, sub_len, must_dim, exc_dim)

def test_mstamp_any_nominal():
    data, sub_len = load_toy()
    pct = 0.5
    pro_mul, pro_idx = mstamp_any(data, sub_len, pct)
    assert np.all(np.isfinite(pro_idx) | (pro_idx == 0))

def test_mstamp_any_pct_bounds():
    data, sub_len = load_toy()
    with pytest.raises(Exception):
        mstamp_any(data, sub_len, -1)
    with pytest.raises(Exception):
        mstamp_any(data, sub_len, 2)

def test_extract_k_motif_nominal():
    data, sub_len = load_toy()
    must_dim = []
    exc_dim = []
    pro_mul, pro_idx = mstamp(data, sub_len, must_dim, exc_dim)
    n_bit = 8
    k = 2
    motif_idx, motif_dim = extract_k_motif(data, sub_len, pro_mul, pro_idx, n_bit, k)
    assert len(motif_idx) >= 1
    assert isinstance(motif_dim, list)

def test_guide_serach_nominal():
    data, sub_len = load_toy()
    must_dim = []
    exc_dim = []
    pro_mul, pro_idx = mstamp(data, sub_len, must_dim, exc_dim)
    n_dim = 1
    motif_idx, motif_dim = guide_serach(data, sub_len, pro_mul, pro_idx, n_dim)
    assert isinstance(motif_idx, np.ndarray)
    assert isinstance(motif_dim, list)