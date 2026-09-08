import threading
import time
import pytest
from src.threadpool.safequeue import SafeQueue

def test_empty_at_start():
    sq = SafeQueue()
    assert sq.empty()
    assert sq.size() == 0

def test_enqueue_changes_state():
    sq = SafeQueue()
    x = 123.456
    sq.enqueue(x)
    assert not sq.empty()
    assert sq.size() == 1

def test_enqueue_dequeue_value():
    sq = SafeQueue()
    msg = "test_public"
    sq.enqueue(msg)
    ok, out = sq.dequeue()
    assert ok
    assert out == "test_public"
    assert sq.empty()

def test_dequeue_when_empty_returns_false():
    sq = SafeQueue()
    ok, y = sq.dequeue()
    assert not ok

def test_threaded_enqueue_dequeue_public():
    sq = SafeQueue()

    def producer():
        for i in range(100, 200):
            sq.enqueue(i)

    sum_val = {"sum": 0}
    def consumer():
        for i in range(100, 200):
            while True:
                ok, val = sq.dequeue()
                if ok:
                    sum_val["sum"] += val
                    break
                time.sleep(0)

    t1 = threading.Thread(target=producer)
    t2 = threading.Thread(target=consumer)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    # Sum of integers from 100 to 199
    assert sum_val["sum"] == (199 * 200 // 2) - (99 * 100 // 2)