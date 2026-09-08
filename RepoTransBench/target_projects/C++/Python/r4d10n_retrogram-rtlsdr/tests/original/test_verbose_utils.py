import numpy as np

class DummyDev:
    pass

def stub_set_center_freq(dev, freq):
    return -1
def stub_set_freq_correction(dev, ppm):
    return 0
def stub_set_sample_rate(dev, sr):
    return 42
def stub_set_tuner_gain_mode(dev, val):
    return -1
def stub_get_tuner_gains(dev, arr):
    return 0

def verbose_set_frequency(dev, freq):
    return stub_set_center_freq(dev, freq)
def verbose_set_freq_correction(dev, ppm):
    return stub_set_freq_correction(dev, ppm)
def verbose_set_sample_rate(dev, sr):
    return stub_set_sample_rate(dev, sr)
def nearest_gain(dev, tg):
    return stub_get_tuner_gains(dev, None)

def test_verbose_set_frequency_error():
    dev = DummyDev()
    ret = verbose_set_frequency(dev, 12345)
    assert ret < 0

def test_verbose_set_freq_correction_ok():
    dev = DummyDev()
    ret = verbose_set_freq_correction(dev, 1)
    assert ret == 0

def test_verbose_set_sample_rate_fail():
    dev = DummyDev()
    ret = verbose_set_sample_rate(dev, 48000)
    assert ret == 42

def test_verbose_nearest_gain_no_gains():
    dev = DummyDev()
    ret = nearest_gain(dev, 10)
    assert ret == 0