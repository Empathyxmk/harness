import pytest
from src.d3_queue import queue
import threading

def test_process_tasks_in_series_by_default():
    order = []
    done = threading.Event()
    q = queue.queue()
    def t1(cb):
        threading.Timer(0.01, lambda: (order.append(1), cb(None, 1))).start()
    def t2(cb):
        threading.Timer(0.005, lambda: (order.append(2), cb(None, 2))).start()
    q.defer(t1)
    q.defer(t2)
    def callback(err, results):
        assert err is None
        assert results == [1, 2]
        assert order == [1, 2]
        done.set()
    q.awaitAll(callback)
    done.wait(timeout=1)

def test_handle_multiple_concurrency():
    order = []
    done = threading.Event()
    q = queue.queue(2)
    def t1(cb):
        threading.Timer(0.01, lambda: (order.append(1), cb(None, 1))).start()
    def t2(cb):
        threading.Timer(0.005, lambda: (order.append(2), cb(None, 2))).start()
    q.defer(t1)
    q.defer(t2)
    def callback(err, results):
        assert err is None
        assert sorted(results) == [1, 2]
        done.set()
    q.awaitAll(callback)
    done.wait(timeout=1)

def test_throws_when_defer_after_awaitAll():
    q = queue.queue()
    q.awaitAll(lambda err, results: None)
    with pytest.raises(Exception, match="defer after await"):
        q.defer(lambda cb: None)

def test_throws_when_awaitAll_called_twice():
    q = queue.queue()
    q.defer(lambda cb: cb(None, 1))
    q.awaitAll(lambda err, results: None)
    with pytest.raises(Exception, match="multiple await"):
        q.awaitAll(lambda err, results: None)

def test_propagate_thrown_errors():
    done = threading.Event()
    q = queue.queue()
    def throw_task(cb):
        raise Exception("fail!")
    def callback(err, results=None):
        assert isinstance(err, Exception)
        assert str(err) == "fail!"
        done.set()
    q.defer(throw_task)
    q.awaitAll(callback)
    done.wait(timeout=1)

def test_error_if_defer_is_not_function():
    q = queue.queue()
    with pytest.raises(Exception, match="callback is not a function"):
        q.defer(42)