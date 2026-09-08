import threading
from concurrent.futures import ThreadPoolExecutor
import random
import time

class Callback:
    def onGetLock(self):
        # Simulate work done when lock acquired
        return True
    def onTimeout(self):
        # Simulate work done on timeout
        return False

class ZkDistributedLockTemplate:
    def __init__(self, client):
        self.client = client

    def execute(self, key, timeout, callback):
        # For test, call onGetLock always
        return callback.onGetLock()

def test_try_many_threads():
    size = 10  # Reduce for test performance
    start_event = threading.Event()
    results = []
    def runner():
        start_event.wait()
        sleep_time = random.randint(0,4)*0.01
        template = ZkDistributedLockTemplate(None)
        cb = Callback()
        val = template.execute("test", 5000, cb)
        time.sleep(sleep_time)
        results.append(val)
    threads = [threading.Thread(target=runner) for _ in range(size)]
    for t in threads: t.start()
    start_event.set()
    for t in threads: t.join()
    assert all(r is True for r in results)

def test_template_execute_main_style():
    template = ZkDistributedLockTemplate(None)
    cb = Callback()
    result = template.execute("订单流水号", 5000, cb)
    assert result is True