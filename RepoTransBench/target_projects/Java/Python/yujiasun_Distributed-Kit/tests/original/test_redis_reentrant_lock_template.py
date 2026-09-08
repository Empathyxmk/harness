import threading
import random
import time

class Callback:
    def onGetLock(self):
        return True
    def onTimeout(self):
        return False

class RedisDistributedLockTemplate:
    def __init__(self, jp):
        self.jp = jp

    def execute(self, key, timeout, callback):
        # Simulate callback execution
        return callback.onGetLock()

def test_try_many_threads():
    size = 10
    start_event = threading.Event()
    results = []
    def runner():
        start_event.wait()
        sleep_time = random.randint(0,4)*0.01
        template = RedisDistributedLockTemplate(None)
        cb = Callback()
        val = template.execute("test", 5000, cb)
        time.sleep(sleep_time)
        results.append(val)
    threads = [threading.Thread(target=runner) for _ in range(size)]
    for t in threads: t.start()
    start_event.set()
    for t in threads: t.join()
    assert all(r is True for r in results)