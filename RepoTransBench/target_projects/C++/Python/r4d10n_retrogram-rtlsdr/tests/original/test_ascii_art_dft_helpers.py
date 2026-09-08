import numpy as np
from src.retrogram_rtlsdr.ascii_art_dft import to_clean_num, log_pwr_dft

def call_iround(v):
    return int(v + 0.5) if v > 0 else int(v - 0.5)

def test_helpers_iround():
    assert call_iround(1.3) == 1
    assert call_iround(1.7) == 2
    assert call_iround(-1.2) == -1
    assert call_iround(-1.7) == -2

def test_helpers_to_clean_num():
    assert to_clean_num(0) == 0
    assert to_clean_num(103) == 100
    assert to_clean_num(425) == 400
    assert to_clean_num(-999) == -1000

def test_helpers_ctfft_k():
    arr = [1.0+0j] * 4
    out = log_pwr_dft(arr, len(arr))
    assert len(out) == 4
    for v in out:
        assert np.isfinite(v)