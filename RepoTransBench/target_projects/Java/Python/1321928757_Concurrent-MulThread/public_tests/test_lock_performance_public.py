import threading

def test_reentrant_lock_low_contention():
    lock = threading.Lock()
    sum_val = 0
    N = 50
    for i in range(N):
        lock.acquire()
        try:
            sum_val += i
        finally:
            lock.release()
    assert sum_val > 0