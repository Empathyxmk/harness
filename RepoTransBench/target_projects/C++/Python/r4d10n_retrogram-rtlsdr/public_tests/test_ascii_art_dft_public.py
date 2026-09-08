import numpy as np
from src.retrogram_rtlsdr.ascii_art_dft import log_pwr_dft, dft_to_plot

def float_vec_close_pub(v1, v2, tol=1e-3):
    if len(v1) != len(v2):
        return False
    for a, b in zip(v1, v2):
        if abs(a - b) > tol:
            return False
    return True

def test_logpwrdft_public_single_sample_one():
    inbuf = [1.0 + 0.0j]
    out = log_pwr_dft(inbuf, 1)
    assert len(out) == 1
    assert np.isfinite(out[0])

def test_logpwrdft_public_two_samples_alternating():
    inbuf = [-1.0+0.0j, 1.0+0.0j]
    out = log_pwr_dft(inbuf, 2)
    assert len(out) == 2
    assert np.isfinite(out[0])
    assert np.isfinite(out[1])
    assert out[0] != out[1]

def test_logpwrdft_public_many_samples_cosine():
    N = 24
    inbuf = [np.cos(2 * np.pi * i / (N/2)) + (np.sin(2 * np.pi * i / (N/2))/2.0)*1j for i in range(N)]
    out = log_pwr_dft(inbuf, N)
    assert len(out) == N
    for v in out:
        assert np.isfinite(v)

def test_dfttoplot_public_stepped_spectrum():
    stepped = [-40.0 + 2 * i for i in range(10)]
    plot = dft_to_plot(stepped, 10, 5, 2.5e6, 500, 25, 10)
    assert plot != ''
    assert '\n' in plot

def test_dfttoplot_public_negative_dynamic_range():
    dft = [-10, -20, -30, -40, -50, -60, -70, -80]
    plot = dft_to_plot(dft, 8, 3, 2.25e6, 2000, 70, -20)
    assert "dB" in plot

def test_dfttoplot_public_minimal_input():
    dft = [-100.0, -100.0]
    plot = dft_to_plot(dft, 2, 2, 1.1e6, 12, 10, -75)
    assert plot != ''

def test_dfttoplot_public_boundary_checks():
    dft = [-7.0]*14
    plot = dft_to_plot(dft, 14, 1, 1.5e6, 2, 99, 44)
    assert plot != ''
    plot = dft_to_plot(dft, 14, 1, 1.5e6, 2, 0.01, -7)
    assert plot != ''