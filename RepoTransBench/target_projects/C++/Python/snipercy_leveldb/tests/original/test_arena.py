def test_arena_empty():
    blocks = []
    assert blocks == []

def test_arena_simple():
    import random
    blocks = []
    N = 100
    bytes_total = 0
    for i in range(N):
        size = random.randint(1, 100)
        blk = bytearray([i % 256] * size)
        blocks.append((size, blk))
        bytes_total += size
        assert len(blk) == size
    # check pattern
    for idx, (size, blk) in enumerate(blocks):
        for b in blk:
            assert b == idx % 256