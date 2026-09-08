import pytest

from src.buddy import (
    buddy_new,
    buddy_delete,
    buddy_alloc,
    buddy_free,
    buddy_size,
    buddy_dump
)

# Use a different level and different allocation patterns than the original test
def test_public_flow():
    b = buddy_new(4)

    # Dump initial state
    buddy_dump(b)

    m1 = buddy_alloc(b,5)
    print(f"alloc {m1} (sz= 5)")
    buddy_size_1 = buddy_size(b,m1)
    print(f"size {m1} (sz = {buddy_size_1})")

    m2 = buddy_alloc(b,7)
    print(f"alloc {m2} (sz= 7)")
    buddy_size_2 = buddy_size(b,m2)
    print(f"size {m2} (sz = {buddy_size_2})")

    m3 = buddy_alloc(b,2)
    print(f"alloc {m3} (sz= 2)")
    buddy_size_3 = buddy_size(b,m3)
    print(f"size {m3} (sz = {buddy_size_3})")

    m4 = buddy_alloc(b,8)
    print(f"alloc {m4} (sz= 8)")

    buddy_free(b, m2)
    print(f"free {m2}")
    buddy_free(b, m4)
    print(f"free {m4}")
    buddy_free(b, m1)
    print(f"free {m1}")
    buddy_free(b, m3)
    print(f"free {m3}")

    m5 = buddy_alloc(b,16)
    print(f"alloc {m5} (sz= 16)")
    buddy_free(b, m5)
    print(f"free {m5}")

    m6 = buddy_alloc(b,1)
    print(f"alloc {m6} (sz= 1)")
    buddy_free(b, m6)
    print(f"free {m6}")

    buddy_delete(b)