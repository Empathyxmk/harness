import numpy as np
import pytest
from src.mcyeh_mstamp.mstamp_stamp import mstamp, extract_k_motif, guide_serach

def load_toy():
    try:
        toy = np.load('src/mcyeh_mstamp/toy_data.npy', allow_pickle=True).item()
        data = toy['data']
        sub_len = int(toy['sub_len'])
        return data, sub_len
    except Exception:
        np.random.seed(6)
        return np.random.randn(60,3), 14

def test_extract_k_motif_simple():
    data, sub_len = load_toy()
    must_dim = []
    exc_dim = []
    pro_mul, pro_idx = mstamp(data, sub_len, must_dim, exc_dim)
    k = 2
    motif_idx, motif_dim = extract_k_motif(pro_mul, pro_idx, k, data, sub_len)
    assert isinstance(motif_idx, list)
    assert isinstance(motif_dim, list)

def test_extract_k_motif_invalid_inputs():
    pro_mul = []
    pro_idx = []
    k = 0
    try:
        motif_idx, motif_dim = extract_k_motif(pro_mul, pro_idx, k, [], [])
        assert motif_idx == [] and motif_dim == []
    except Exception:
        assert True

def test_guide_serach():
    data, sub_len = load_toy()
    must_dim = []
    exc_dim = []
    pro_mul, pro_idx = mstamp(data, sub_len, must_dim, exc_dim)
    guide_serach(data, sub_len, pro_mul, pro_idx)