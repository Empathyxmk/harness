import numpy as np
from src.mcyeh_mstamp.mstamp_stamp import mstamp_par, extract_k_motif

def test_public_extract_and_guide_simple():
    from scipy.signal import sawtooth
    x = np.arange(1,81)
    data = np.column_stack([sawtooth(2*np.pi*x/25), sawtooth(2*np.pi*(x+7)/25)])
    data += np.random.randn(*data.shape)*0.1
    sub_len = 16
    pro_mul, pro_idx = mstamp_par(data, sub_len, 2)
    n_bit = 3
    k = 1
    motif_idx, motif_dim = extract_k_motif(data, sub_len, pro_mul, pro_idx, n_bit, k)
    assert motif_idx[0] >= 1
    assert motif_idx[0] <= data.shape[0]-sub_len+1
    assert isinstance(motif_dim, list)