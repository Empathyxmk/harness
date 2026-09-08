import pytest
from src.async2 import (
    AsyncArr, async_arr_init, async_arr_push, async_arr_splice, async_arr_destroy
)

def test_async_arr_splice_negative_count():
    arr = AsyncArr()
    async_arr_init(arr)
    # Fill some data
    for i in range(5):
        assert async_arr_push(arr, i) == 1
    # Use splice with maximum len, should not underflow
    async_arr_splice(arr, 0, 100)
    assert arr.count == 0

    # force count, then splice
    arr.count = 2
    arr.data = [10, 11]
    async_arr_splice(arr, 1, 2)  # only one left, should just remove that one
    assert arr.count == 1
    assert arr.data[0] == 10

    arr.count = 0
    arr.data = []
    async_arr_splice(arr, 0, 1) # nothing to remove, should stay at zero
    assert arr.count == 0

def test_async_arr_destroy_resets_count():
    arr = AsyncArr()
    arr.count = 5
    arr.data = [1]*5
    async_arr_destroy(arr)
    assert arr.count == 0
    # Destroying again is safe
    async_arr_destroy(arr)
    assert arr.count == 0