import pytest
import numpy as np

def sensor_noise(signal, noise_std):
    rng = np.random.default_rng(0)
    return np.array(signal) + rng.normal(0, noise_std, size=np.shape(signal))

def test_public_test_sensor_noise():
    sensor_signal = np.linspace(0, 1, 50)
    noise_std = 0.2
    noisy_signal = sensor_noise(sensor_signal, noise_std)

    assert noisy_signal.shape[0] == 50
    assert np.any(np.abs(noisy_signal - sensor_signal) > 0)