import pytest
from src import pool

SUCCESS = 0
FAILURE = -1

class Point:
    def __init__(self):
        self.x = 0
        self.y = 0

def fill_point(p: Point, offset: int):
    p.x = 1000 + offset
    p.y = 2000 + offset

def test_public_ext_pool():
    pool_ptr = pool.Pool()
    element_size = 8 # For the mock: size is not actually used apart from structure
    block_size = 6

    pool.poolInitialize(pool_ptr, element_size, block_size)

    objects = []
    for offset in (10, 20, 30):
        pt = Point()
        fill_point(pt, offset)
        objects.append(pt)
    # allocate from pool for correspondence of pointers
    slots = [pool.poolMalloc(pool_ptr) for _ in range(3)]

    # simulate that the slots point to objects
    idx_map = {}
    for slot, obj in zip(slots, objects):
        idx_map[slot] = obj

    assert idx_map[slots[0]].x == 1010 and idx_map[slots[0]].y == 2010
    assert idx_map[slots[1]].x == 1020 and idx_map[slots[1]].y == 2020
    assert idx_map[slots[2]].x == 1030 and idx_map[slots[2]].y == 2030

    # Free one element, allocate again, should recycle:
    pool.poolFree(pool_ptr, slots[1]) # Free the 'p2' slot
    slot4 = pool.poolMalloc(pool_ptr)
    p4 = Point()
    fill_point(p4, 40)
    # Should be same slot identity as slots[1] due to LIFO in mock
    assert slot4 == slots[1]
    idx_map[slot4] = p4
    assert idx_map[slot4].x == 1040 and idx_map[slot4].y == 2040

    pool.poolFreePool(pool_ptr)