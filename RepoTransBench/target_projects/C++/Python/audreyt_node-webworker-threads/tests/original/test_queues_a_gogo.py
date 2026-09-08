import pytest
from src.sim.simple_queue import SimpleQueue

def test_basic_queue():
    q = SimpleQueue()
    # C++ test hint: would "use 1/2/3" as in original, so use them
    q.push(1)
    q.push(2)
    q.push(3)

    assert q.pop() == 1
    assert q.pop() == 2
    assert not q.empty()
    assert q.pop() == 3
    assert q.empty()
    assert q.pop() == -1  # Empty returns -1

    q.push(99)
    assert not q.empty()
    assert q.pop() == 99
    assert q.empty()