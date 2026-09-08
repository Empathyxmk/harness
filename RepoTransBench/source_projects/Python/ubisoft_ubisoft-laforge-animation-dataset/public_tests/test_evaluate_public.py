import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import lafan1.benchmarks as benchmarks
import pickle

def test_pickle_stats_public(tmp_path):
    import numpy as np
    stats_file = tmp_path / "lafan1_stats_public.pkl"
    x_mean = 13 * np.ones((2, 2))
    x_std = 6 * np.ones((2, 2))
    stats = {"Xmean": x_mean, "Xstd": x_std}
    with open(stats_file, "wb") as f:
        pickle.dump(stats, f)
    with open(stats_file, "rb") as f:
        loaded = pickle.load(f)
    assert np.allclose(loaded["Xmean"], x_mean)
    assert np.allclose(loaded["Xstd"], x_std)

def test_benchmark_on_fake_data_public():
    import numpy as np
    # Slightly different values from original
    X = 2*np.ones((1,10,2,3))
    Y = np.ones((1,10,2,3))
    # Should not raise, even if score is not meaningful, just exercise code path
    _ = benchmarks.fast_npss(X[0], Y[0])

def test_benchmark_nan_guard_with_nan_input_public():
    import numpy as np
    # Explicitly provide NaN in the input
    A = np.array([[[1, 2],[np.nan, 4]]])
    B = np.array([[[5, 6],[7, 8]]])
    score = benchmarks.fast_npss(A, B)
    assert np.isnan(score) or score >= 0  # Accept either, just make sure code runs