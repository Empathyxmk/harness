import pytest
from src.d3_queue import queue
import threading

def test_not_start_above_concurrency():
    started = [0]
    done = threading.Event()
    q = queue.queue(1)
    def t1(cb):
        started[0] += 1
        threading.Timer(0.04, lambda: cb(None, 1)).start()
    def t2(cb):
        started[0] += 1
        threading.Timer(0.01, lambda: cb(None, 2)).start()
    q.defer(t1)
    q.defer(t2)
    def callback(err, results):
        assert started[0] == 2
        assert err is None
        assert results == [1, 2]
        done.set()
    q.awaitAll(callback)
    done.wait(timeout=1)

def test_propagates_errors_and_aborts():
    called = [False]
    done = threading.Event()
    q = queue.queue(2)
    def err_task(cb):
        cb(Exception("expected"))
    def never_run(cb):
        called[0] = True
        cb(None, 5)
    q.defer(err_task)
    q.defer(never_run)
    def callback(err, results):
        assert isinstance(err, Exception)
        assert called[0] is False
        done.set()
    q.awaitAll(callback)
    done.wait(timeout=1)