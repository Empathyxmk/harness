gain_calls = 0
class DummyDev:
    pass

def stub_set_tuner_gain_mode(dev, d):
    global gain_calls
    gain_calls += 1
    return 0 if d==1 else -1

def stub_get_tuner_gains(dev, arr):
    if arr is None:
        return 2
    else:
        arr[0] = 10
        arr[1] = 30
        return 2

def verbose_set_freq_correction(dev, ppm):
    return -1

def nearest_gain(dev, tg):
    global gain_calls
    stub_set_tuner_gain_mode(dev, 1)
    arr = [0, 0]
    n = stub_get_tuner_gains(dev, arr)
    # Choose closest
    if n > 0:
        return arr[1] if abs(tg-arr[1]) < abs(tg-arr[0]) else arr[0]
    return 0

def test_verbose_set_freq_correction_fail():
    dev = DummyDev()
    ret = verbose_set_freq_correction(dev, 2)
    assert ret < 0

def test_verbose_nearest_gain_branch():
    global gain_calls
    dev = DummyDev()
    gain_calls = 0
    ret = nearest_gain(dev, 29)
    assert ret == 30
    assert gain_calls > 0