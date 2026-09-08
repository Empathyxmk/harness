import pytest
import numpy as np
from src.sp import sig_delay

def test_no_delay():
    sig = np.ones((10, 1))
    R = 0
    fc = 1e9
    fs = 1e6
    out = sig_delay(sig, R, fc, fs)
    assert out.shape == (10, 1)
    assert np.linalg.norm(out[:10] - sig) < 1e-10

def test_with_delay():
    sig = np.array([[1], [2], [3], [4], [5]])
    R = 3e8
    fc = 3e9
    fs = 1
    out = sig_delay(sig, R, fc, fs)
    delay_N = round((R/3e8)/1)
    assert out.shape == (5 + delay_N, 1)
    phase = np.exp(1j * R / (3e8 / fc) * 2 * np.pi)
    assert np.linalg.norm(out[delay_N:]-sig*phase) < 1e-8

def test_short_signal():
    sig = np.random.randn(3, 1) + 1j*np.random.randn(3, 1)
    R = 0.5
    fc = 1e6
    fs = 1e6
    out = sig_delay(sig, R, fc, fs)
    assert len(out.shape) == 2 and (out.shape[0] == 3 or out.shape[1] == 1)

def test_phase_rotation_real_imag():
    sig = np.ones((2, 1))
    R = 10
    fc = 100e6
    fs = 10e6
    out = sig_delay(sig, R, fc, fs)
    phi = np.exp(1j * R / (3e8 / fc) * 2 * np.pi)
    expected = sig * phi
    assert np.linalg.norm(out[:2] - expected) < 1e-10

def test_zero_fs():
    sig = np.array([[1], [2], [3]])
    R = 1
    fc = 2e9
    fs = 1e12
    out = sig_delay(sig, R, fc, fs)
    assert out.shape == (3, 1)