import pytest
from src import pool

@pytest.mark.parametrize("element_size, block_size", [
    (8, 1), (16, 2), (32, 4), (64, 8)
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
    N = 100
    ptrs = []
    # Allocate N items
    for _ in range(N):
        ptrs.append(pool.poolMalloc(p))
    assert len(set(id(ptr) for ptr in ptrs)) == N
    # Deallocate all
    for ptr in ptrs:
        pool.poolFree(p, ptr)
    assert len(p.freed) == N
    # Reallocate and verify reuse
    ptrs2 = [pool.poolMalloc(p) for _ in range(N)]
    assert set(id(ptr) for ptr in ptrs) == set(id(ptr) for ptr in ptrs2)