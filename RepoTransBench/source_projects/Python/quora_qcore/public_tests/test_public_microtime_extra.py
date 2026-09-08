from qcore.microtime import now, seconds, millitime, microtime
from qcore.asserts import assert_eq

def test_public_microtime_all_greater():
    t1 = now()
    t2 = seconds()
    t3 = millitime()
    t4 = microtime()
    assert t1 >= 0
    assert t2 >= 0
    assert t3 >= 0
    assert t4 >= 0