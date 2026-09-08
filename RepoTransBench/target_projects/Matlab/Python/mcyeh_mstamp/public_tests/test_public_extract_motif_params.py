import numpy as np
from src.mcyeh_mstamp.mstamp_stamp import mstamp_par, extract_k_motif

def test_public_extract_motif_params_basic():
    t = np.linspace(0, 4*np.pi, 50)
    data = np.column_stack([np.cos(t), np.cos(t+0.5)])
    data += np.random.randn(*data.shape)*0.05
    sub_len = 12
    pro_mul, pro_idx = mstamp_par(data, sub_len, 2)
    n_bit = 4
    k = 2
    motif_idx, motif_dim = extract_k_motif(data, sub_len, pro_mul, pro_idx, n_bit, k)
    assert len(motif_idx) > 0
    assert isinstance(motif_dim, list)