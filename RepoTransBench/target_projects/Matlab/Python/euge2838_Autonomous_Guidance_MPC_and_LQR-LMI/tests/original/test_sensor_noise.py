import pytest
import numpy as np

# Dummy definition for sensor_noise. Replace with import from actual module as needed.
def sensor_noise(signal, noise_std):
    rng = np.random.default_rng(42)
    return np.array(signal) + rng.normal(0, noise_std, size=np.shape(signal))

def test_sensor_noise():
    sensor_signal = np.ones(100)
    noise_std = 0.1
    noisy_signal = sensor_noise(sensor_signal, noise_std)

    assert noisy_signal.shape[0] == 100
    # There should be at least one entry that is different (i.e., noise added)
    assert np.any(np.abs(noisy_signal - sensor_signal) > 0)