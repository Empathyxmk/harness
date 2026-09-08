import threading
import time
from src.d3_queue.queue import queue

def test_defer_and_await_with_abort():
    q = queue(1)
    results = []

    def task1(callback):
        t = threading.Timer(0.01, lambda: callback(None, 1))
        t.start()

    def task2(callback):
        t = threading.Timer(0.02, lambda: callback(None, 2))
        t.start()

    q.defer(task1)
    q.defer(task2)

    done = threading.Event()

    def await_callback(error, r1, r2):
        results.append((error, r1, r2))
        done.set()

    q.await_(await_callback)
    q.abort()

    # Wait for all to finish or abort
    done.wait(0.1)
    assert results[0][0] is not None  # error should not be None

def test_await_all_with_abort():
    q = queue(2)
    results = []

    def task(i, callback):
        t = threading.Timer(0.005 * i, lambda: callback(None, i))
        t.start()

    for i in range(5):
        q.defer(task, i)

    done = threading.Event()

    def await_all_callback(error, results_all):
        results.append((error, results_all))
        done.set()

    q.await_all(await_all_callback)
    q.abort()

    done.wait(0.1)
    assert results[0][0] is not None  # error should not be None

def test_aborted_task_is_not_called():
    q = queue(1)
    called = [False]

    def task(callback):
        called[0] = True
        callback()

    q.defer(task)
    q.abort()
    # Small delay to ensure that the task does not get called after abort
    time.sleep(0.02)
    assert not called[0]

def test_no_callback_called_after_abort():
    q = queue(1)
    called = [False]
    done = threading.Event()

    def task(callback):
        time.sleep(0.01)  # enough time for abort to be called before this runs
        callback(None, 42)

    def callback(error, result=None):
        called[0] = True
        done.set()

    q.defer(task)
    q.await_(callback)
    q.abort()

    # Wait for a short duration to ensure callback is not called
    def check_and_set():
        assert not called[0], "Callback was called after abort"
        done.set()
    t = threading.Timer(0.03, check_and_set)
    t.start()
    done.wait(0.05)