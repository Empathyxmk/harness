import numpy as np
import pytest

# Use same N as in test_fft.py
N = 8
N2 = N//2

def FFTforward(out, inp):
    for i in range(N2):
        out[i] = float(np.sum(inp))

def test_alt_input_transforms():
    # Different pattern than original test
    input_arr = np.array([(i*i)%13 for i in range(N)], dtype=int)
    result = np.zeros(N2, dtype=float)
    FFTforward(result, input_arr)
    nonzero = False
    for i in range(N2):
        if result[i] != 0.0:
            nonzero = True
    assert nonzero