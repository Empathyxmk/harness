import threading
import time
import pytest
from src.threadpool.safequeue import SafeQueue

def test_empty_initially():
    sq = SafeQueue()
    assert sq.empty()
    assert sq.size() == 0

def test_enqueue_and_not_empty():
    sq = SafeQueue()
    x = 42
    sq.enqueue(x)
    assert not sq.empty()
    assert sq.size() == 1

def test_enqueue_dequeue_single():
    sq = SafeQueue()
    x = 7
    sq.enqueue(x)
    ok, y = sq.dequeue()
    assert ok
    assert y == 7
    assert sq.empty()

def test_dequeue_from_empty():
    sq = SafeQueue()
    ok, x = sq.dequeue()
    assert not ok

def test_threaded_enqueue_dequeue():
    sq = SafeQueue()
    def producer():
        for i in range(100):
            sq.enqueue(i)
    def consumer():
        success_count = 0
        tries = 0
        while success_count < 100 and tries < 200:
            ok, out = sq.dequeue()
            if ok:
                success_count += 1
            tries += 1
            time.sleep(0)
        assert success_count == 100
    t1 = threading.Thread(target=producer)
    t2 = threading.Thread(target=consumer)
    t1.start()
    t2.start()
    t1.join()
    t2.join()