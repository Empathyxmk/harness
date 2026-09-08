import pytest
import threading
from src.d3_queue import queue as queue_mod

class DummyQueue:
    def __init__(self, concurrency):
        if concurrency < 1:
            raise RuntimeError("invalid concurrency")
        self._size = concurrency

def get_queueESM(concurrency=None):
    # Emulate the ES module default export as in the JS test file
    return queue_mod.queue(concurrency)

def test_throws_if_concurrency_lt_1():
    with pytest.raises(Exception, match="invalid concurrency"):
        get_queueESM(0)
    with pytest.raises(Exception, match="invalid concurrency"):
        get_queueESM(-5)

def test_defaults_concurrency_to_infinity():
    q = get_queueESM()
    assert q._size == float("inf")

def test_throws_if_defer_arg_not_function():
    q = get_queueESM(2)
    with pytest.raises(Exception, match="function"):
        q.defer(123)
    with pytest.raises(Exception, match="function"):
        q.defer(None)

def test_throws_if_await_called_with_nonfunction():
    q = get_queueESM(2)
    with pytest.raises(Exception, match="invalid callback"):
        q.await_(123)

def test_throws_if_awaitAll_called_with_nonfunction():
    q = get_queueESM(2)
    with pytest.raises(Exception, match="invalid callback"):
        q.awaitAll(123)

def test_throws_if_await_called_twice():
    q = get_queueESM(2)
    q.await_(lambda err, a=None, b=None: None)
    with pytest.raises(Exception, match="multiple await"):
        q.await_(lambda err, a=None, b=None: None)

def test_throws_if_defer_after_await_called():
    q = get_queueESM(2)
    q.await_(lambda err, a=None, b=None: None)
    with pytest.raises(Exception, match="defer after await"):
        q.defer(lambda cb: None)

def test_processes_basic_async_callback():
    done = threading.Event()
    q = get_queueESM(2)
    def task(cb):
        threading.Timer(0.003, lambda: cb(None, 5)).start()
    def callback(err, a=None, b=None):
        assert err is None
        assert a == 5
        done.set()
    q.defer(task)
    q.await_(callback)
    done.wait(timeout=1)

def test_handles_queue_abort():
    done = threading.Event()
    q = get_queueESM(1)
    def task(cb):
        threading.Timer(0.005, lambda: cb(None, 7)).start()
    def callback(err, res=None):
        assert isinstance(err, Exception)
        assert str(err) == "abort"
        done.set()
    q.defer(task)
    q.await_(callback)
    q.abort()
    done.wait(timeout=1)