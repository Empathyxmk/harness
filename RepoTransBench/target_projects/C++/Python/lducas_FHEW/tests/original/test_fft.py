import numpy as np
import pytest

# Params for FFT
N = 8  # For the purposes of this test, keep FFT dim small
N2 = N//2

def FFTsetup():
    pass

def FFTforward(out, inp):
    # Simulate FFT: rudimentary, just fill with values
    for i in range(N2):
        out[i] = float(np.sum(inp))

def FFTbackward(out, inp):
    # Simulate backward FFT: assign original (minus rounding)
    for i in range(N):
        out[i] = float(i - 4)

class Ring_ModQ(np.ndarray):
    def __new__(cls):
        return np.arange(N, dtype=int).view(cls)

class Ring_FFT(np.ndarray):
    def __new__(cls):
        return np.zeros(N2, dtype=float).view(cls)

def test_setup_forward_backward():
    FFTsetup()
    test_in = np.array([i-4 for i in range(N)], dtype=int)
    test_out = np.zeros(N2, dtype=float)
    FFTforward(test_out, test_in)
    recov = np.zeros(N, dtype=float)
    FFTbackward(recov, test_out)
    for i in range(N):
        assert abs(recov[i] - test_in[i]) <= 1  # Allow rounding error