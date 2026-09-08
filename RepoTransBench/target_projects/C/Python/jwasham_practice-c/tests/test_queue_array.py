import pytest

class Queue:
    # Simple array-based queue, limited size 5 for full test
    def __init__(self):
        self.capacity = 5
        self.arr = [None]*self.capacity
        self.front = 0
        self.rear = 0
        self.size = 0

    def empty(self):
        return self.size == 0

    def full(self):
        return self.size == self.capacity

    def enqueue(self, val):
        if self.full():
            raise Exception("Queue full")
        self.arr[self.rear] = val
        self.rear = (self.rear + 1) % self.capacity
        self.size += 1

    def dequeue(self):
        if self.empty():
            raise Exception("Queue empty")
        val = self.arr[self.front]
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return val

def test_empty():
    q = Queue()
    assert q.empty()
    q.enqueue(43)
    assert not q.empty()

def test_enqueue():
    q = Queue()
    q.enqueue(100)
    q.enqueue(200)
    q.enqueue(300)
    q.enqueue(400)
    q.enqueue(500)
    assert q.full()

def test_dequeue():
    q = Queue()
    assert q.empty()
    q.enqueue(100)
    assert not q.empty()
    assert q.dequeue() == 100
    assert q.empty()

def test_rotation():
    q = Queue()
    q.enqueue(100)
    q.enqueue(200)
    assert q.dequeue() == 100
    q.enqueue(300)
    q.enqueue(400)
    assert q.dequeue() == 200
    q.enqueue(500)
    q.enqueue(600)
    q.enqueue(700)
    assert q.full()