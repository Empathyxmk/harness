import threading

class DummyThreadPool:
    def __init__(self, max_workers):
        self.max_workers = max_workers
        self.tasks = []
        self.threads = []
        self.shutdown_called = False

    def execute(self, fn):
        thread = threading.Thread(target=fn)
        self.threads.append(thread)
        thread.start()

    def shutdown(self):
        self.shutdown_called = True
        for t in self.threads:
            t.join()

def test_threadpool_execution_and_shutdown():
    pool = DummyThreadPool(max_workers=5)
    results = []

    def task(i):
        results.append(i)

    for i in range(10):
        pool.execute(lambda i=i: task(i))
    pool.shutdown()

    assert pool.shutdown_called
    assert sorted(results) == list(range(10))