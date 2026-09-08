from qcore.microtime import microtime, now, seconds, millitime
from qcore.asserts import assert_eq, assert_is_instance

def test_public_microtime_return_type():
    t = microtime()
    assert_is_instance(t, float)
    t2 = microtime()
    assert t2 >= t

def test_public_now_and_seconds_are_ints():
    t1 = now()
    t2 = seconds()
    assert_is_instance(t1, int)
    assert_is_instance(t2, int)
    assert t1 >= 0
    assert t2 >= 0

def test_public_millitime_is_int():
    mt = millitime()
    assert_is_instance(mt, int)
    assert mt >= 0