import pytest

class OARFrame:
    def __init__(self, dummy):
        self.dummy = dummy

class OARFrameQueue:
    def __init__(self, maxsize):
        if maxsize <= 0:
            raise ValueError("Maxsize must be positive")
        self.maxsize = maxsize
        self.queue = []
    
    def put(self, frame):
        if frame is None:
            return -1
        if len(self.queue) >= self.maxsize:
            return -2
        self.queue.append(frame)
        return 0
    def get(self):
        if len(self.queue) == 0:
            return None
        return self.queue.pop(0)

def oar_frame_queue_create(size):
    if size <= 0:
        return None
    return OARFrameQueue(size)

def oar_frame_queue_free(queue):
    # In C, would free memory, in Python no-op or clear for test
    pass

def oar_frame_queue_put(queue, frame):
    if queue is None or frame is None:
        return -1
    return queue.put(frame)

def oar_frame_queue_get(queue):
    if queue is None:
        return None
    return queue.get()


def test_create_and_free_null_and_valid():
    assert oar_frame_queue_create(0) is None
    oar_frame_queue_free(None)

    queue = oar_frame_queue_create(3)
    assert queue is not None
    oar_frame_queue_free(queue)

def test_put_get_normal_and_edge():
    queue = oar_frame_queue_create(2)
    assert queue is not None

    f1 = OARFrame(1)
    f2 = OARFrame(2)
    f3 = OARFrame(3)

    # Get from empty
    assert oar_frame_queue_get(queue) is None

    # Put frame 1
    assert oar_frame_queue_put(queue, f1) == 0
    # Put frame 2
    assert oar_frame_queue_put(queue, f2) == 0
    # Overfill: Put frame 3
    assert oar_frame_queue_put(queue, f3) == -2

    # NULL input tests
    assert oar_frame_queue_put(None, f3) == -1
    assert oar_frame_queue_put(queue, None) == -1
    assert oar_frame_queue_get(None) is None

    # Get frame 1
    got1 = oar_frame_queue_get(queue)
    assert got1 is not None
    assert got1.dummy == 1

    # Get frame 2
    got2 = oar_frame_queue_get(queue)
    assert got2 is not None
    assert got2.dummy == 2

    # get from empty
    assert oar_frame_queue_get(queue) is None

    oar_frame_queue_free(queue)