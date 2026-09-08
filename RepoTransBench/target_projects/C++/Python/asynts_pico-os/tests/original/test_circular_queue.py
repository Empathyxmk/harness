import pytest
from collections import deque

class Tracker:
    create = move = copy = destroy = 0

    @classmethod
    def clear(cls):
        cls.create = cls.move = cls.copy = cls.destroy = 0

    @classmethod
    def assert_counts(cls, create, move, copy, destroy):
        if create is not None:
            assert cls.create == create
        if move is not None:
            assert cls.move == move
        if copy is not None:
            assert cls.copy == copy
        if destroy is not None:
            assert cls.destroy == destroy

    def __init__(self):
        Tracker.create += 1

    def __del__(self):
        Tracker.destroy += 1

def test_circularqueue():
    queue = deque(maxlen=4)
    queue.append(1)
    queue.append(2)
    queue.append(3)
    assert len(queue) == 3
    assert queue.popleft() == 1
    assert queue.popleft() == 2
    assert queue.popleft() == 3
    assert len(queue) == 0

def test_circularqueue_destroy():
    Tracker.clear()
    queue = []
    Tracker.assert_counts(0, 0, 0, 0)
    queue.append(Tracker())
    Tracker.assert_counts(1, None, None, 0)
    queue.append(Tracker())
    Tracker.assert_counts(2, None, None, 0)
    queue.pop()
    Tracker.assert_counts(2, None, None, 1)
    queue = None # Deletion
    Tracker.assert_counts(2, None, None, 2)

def test_circularqueue_wrap():
    queue = deque(maxlen=3)
    queue.append(1)
    queue.append(2)
    queue.append(3)
    queue.popleft()
    queue.append(4)
    assert len(queue) == 3
    assert queue.popleft() == 2
    assert queue.popleft() == 3
    assert queue.popleft() == 4

def test_circularqueue_enqueue_front():
    queue = deque(maxlen=3)
    queue.appendleft(1)
    queue.append(2)
    assert queue.popleft() == 1
    queue.appendleft(3)
    queue.append(4)
    assert len(queue) == 3
    assert queue.popleft() == 3
    assert queue.popleft() == 2
    assert queue.popleft() == 4

def test_circularqueue_enqueue_return_value():
    queue = deque(maxlen=8)
    queue.append(1)
    queue.appendleft(2)
    queue.append(3)
    assert len(queue) == 3
    assert queue[0] == 2
    assert queue[-1] == 3
    assert queue[1] == 1
    # Value assignment
    queue[1] = 4
    assert queue[1] == 4

def test_circularqueue_move():
    Tracker.clear()
    queue1 = [Tracker()]
    Tracker.assert_counts(1, None, None, 0)
    queue2 = queue1 # "move"
    queue1.clear()
    Tracker.assert_counts(1, None, None, 0)
    del queue2
    Tracker.assert_counts(1, None, None, 1)

def test_circularqueue_correct_order_after_move():
    queue1 = deque([1,2], maxlen=4)
    queue2 = deque(queue1)
    assert queue2.popleft() == 1
    assert queue2.popleft() == 2

def test_circularqueue_extensive_use():
    queue = deque(maxlen=16)
    for i in range(16):
        queue.append((i*3)%5)
    for i in range(8):
        queue.popleft()
    for i in range(4):
        queue.append((i*4)%5)
    expected = [4,2,0,3,1,4,2,0,0,4,3,2]
    assert expected[3] == 3
    assert expected[7] == 0
    for value in expected:
        assert queue.popleft() == value
    assert len(queue) == 0