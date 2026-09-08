import pytest

class LFQueue:
    """A simple FIFO queue to simulate the C/C++ lfqueue for integer pointers."""
    def __init__(self):
        self._data = []

    def init(self):
        self._data = []
        return 0

    def destroy(self):
        self._data = []

    def size(self):
        return len(self._data)

    def enq(self, item):
        self._data.append(item)
        return 0

    def deq(self):
        if self._data:
            return self._data.pop(0)
        else:
            return None

def test_basic_enqueue_dequeue():
    q = LFQueue()
    assert q.init() == 0

    value1 = 5
    assert q.enq(value1) == 0
    assert q.size() == 1

    p = q.deq()
    assert p == 5
    assert q.size() == 0

    assert q.deq() is None
    q.destroy()

def test_multiple_enqueue_dequeue():
    q = LFQueue()
    assert q.init() == 0

    v1, v2, v3 = 1, 2, 3
    q.enq(v1)
    q.enq(v2)
    q.enq(v3)

    p = q.deq()
    assert p == 1
    p = q.deq()
    assert p == 2
    p = q.deq()
    assert p == 3

    assert q.size() == 0
    q.destroy()