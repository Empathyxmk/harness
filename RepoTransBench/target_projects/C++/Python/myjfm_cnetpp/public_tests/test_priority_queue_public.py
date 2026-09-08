import pytest

import heapq

class PriorityQueue:
    def __init__(self, cap, cmp):
        self.q = []
        self.cap = cap
        self.cmp = cmp

    def Push(self, val):
        heapq.heappush(self.q, val)

    def Pop(self, value_out):
        if not self.q:
            return False
        value_out[0] = heapq.heappop(self.q)
        return True

def test_basic_insert_extract():
    pq = PriorityQueue(10, lambda x, y: x > y)
    pq.Push(9)
    pq.Push(4)
    pq.Push(17)
    value = [None]
    assert pq.Pop(value)
    assert value[0] == 4
    assert pq.Pop(value)
    assert value[0] == 9
    assert pq.Pop(value)
    assert value[0] == 17