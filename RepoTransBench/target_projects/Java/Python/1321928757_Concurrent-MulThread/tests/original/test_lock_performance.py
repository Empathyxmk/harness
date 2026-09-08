import threading

def run_lock_performance(reentrant=True):
    lock = threading.Lock() if reentrant else threading.RLock()
    shared_resource = [0]
    READ_THREADS = 10
    WRITE_THREADS = 2
    ITERATIONS = 10000

    def read_fn():
        for _ in range(ITERATIONS):
            with lock:
                _ = shared_resource[0]

    def write_fn():
        for _ in range(ITERATIONS):
            with lock:
                shared_resource[0] += 1

    threads = []
    for _ in range(READ_THREADS):
        threads.append(threading.Thread(target=read_fn))
    for _ in range(WRITE_THREADS):
        threads.append(threading.Thread(target=write_fn))

    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return shared_resource[0]

def test_lock_performance():
    final_count = run_lock_performance(True)
    # With 2 write threads and 10,000 iterations, total increment should be 2*10,000
    assert final_count == 2 * 10000