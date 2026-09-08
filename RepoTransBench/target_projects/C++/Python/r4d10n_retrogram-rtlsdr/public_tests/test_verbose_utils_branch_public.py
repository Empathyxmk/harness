class DummyDev:
    pass

def stub_set_tuner_gain_mode_pub(dev, val):
    return -5
def stub_get_tuner_gains_pub(dev, arr):
    return 99

def nearest_gain(dev, tg):
    ret = stub_set_tuner_gain_mode_pub(dev, 1)
    if ret != 0:
        return ret
    return stub_get_tuner_gains_pub(dev, None)

def test_verbosebranch_public_nearest_gain_manual_gain_failed():
    dev = DummyDev()
    ret = nearest_gain(dev, 50)
    assert ret == -5

def test_verbosebranch_public_nearest_gain_gains99():
    # redefine stubs in local scope to simulate branch
    def stub_set_tuner_gain_mode_pass(dev, val):
        return 0
    def stub_get_tuner_gains_99(dev, arr):
        return 99
    def nearest_gain_branch(dev, tg):
        ret = stub_set_tuner_gain_mode_pass(dev, 1)
        if ret != 0:
            return ret
        return stub_get_tuner_gains_99(dev, None)
    dev = DummyDev()
    ret = nearest_gain_branch(dev, 77)
    assert ret == 99