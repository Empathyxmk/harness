import pytest
import threading

class ThreadPool:
    def __init__(self, num_threads, unused):
        self.num_threads = num_threads
        self.queue = []
        self.threads = []

    def Start(self):
        for _ in range(self.num_threads):
            t = threading.Thread(target=self._worker)
            t.daemon = True
            self.threads.append(t)
            t.start()

    def AddTask(self, func):
        self.queue.append(func)

    def Stop(self):
        while self.queue:
            func = self.queue.pop(0)
            func()
        for t in self.threads:
            t.join(timeout=0.1)

    def _worker(self):
        while self.queue:
            func = self.queue.pop(0)
            func()

def test_simple_task():
    pool = ThreadPool(3, 1)
    from multiprocessing import Value
    import ctypes
    counter = [0]
    def add_10():
        counter[0] += 10
    pool.Start()
    pool.AddTask(add_10)
    pool.Stop()
    assert counter[0] >= 10