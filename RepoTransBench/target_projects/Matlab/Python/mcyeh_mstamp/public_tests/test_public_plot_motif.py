import numpy as np
import matplotlib.pyplot as plt
from src.mcyeh_mstamp.mstamp_stamp import mstamp_par, plot_motif_on_data

def test_public_plot_motif_on_data():
    x = np.arange(0, 38.1, 0.3)
    data = np.column_stack([np.cos(x) + np.random.randn(len(x))*0.04,
                            np.sin(x) + np.random.randn(len(x))*0.04])
    sub_len = 9
    pro_mul, pro_idx = mstamp_par(data, sub_len, 2)
    sel_idx = np.random.randint(0, pro_idx.shape[0])
    try:
        plot_motif_on_data(data, sub_len, [sel_idx, sel_idx+2], [1])
    except Exception:
        assert False