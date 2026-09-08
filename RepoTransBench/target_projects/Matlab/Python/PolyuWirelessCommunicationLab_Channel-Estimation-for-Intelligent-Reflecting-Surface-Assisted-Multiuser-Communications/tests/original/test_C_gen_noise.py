import numpy as np
from src.channel_estimation.c_gen import C_gen

def test_RealNoiseOriginal():
    D = 2
    c_bs = 1
    actual = C_gen(D, c_bs)
    expected = np.array([[1, 1], [1, 1]], dtype=np.complex128)
    np.testing.assert_allclose(actual, expected, atol=1e-12)

def test_ComplexNoiseOriginal():
    D = 2
    c_bs = 1-1j
    actual = C_gen(D, c_bs)
    expected = np.array([[1, 1-1j], [1+1j, 1]], dtype=np.complex128)
    np.testing.assert_allclose(actual, expected, atol=1e-12)