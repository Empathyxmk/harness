class DummyDev:
    pass

def stub_set_center_freq_pub(dev, freq):
    return 0
def stub_set_freq_correction_pub(dev, ppm):
    return -2
def stub_set_sample_rate_pub(dev, sr):
    return 0
def stub_set_tuner_gain_mode_pub(dev, val):
    return 0
def stub_get_tuner_gains_pub(dev, arr):
    return 3

def verbose_set_frequency(dev, freq):
    return stub_set_center_freq_pub(dev, freq)
def verbose_set_freq_correction(dev, ppm):
    return stub_set_freq_correction_pub(dev, ppm)
def verbose_set_sample_rate(dev, sr):
    return stub_set_sample_rate_pub(dev, sr)
def nearest_gain(dev, tg):
    return stub_get_tuner_gains_pub(dev, None)

def test_verbose_public_set_frequency_ok():
    dev = DummyDev()
    ret = verbose_set_frequency(dev, 98765)
    assert ret == 0

def test_verbose_public_set_freq_correction_fail():
    dev = DummyDev()
    ret = verbose_set_freq_correction(dev, 15)
    assert ret == -2

def test_verbose_public_set_sample_rate_ok():
    dev = DummyDev()
    ret = verbose_set_sample_rate(dev, 96000)
    assert ret == 0

def test_verbose_public_nearest_gain_gains_exist():
    dev = DummyDev()
    ret = nearest_gain(dev, 100)
    assert ret == 3