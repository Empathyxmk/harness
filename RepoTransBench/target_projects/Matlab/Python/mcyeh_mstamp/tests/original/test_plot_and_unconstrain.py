import numpy as np
from src.mcyeh_mstamp.mstamp_stamp import mstamp, plot_motif_on_data, unconstrain_search

def load_toy():
    try:
        toy = np.load('src/mcyeh_mstamp/toy_data.npy', allow_pickle=True).item()
        data = toy['data']
        sub_len = int(toy['sub_len'])
        return data, sub_len
    except Exception:
        np.random.seed(4)
        return np.random.randn(55,3), 13

def test_plot_motif_on_data_basic():
    data, sub_len = load_toy()
    must_dim = []
    exc_dim = []
    pro_mul, pro_idx = mstamp(data, sub_len, must_dim, exc_dim)
    motif_idx = [1, 2]
    motif_dim = [1, 2]
    plot_motif_on_data(data, motif_idx, motif_dim, sub_len)

def test_unconstrain_search_basic():
    data, sub_len = load_toy()
    unconstrain_search(data, sub_len)

def test_unconstrain_search_input():
    data, sub_len = load_toy()
    must_dim = []
    exc_dim = []
    pro_mul, pro_idx = mstamp(data, sub_len, must_dim, exc_dim)
    unconstrain_search(data, sub_len, pro_mul, pro_idx)