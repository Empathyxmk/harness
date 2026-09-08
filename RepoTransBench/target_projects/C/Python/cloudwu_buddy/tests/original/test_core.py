import pytest

from src.buddy import (
    buddy_new,
    buddy_delete,
    buddy_alloc,
    buddy_free,
    buddy_size,
    buddy_dump
)

# Main functional tests derived from test.c.

def test_main_flow():
    b = buddy_new(5)
    buddy_dump(b)
    m1 = buddy_alloc(b,4)
    buddy_size_1 = buddy_size(b,m1)
    print(f"alloc {m1} (sz= 4)\nsize {m1} (sz = {buddy_size_1})")
    m2 = buddy_alloc(b,9)
    buddy_size_2 = buddy_size(b,m2)
    print(f"alloc {m2} (sz= 9)\nsize {m2} (sz = {buddy_size_2})")
    m3 = buddy_alloc(b,3)
    buddy_size_3 = buddy_size(b,m3)
    print(f"alloc {m3} (sz= 3)\nsize {m3} (sz = {buddy_size_3})")
    m4 = buddy_alloc(b,7)
    # Freeing in different order
    buddy_free(b,m3)
    buddy_free(b,m1)
    buddy_free(b,m4)
    buddy_free(b,m2)
    m5 = buddy_alloc(b,32)
    buddy_free(b,m5)
    m6 = buddy_alloc(b,0)
    buddy_free(b,m6)
    buddy_delete(b)