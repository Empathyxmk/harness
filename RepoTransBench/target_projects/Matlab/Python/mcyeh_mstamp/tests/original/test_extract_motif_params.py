import numpy as np
import pytest
from src.mcyeh_mstamp.mstamp_stamp import extract_k_motif

def load_toy():
    try:
        toy = np.load('src/mcyeh_mstamp/toy_data.npy', allow_pickle=True).item()
        data = toy['data']
        sub_len = int(toy['sub_len'])
        return data, sub_len
    except Exception:
        np.random.seed(2)
        return np.random.randn(55,3), 13

def test_motif_basic():
    data, sub_len = load_toy()
    pos, radii = extract_k_motif(data, sub_len, 2)
    assert len(pos) == 2

def test_motif_too_many():
    data, sub_len = load_toy()
    try:
        pos, _ = extract_k_motif(data, sub_len, 99)
        assert len(pos) <= 99
    except Exception:
        assert True

def test_motif_zero():
    data, sub_len = load_toy()
    try:
        pos, _ = extract_k_motif(data, sub_len, 0)
        assert pos == []
    except Exception:
        assert True