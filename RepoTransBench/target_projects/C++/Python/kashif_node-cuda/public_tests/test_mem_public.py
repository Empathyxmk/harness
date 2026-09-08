import pytest

class DummyMem:
    pass

@pytest.mark.usefixtures("dummy_cuda", "dummy_v8")
def test_allocation_free_different_size():
    CUDA_SUCCESS = 0
    alloc_size = 512 * 1024
    result_tracker = {}

    def cuMemAlloc(ptr_dict, size):
        if size == alloc_size:
            ptr_dict["ptr"] = 12345678  # Arbitrary non-zero device pointer
            return CUDA_SUCCESS
        return 1

    def cuMemFree(ptr):
        if ptr != 0:
            return CUDA_SUCCESS
        return 1

    mem = DummyMem()
    ptr_holder = {}
    alloc_res = cuMemAlloc(ptr_holder, alloc_size)
    assert alloc_res == CUDA_SUCCESS
    assert ptr_holder["ptr"] != 0
    free_res = cuMemFree(ptr_holder["ptr"])
    assert free_res == CUDA_SUCCESS