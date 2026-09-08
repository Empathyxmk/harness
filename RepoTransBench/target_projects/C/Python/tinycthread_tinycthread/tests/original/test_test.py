import threading
import time
import random

import pytest

# -----------------------
# Placeholder C-threading API simulated for translation.

# These would wrap the behavior of tinycthread, for now we simulate using Python threading.

class Mutex:
    def __init__(self, recursive=False):
        self._lock = threading.RLock() if recursive else threading.Lock()
    def lock(self):
        self._lock.acquire()
    def unlock(self):
        self._lock.release()
    def trylock(self):
        return self._lock.acquire(blocking=False)
    def destroy(self):
        pass

class CondVar:
    def __init__(self):
        self._cond = threading.Condition()
    def broadcast(self):
        with self._cond:
            self._cond.notify_all()
    def wait(self, mutex):
        # Simulate: unlock mutex, wait, then lock mutex again
        with self._cond:
            mutex.unlock()
            self._cond.wait()
            mutex.lock()

# Thread local simulation
thread_local_var = threading.local()

def thrd_yield():
    time.sleep(0)  # Yield

def thrd_sleep(duration):
    time.sleep(duration)

def thrd_exit(val):
    raise SystemExit(val)

# ---- TESTS ----

def test_thread_arg_and_retval():
    N = 4
    results = [None]*N
    ids = [random.randint(0, 100000) for _ in range(N)]

    def f(idx):
        results[idx] = ids[idx]

    threads = []
    for i in range(N):
        t = threading.Thread(target=f, args=(i,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    for i in range(N):
        assert results[i] == ids[i]

def test_mutex_locking():
    MUTEX_THREADS = 8  # Lower number for speed
    LOCK_ITER = 1000

    counter = [0]
    mtx = Mutex()
    def worker():
        for _ in range(LOCK_ITER):
            mtx.lock()
            cnt = counter[0]
            counter[0] += 1
            mtx.unlock()
    threads = []
    for _ in range(MUTEX_THREADS):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    assert counter[0] == MUTEX_THREADS * LOCK_ITER

def test_mutex_recursive():
    mtx = Mutex(recursive=True)
    depth = [0]
    iters = 10
    def worker():
        for i in range(iters):
            mtx.lock()
            depth[0] += 1
        for i in range(iters):
            depth[0] -= 1
            mtx.unlock()
        assert depth[0] == 0
    t = threading.Thread(target=worker)
    t.start()
    t.join()

def test_condition_variables():
    mtx = Mutex()
    cond = CondVar()
    remain = [5]
    def notifier():
        mtx.lock()
        remain[0] -= 1
        cond.broadcast()
        mtx.unlock()
    def waiter():
        mtx.lock()
        while remain[0] > 0:
            cond.wait(mtx)
        mtx.unlock()
    w = threading.Thread(target=waiter)
    w.start()
    notifiers = []
    for _ in range(5):
        t = threading.Thread(target=notifier)
        t.start()
        notifiers.append(t)
    w.join()
    for t in notifiers:
        t.join()
    assert remain[0] == 0

def test_yield():
    thrd_yield()
    assert True

def test_sleep():
    t0 = time.time()
    thrd_sleep(0.01)
    t1 = time.time()
    assert t1-t0 >= 0.01

def test_once():
    mtx = Mutex()
    count = [0]
    once_lock = threading.Lock()
    once_ran = [False]
    def once_fn():
        mtx.lock()
        count[0] += 1
        mtx.unlock()
    def run_once():
        with once_lock:
            if not once_ran[0]:
                once_fn()
                once_ran[0] = True
    threads = []
    for _ in range(4):
        t = threading.Thread(target=run_once)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    assert count[0] == 1