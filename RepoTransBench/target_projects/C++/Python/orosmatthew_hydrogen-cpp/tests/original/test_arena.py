import pytest

# Mock Arena for testing, mimicking C++ arena allocation by list-of-objects.
class Arena:
    def __init__(self):
        self.allocations = []
    def alloc(self, T=int):
        val = [None]
        self.allocations.append(val)
        return val

def test_arena_allocation_simple():
    arena = Arena()
    num = arena.alloc()
    num[0] = 1234
    assert num[0] == 1234

def test_arena_vector_allocation():
    arena = Arena()
    nums = []
    for i in range(5):
        slot = arena.alloc()
        slot[0] = i
        nums.append(slot)
    for i in range(5):
        assert nums[i][0] == i