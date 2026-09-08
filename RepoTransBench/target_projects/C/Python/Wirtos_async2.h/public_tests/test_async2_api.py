import pytest
from src.async2 import AsyncArr, async_arr_push, async_arr_splice, async_arr_destroy

def test_public_async2_api():
    arr = AsyncArr()
    arr.count = 0
    arr.data = []
    # Push different numbers than private (e.g., 5, 16, 25)
    async_arr_push(arr, 5)
    async_arr_push(arr, 16)
    async_arr_push(arr, 25)

    assert arr.count == 3
    assert arr.data[0] == 5
    assert arr.data[1] == 16
    assert arr.data[2] == 25

    # Splice at a different index (remove second element)
    async_arr_splice(arr, 1, 1)
    assert arr.count == 2
    assert arr.data[0] == 5
    assert arr.data[1] == 25

    # Further splice (remove first element)
    async_arr_splice(arr, 0, 1)
    assert arr.count == 1
    assert arr.data[0] == 25

    # Test destroy resets to zero
    async_arr_destroy(arr)
    assert arr.count == 0