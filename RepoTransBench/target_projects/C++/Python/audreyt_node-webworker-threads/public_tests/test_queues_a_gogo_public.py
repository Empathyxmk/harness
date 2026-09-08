import pytest
from src.sim.simple_queue import SimpleQueue

def test_queues_a_gogo_public():
    q = SimpleQueue()
    # Public test: different data than original
    q.push(42)
    q.push(-7)
    q.push(0)

    assert q.pop() == 42
    assert q.pop() == -7
    assert not q.empty()
    assert q.pop() == 0
    assert q.empty()
    assert q.pop() == -1

    q.push(99)
    assert not q.empty()
    assert q.pop() == 99
    assert q.empty()