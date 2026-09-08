import numpy as np
from src.retrogram_rtlsdr.ascii_art_dft import log_pwr_dft, dft_to_plot

def float_vec_close(v1, v2, tol=1e-3):
    if len(v1) != len(v2):
        return False
    for a, b in zip(v1, v2):
        if abs(a - b) > tol:
            return False
    return True

def test_logpwrdft_single_sample_zero():
    inbuf = [0.0 + 0.0j]
    out = log_pwr_dft(inbuf, 1)
    assert len(out) == 1

def test_logpwrdft_two_samples_delta():
    inbuf = [1.0 + 0.0j, 0.0 + 0.0j]
    out = log_pwr_dft(inbuf, 2)
    assert len(out) == 2
    # Both values should be finite
    assert np.isfinite(out[0])
    assert np.isfinite(out[1])

def test_logpwrdft_many_samples_sine():
    N = 32
    inbuf = [np.sin(2 * np.pi * i / N) + 0.0j for i in range(N)]
    out = log_pwr_dft(inbuf, N)
    assert len(out) == N

def test_dfttoplot_typical_values():
    flat = [-50.0] * 8
    plot = dft_to_plot(flat, 8, 4, 2e6, 0, 60, 0)
    assert plot != ''
    assert '\n' in plot

def test_dfttoplot_dynamic_range():
    dft = [0, -10, -20, -30, -40, -50, -60, -70]
    plot = dft_to_plot(dft, 8, 4, 2e6, 1000, 50, -10)
    assert "dB" in plot

def test_dfttoplot_tiny_input():
    dft = [-90.0]
    plot = dft_to_plot(dft, 1, 2, 1e6, 0, 20, 0)
    assert plot != ''

def test_dfttoplot_cheesy_boundaries():
    dft = [-10.0] * 16
    plot = dft_to_plot(dft, 16, 1, 1e6, 0, 200, 100)
    assert plot != ''
    plot = dft_to_plot(dft, 16, 1, 1e6, 0, 0.001, -10)
    assert plot != ''