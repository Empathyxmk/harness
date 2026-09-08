from src import pool

def test_poolMalloc_without_blocks():
    p = pool.Pool()
    p.element_size = 8
    p.block_size = 1
    p.blocks_used = 0
    p.blocks = []       # Fix: Start with an empty list, not [None]
    p.block = -1
    p.used = 0
    p.freed = []
    # Simulate calling poolMalloc when block needs to be incremented
    ptr = pool.poolMalloc(p)
    assert ptr is not None
    assert p.blocks_used == 1     # Make sure a block was added
    assert len(p.blocks) == 1
    assert p.used == 0
    assert p.block == 0