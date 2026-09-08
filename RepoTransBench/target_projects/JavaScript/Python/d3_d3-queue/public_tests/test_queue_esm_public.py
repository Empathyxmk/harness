import pytest
import threading
from src.d3_queue import queue as queue_mod

def get_queueESM(concurrency=None):
    # Same as above: mimic ESM behavior via Python object
    return queue_mod.queue(concurrency)

def test_queue_accepts_different_concurrency_number():
    done = threading.Event()
    q = get_queueESM(4)
    result = [None] * 4
    def make_task(i):
        def task(cb):
            threading.Timer(0.003 * (i+1), lambda: (result.__setitem__(i, i+1), cb(None, i+1))).start()
        return task
    for i in range(4):
        q.defer(make_task(i))
    def callback(err, results):
        assert err is None
        assert results == [1, 2, 3, 4]
        done.set()
    q.awaitAll(callback)
    done.wait(timeout=1)

def test_queue_defer_should_support_arg_passing():
    done = threading.Event()
    q = get_queueESM()
    def add(a, b, cb):
        threading.Timer(0.002, lambda: cb(None, a * b)).start()
    q.defer(add, 7, 3)
    q.defer(add, 2, 6)
    def callback(err, results):
        assert err is None
        assert results == [21, 12]
        done.set()
    q.awaitAll(callback)
    done.wait(timeout=1)