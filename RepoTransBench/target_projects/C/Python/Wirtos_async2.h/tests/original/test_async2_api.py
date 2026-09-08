import pytest
from src.async2 import (
    AsyncArr, async_new, async_resume, async_free,
    async_arr_init, async_arr_push, async_arr_pop, async_arr_splice, async_arr_destroy
)

def test_async_memory():
    state = async_new()
    assert state is not None
    async_resume(state)
    async_resume(state)
    async_free(state)

def test_async_nullptrs():
    # Test NULL pointer handling for all public API
    async_free(None)
    async_resume(None)

    arr = None
    async_arr_init(arr) # should do nothing
    assert async_arr_push(arr, 1) == 0
    assert async_arr_pop(arr) == -1
    async_arr_splice(arr, 0, 1) # should do nothing
    async_arr_destroy(arr) # should do nothing

def test_async_arr():
    arr = AsyncArr()
    async_arr_init(arr)
    x = 42
    assert async_arr_push(arr, x) == 1
    assert async_arr_push(arr, x + 1) == 1
    assert async_arr_push(arr, x + 2) == 1

    for i in range(arr.count, 10):
        assert async_arr_push(arr, i)

    # Buffer full now
    assert async_arr_push(arr, 100) == 0

    top = async_arr_pop(arr)
    assert top >= 0

    # Test splice normal case
    async_arr_splice(arr, 0, 1)

    # Test splice edge cases (negative, past end, zero)
    async_arr_splice(arr, -1, 2)  # should do nothing
    async_arr_splice(arr, arr.count, 1) # should do nothing
    async_arr_splice(arr, 0, 0) # should do nothing
    async_arr_splice(arr, 0, 100) # trim to count

    async_arr_destroy(arr)

def test_async_pop_empty():
    arr = AsyncArr()
    async_arr_init(arr)
    assert async_arr_pop(arr) == -1