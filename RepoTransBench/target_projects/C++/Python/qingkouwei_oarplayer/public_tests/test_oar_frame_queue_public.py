import pytest

class OarFrameQueue:
    # For test, store pointers as actual objects for enqueue/dequeue
    def __init__(self, size):
        if size <= 0:
            raise ValueError("size must be positive")
        self._size = size
        self._queue = []
    def enqueue(self, item):
        if item is None:
            return -1
        if len(self._queue) >= self._size:
            return -1
        self._queue.append(item)
        return 0
    def dequeue(self, out_ref):
        if len(self._queue) == 0:
            return -1
        item = self._queue.pop(0)
        if out_ref is not None:
            out_ref[0] = item
        return 0
    def destroy(self):
        pass

def oar_frame_queue_create(size):
    if size <= 0:
        return None
    return OarFrameQueue(size)

def oar_frame_queue_destroy(queue):
    # No-op for Python mock
    if queue is not None:
        queue.destroy()

def oar_frame_queue_enqueue(queue, item):
    if queue is None or item is None:
        return -1
    return queue.enqueue(item)
def oar_frame_queue_dequeue(queue, out_ref):
    if queue is None or out_ref is None:
        return -1
    return queue.dequeue(out_ref)

def test_public_create_and_destroy():
    queue = oar_frame_queue_create(16)
    assert queue is not None
    oar_frame_queue_destroy(queue)

def test_public_enqueue_dequeue():
    queue = oar_frame_queue_create(8)
    assert queue is not None
    test_data = [42,43,44,45,46,47,48,49]
    for i in range(8):
        ret = oar_frame_queue_enqueue(queue, test_data[i])
        assert ret == 0
    for i in range(8):
        out = [None]
        ret = oar_frame_queue_dequeue(queue, out)
        assert ret == 0
        assert out[0] == 42+i
    oar_frame_queue_destroy(queue)

def test_public_queue_full_test():
    queue = oar_frame_queue_create(2)
    assert queue is not None
    a, b, c = 99, 100, 101
    assert oar_frame_queue_enqueue(queue, a) == 0
    assert oar_frame_queue_enqueue(queue, b) == 0
    assert oar_frame_queue_enqueue(queue, c) == -1
    oar_frame_queue_destroy(queue)