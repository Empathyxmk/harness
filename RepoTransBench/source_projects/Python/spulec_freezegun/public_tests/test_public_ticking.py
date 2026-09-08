import time

def test_public_ticking_time_progression():
    t1 = time.time()
    time.sleep(0.002)
    t2 = time.time()
    assert t2 > t1

def test_public_ticking_perf_counter():
    c1 = time.perf_counter()
    time.sleep(0.003)
    c2 = time.perf_counter()
    assert c2 > c1