import numpy as np
from src.retrogram_rtlsdr.ascii_art_dft import to_clean_num, log_pwr_dft

def call_iround_public(v):
    return int(v + 0.5) if v > 0 else int(v - 0.5)

def test_helpers_public_iround_different_vals():
    assert call_iround_public(2.4) == 2
    assert call_iround_public(2.6) == 3
    assert call_iround_public(-2.1) == -2
    assert call_iround_public(-2.6) == -3

def test_helpers_public_to_clean_num_other_cases():
    assert to_clean_num(207) == 200
    assert to_clean_num(650) == 600
    assert to_clean_num(-1421) == -1000
    assert to_clean_num(0) == 0

def test_helpers_public_ctfft_different_input():
    arr = [2.0+1.0j] * 3
    out = log_pwr_dft(arr, len(arr))
    assert len(out) == 3
    for v in out:
        assert np.isfinite(v)