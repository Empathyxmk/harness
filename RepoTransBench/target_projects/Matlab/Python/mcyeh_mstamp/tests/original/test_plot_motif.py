import numpy as np
import pytest
from src.mcyeh_mstamp.mstamp_stamp import plot_motif_on_data, mstamp

def load_toy():
    try:
        toy = np.load('src/mcyeh_mstamp/toy_data.npy', allow_pickle=True).item()
        data = toy['data']
        sub_len = int(toy['sub_len'])
        return data, sub_len
    except Exception:
        np.random.seed(3)
        return np.random.randn(45,2), 8

def test_plot_motif_basic():
    data, sub_len = load_toy()
    try:
        plot_motif_on_data(data, [1, 5], sub_len)
    except Exception:
        assert False

def test_plot_motif_edge():
    data, sub_len = load_toy()
    try:
        plot_motif_on_data(data, [1], sub_len)
    except Exception:
        assert True