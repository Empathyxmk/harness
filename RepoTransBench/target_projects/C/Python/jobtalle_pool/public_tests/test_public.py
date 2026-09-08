import pytest
from src import pool

@pytest.mark.parametrize("element_size, block_size", [
    (8, 2), (16, 4), (32, 8)
])
def test_pool(element_size, block_size):
    p = pool.Pool()
    p.element_size = element_size
    p.block_size = block_size
    p.blocks_used = 0
    p.blocks = []
    p.block = -1
    p.used = 0
    p.freed = []
    N = 20
    ptrs = []
    for _ in range(N):
        ptrs.append(pool.poolMalloc(p))
    # All returned objects should be unique
    assert len(set(id(ptr) for ptr in ptrs)) == N
    for ptr in ptrs:
        pool.poolFree(p, ptr)
    assert len(p.freed) == N
    # Reallocate and verify old objects reused
    ptrs2 = [pool.poolMalloc(p) for _ in range(N)]
    assert set(id(ptr) for ptr in ptrs) == set(id(ptr) for ptr in ptrs2)