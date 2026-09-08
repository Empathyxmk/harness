import pytest

class Arena:
    def __init__(self):
        self.allocations = []
    def alloc(self, T=int):
        val = [None]
        self.allocations.append(val)
        return val

def test_arena_public_single_alloc():
    arena = Arena()
    num = arena.alloc()
    num[0] = 5678
    assert num[0] == 5678

def test_arena_public_multiple():
    arena = Arena()
    nums = []
    for i in range(4):
        slot = arena.alloc()
        slot[0] = i + 10
        nums.append(slot)
    for i in range(4):
        assert nums[i][0] == i + 10