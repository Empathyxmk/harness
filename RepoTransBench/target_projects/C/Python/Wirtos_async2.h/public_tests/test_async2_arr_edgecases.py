import pytest
from src.async2 import AsyncArr, async_arr_push, async_arr_splice, async_arr_destroy

def test_public_async2_arr_edgecases():
    arr = AsyncArr()
    arr.count = 0
    arr.data = []

    # Test pushing then splicing all
    async_arr_push(arr, 100)
    async_arr_push(arr, 200)

    # Edge: remove whole array in one go
    async_arr_splice(arr, 0, 2)
    assert arr.count == 0

    # Edge: try splicing more than count (should not crash or go negative)
    async_arr_push(arr, 44)
    async_arr_splice(arr, 0, 5)
    assert arr.count == 0

    # Edge: try splicing from index greater than count (should not crash)
    async_arr_push(arr, 77)
    async_arr_splice(arr, 5, 1) # out of range
    assert arr.count == 1 and arr.data[0] == 77

    # Test destroy resets to zero
    async_arr_destroy(arr)
    assert arr.count == 0