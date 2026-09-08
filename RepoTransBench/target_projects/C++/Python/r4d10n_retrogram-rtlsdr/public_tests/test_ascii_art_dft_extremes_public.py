from src.retrogram_rtlsdr.ascii_art_dft import dft_to_plot

def test_dfttoplot_public_handles_inf_and_nan_opposite():
    dft = [0.0]*8
    dft[1] = float('inf')
    dft[5] = float('-inf')
    dft[6] = float('nan')
    plot = dft_to_plot(dft, 8, 5, 2e6, 42, 12, 3)
    assert plot != ''

def test_dfttoplot_public_handles_extremely_wide_range():
    dft = [1e5 if i % 3 == 0 else -1e5 for i in range(10)]
    plot = dft_to_plot(dft, 10, 4, 2e3, 0, 1e6, -42)
    assert plot != ''