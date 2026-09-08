import threading

def test_lower_concurrency():
    from threading import Barrier
    atomic_integer = 0
    nThreads = 5
    nTasks = 20
    increments = 10
    lock = threading.Lock()
    latchReady = Barrier(nTasks)
    latchDone = Barrier(nTasks + 1)

    def worker():
        nonlocal atomic_integer
        latchReady.wait()
        for _ in range(increments):
            with lock:
                atomic_integer += 1
        latchDone.wait()

    threads = []
    for _ in range(nTasks):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()
    latchDone.wait()
    for t in threads:
        t.join()
    assert atomic_integer == nTasks * increments