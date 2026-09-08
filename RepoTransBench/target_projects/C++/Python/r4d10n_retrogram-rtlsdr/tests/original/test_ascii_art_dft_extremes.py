import numpy as np
from src.retrogram_rtlsdr.ascii_art_dft import dft_to_plot, log_pwr_dft

def test_dfttoplot_handles_inf_and_nan():
    dft = [0.0]*8
    dft[2] = float('inf')
    dft[3] = float('-inf')
    dft[4] = float('nan')
    plot = dft_to_plot(dft, 8, 3, 1e6, 0, 10, 0)
    assert plot != ''

def test_dfttoplot_handles_very_wide_range():
    dft = [1e6 if i % 2 == 0 else -1e6 for i in range(16)]
    plot = dft_to_plot(dft, 16, 8, 1e3, 0, 1e7, 0)
    assert plot != ''

def test_dfttoplot_large_and_zero_reference():
    dft = [-100.0]*16
    plot = dft_to_plot(dft, 16, 6, 1e6, 0, 10, 1e6)
    assert plot != ''
    plot = dft_to_plot(dft, 16, 6, 1e6, 0, 10, -1e6)
    assert plot != ''

def test_logpwrdft_edge_input_all_ones():
    inbuf = [1.0+0.0j]*8
    out = log_pwr_dft(inbuf, len(inbuf))
    assert len(out) == 8
    for v in out:
        assert np.isfinite(v)

def test_logpwrdft_edge_input_all_minus_one():
    inbuf = [-1.0+0.0j]*8
    out = log_pwr_dft(inbuf, len(inbuf))
    assert len(out) == 8
    for v in out:
        assert np.isfinite(v)