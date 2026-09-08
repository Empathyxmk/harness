import numpy as np
from src.mcyeh_mstamp.mstamp_stamp import mstamp, guide_serach, plot_motif_on_data, unconstrain_search, extract_k_motif

def test_demo_basic():
    # Load toy data (replace this with real toy_data.npy in production)
    try:
        import numpy as np
        # Try loading serialized toy_data (must be a dict with 'data' and 'sub_len')
        toy = np.load('src/mcyeh_mstamp/toy_data.npy', allow_pickle=True).item()
        data = toy['data']
        sub_len = int(toy['sub_len'])
    except Exception:
        # Fallback: Random data for testing structure (not meaningful)
        np.random.seed(42)
        data = np.random.randn(55, 3)
        sub_len = 12

    # alternative 1.a: the basic version
    must_dim = []
    exc_dim = []
    pro_mul, pro_idx = mstamp(data, sub_len, must_dim, exc_dim)
    assert pro_mul.shape[0] == data.shape[0] - sub_len + 1
    assert pro_mul.shape == pro_idx.shape

    # alternative 1.b (commented out above)
    # must_dim = [1]
    # exc_dim = []
    # pro_mul, pro_idx = mstamp(data, sub_len, must_dim, exc_dim)

    # alternative 1.c (commented out above)
    # must_dim = []
    # exc_dim = [3]
    # pro_mul, pro_idx = mstamp(data, sub_len, must_dim, exc_dim)
    # pro_mul = pro_mul[:, :2]
    # pro_idx = pro_idx[:, :2]
    # data = data[:, :2]

    # alternative 2: using "parallel" version (simulated)
    # n_work = 4
    # pro_mul, pro_idx = mstamp_par(data, sub_len, n_work)

    # alternative 3: anytime version with stop pct
    # pct_stop = 0.1
    # pro_mul, pro_idx = mstamp_any(data, sub_len, pct_stop)

    # guided search for 2-dimensional motif
    n_dim = 2
    motif_idx, motif_dim = guide_serach(data, sub_len, pro_mul, pro_idx, n_dim)
    assert isinstance(motif_dim, list) or isinstance(motif_dim, np.ndarray)
    plot_motif_on_data(data, sub_len, motif_idx, motif_dim)

    # extract motif using unconstrained search method
    n_bit = 4
    k = 2
    motif_idx, motif_dim = unconstrain_search(data, sub_len, pro_mul, pro_idx, n_bit, k)
    plot_motif_on_data(data, sub_len, motif_idx, motif_dim)

    # 1D matrix profile
    pro_mul_2, _ = mstamp(data[:, 1], sub_len, must_dim, exc_dim)
    assert pro_mul_2.shape[0] == data.shape[0] - sub_len + 1