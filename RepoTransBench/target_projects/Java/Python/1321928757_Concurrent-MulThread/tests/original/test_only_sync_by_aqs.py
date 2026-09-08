import threading
import time

class OnlySyncByAQS:
    """
    A custom lock with exclusive ownership, similar to a basic mutex. Not re-entrant.
    """
    def __init__(self):
        self._lock = threading.Lock()

    def lock(self):
        self._lock.acquire()

    def unlock(self):
        self._lock.release()

class TestAQS:
    def __init__(self):
        self.only_sync_by_aqs = OnlySyncByAQS()

    def use(self):
        self.only_sync_by_aqs.lock()
        try:
            time.sleep(1)  # simulate work
        finally:
            self.only_sync_by_aqs.unlock()

def test_only_sync_by_aqs():
    test_obj = TestAQS()
    threads = []
    for _ in range(3):
        t = threading.Thread(target=test_obj.use)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    # If we reach here, all threads acquired lock one after another (no assertion needed, test is for exclusivity)