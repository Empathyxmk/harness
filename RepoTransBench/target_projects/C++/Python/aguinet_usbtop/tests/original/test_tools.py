import time

def get_current_timestamp():
    return time.time()

def test_get_current_timestamp():
    t1 = get_current_timestamp()
    time.sleep(0.01)
    t2 = get_current_timestamp()
    assert t1 < t2