import numpy as np
from src.channel_estimation.c_gen import C_gen

def test_RealPublic():
    D = 3
    c_bs = 2
    actual = C_gen(D, c_bs)
    expected = np.array([[1, 2, 2], [2, 1, 2], [2, 2, 1]], dtype=np.complex128)
    np.testing.assert_allclose(actual, expected, atol=1e-12)

def test_ComplexPublic():
    D = 3
    c_bs = -2j
    actual = C_gen(D, c_bs)
    expected = np.array([[1, -2j, -2j], [2j, 1, -2j], [2j, 2j, 1]], dtype=np.complex128)
    np.testing.assert_allclose(actual, expected, atol=1e-12)