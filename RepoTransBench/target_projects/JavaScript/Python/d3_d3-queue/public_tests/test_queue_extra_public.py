import pytest
from src.d3_queue import queue
import threading

def test_not_start_above_concurrency_public():
    started = [0]
    done = threading.Event()
    q = queue.queue(2)
    def t1(cb):
        started[0] += 1
        threading.Timer(0.012, lambda: cb(None, 100)).start()
    def t2(cb):
        started[0] += 1
        threading.Timer(0.008, lambda: cb(None, 200)).start()
    def t3(cb):
        started[0] += 1
        threading.Timer(0.005, lambda: cb(None, 300)).start()
    q.defer(t1)
    q.defer(t2)
    q.defer(t3)
    def callback(err, results):
        assert started[0] == 3
        assert err is None
        assert results == [100, 200, 300]
        done.set()
    q.awaitAll(callback)
    done.wait(timeout=1)

def test_propagates_errors_and_aborts_public():
    called = [False]
    done = threading.Event()
    q = queue.queue(2)
    def err_task(cb):
        cb(Exception("public expected"))
    def never_run(cb):
        called[0] = True
        cb(None, 55)
    q.defer(err_task)
    q.defer(never_run)
    def callback(err, results):
        assert isinstance(err, Exception)
        assert str(err) == "public expected"
        assert called[0] is False
        done.set()
    q.awaitAll(callback)
    done.wait(timeout=1)