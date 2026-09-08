import pytest

class Queue:
    def __init__(self):
        self.lst = []

    def empty(self):
        return len(self.lst) == 0

    def enqueue(self, val):
        self.lst.append(val)

    def dequeue(self):
        return self.lst.pop(0)

def test_empty():
    q = Queue()
    assert q.empty()

def test_all():
    q = Queue()
    q.enqueue(100)
    assert not q.empty()
    assert q.dequeue() == 100
    q.enqueue(200)
    q.enqueue(300)
    q.enqueue(400)
    assert q.dequeue() == 200
    assert q.dequeue() == 300
    assert q.dequeue() == 400
    assert q.empty()