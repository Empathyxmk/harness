import threading
import time

class OnlySyncByAQS:
    def __init__(self):
        self._lock = threading.Lock()

    def lock(self):
        self._lock.acquire()

    def unlock(self):
        self._lock.release()

def test_custom_aqs_lock_multiple_threads():
    lock = OnlySyncByAQS()
    num_threads = 4
    counter = [0]  # Use list for mutability

    def use_lock():
        lock.lock()
        try:
            counter[0] += 1
            time.sleep(0.25)
        finally:
            lock.unlock()

    threads = [threading.Thread(target=use_lock) for _ in range(num_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert counter[0] == num_threads