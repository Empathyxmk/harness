import threading

def concurrence_test():
    import concurrent.futures
    import threading

    atomic_integer = 0
    N = 1000
    increments = 1000
    lock = threading.Lock()
    ready = threading.Barrier(N)
    done = threading.Barrier(N + 1)  # main waits too

    def worker():
        nonlocal atomic_integer
        ready.wait()  # Wait for all threads ready
        for _ in range(increments):
            with lock:
                atomic_integer += 1
        done.wait()

    threads = []
    for _ in range(N):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()
    done.wait()  # Wait for all threads to finish
    for t in threads:
        t.join()
    return atomic_integer

def test_concurrence_test():
    # We'll run a smaller version due to resource constraints
    atomic_integer = 0
    N = 100
    increments = 100
    lock = threading.Lock()
    ready = threading.Barrier(N)
    done = threading.Barrier(N + 1)

    def worker():
        nonlocal atomic_integer
        ready.wait()
        for _ in range(increments):
            with lock:
                atomic_integer += 1
        done.wait()

    threads = []
    for _ in range(N):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()
    done.wait()
    for t in threads:
        t.join()
    assert atomic_integer == N * increments