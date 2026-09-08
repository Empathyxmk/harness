import pytest

class LFQueue:
    """A simple FIFO queue to simulate the C lfqueue for integer pointers."""
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

    def single_deq(self):
        # In our simple single-threaded Python implementation, it's the same as deq
        return self.deq()


def test_lfqueue_c_main_logic():
    q = LFQueue()
    assert q.init() == 0

    x = 123
    y = 321
    assert q.size() == 0
    assert q.enq(x) == 0
    assert q.enq(y) == 0
    assert q.size() == 2

    out = q.deq()
    assert out == 123
    out = q.single_deq()
    assert out == 321

    assert q.deq() is None
    assert q.single_deq() is None

    q.destroy()