class StaticQueue:
    def __init__(self, max_items):
        self._queue = []
        self.max_items = max_items
    def enqueue(self, val):
        if len(self._queue) < self.max_items:
            self._queue.append(val)
            return True
        return False
    def dequeue(self, val_container):
        if not self._queue:
            return False
        val_container[0] = self._queue.pop(0)
        return True

def test_public_push_pop_different_data():
    queue = StaticQueue(4)
    val = [0]

    assert queue.enqueue(99)
    assert queue.enqueue(18)
    assert queue.enqueue(-33)
    assert queue.enqueue(0)
    assert not queue.enqueue(2019)

    assert queue.dequeue(val) and val[0] == 99
    assert queue.dequeue(val) and val[0] == 18
    assert queue.dequeue(val) and val[0] == -33
    assert queue.dequeue(val) and val[0] == 0
    assert not queue.dequeue(val)