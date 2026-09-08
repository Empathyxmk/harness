import threading
import time

class DummyThreadPool:
    def __init__(self, core, queue_cap, max_size, keep_alive, policy, name):
        self.threads = []
        self.queue = []
        self.core = core
        self.max_size = max_size
        self.shutdown_called = False
        self.name = name

    def execute(self, fn):
        t = threading.Thread(target=fn)
        self.threads.append(t)
        t.start()

    def shutdown(self):
        self.shutdown_called = True
        for t in self.threads:
            t.join()

    def isTerminated(self):
        return all(not t.is_alive() for t in self.threads)

def test_public_thread_pool():
    import time
    from threading import Event
    sum_val = [0]
    pool = DummyThreadPool(
        core=2, queue_cap=3, max_size=4, keep_alive=1000,
        policy='abort', name="PublicTestPool"
    )
    number_of_tasks = 7
    lock = threading.Lock()
    for i in range(number_of_tasks):
        def job(idx=i):
            with lock:
                sum_val[0] += idx
        pool.execute(job)
    pool.shutdown()
    while not pool.isTerminated():
        time.sleep(0.01)
    expected = sum(range(number_of_tasks))
    assert sum_val[0] == expected