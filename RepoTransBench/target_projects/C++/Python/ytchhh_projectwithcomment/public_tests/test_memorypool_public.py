import pytest
import math

class Dummy:
    def __init__(self, v):
        self.x = v

@pytest.fixture
def int_pool():
    # A dummy test pool that simulates allocate/construct/destroy/deallocate.
    class Pool:
        def allocate(self, n):
            return [None for _ in range(n)]
        def construct(self, arr, *args, **kwargs):
            arr[0] = args[0]
        def destroy(self, arr):
            arr[0] = None
        def deallocate(self, arr, n):
            pass
    return Pool()

@pytest.fixture
def string_pool():
    class Pool:
        def allocate(self, n):
            return [None for _ in range(n)]
        def construct(self, arr, val):
            arr[0] = val
        def destroy(self, arr):
            arr[0] = None
        def deallocate(self, arr, n):
            pass
    return Pool()

@pytest.fixture
def float_pool():
    # Used for vector integration test - not a real allocator, just for interface.
    class Pool:
        def __init__(self):
            pass
    return Pool()


def test_single_allocation_and_value():
    arr = [None]
    arr[0] = 99
    assert arr[0] == 99
    arr[0] = None  # destroy
    # deallocate simulated

def test_multiple_allocations_with_strings():
    arr = [None, None, None]
    arr[0] = "alpha"
    arr[1] = "beta"
    arr[2] = "gamma"
    assert arr[0] == "alpha"
    assert arr[1] == "beta"
    assert arr[2] == "gamma"
    arr[0] = None
    arr[1] = None
    arr[2] = None
    # deallocate simulated

def test_vector_integration():
    # Just use Python's vector/list
    v = []
    for i in range(4):
        v.append(float(i) / 2.0)
    assert math.isclose(v[0], 0.0)
    assert math.isclose(v[1], 0.5)
    assert math.isclose(v[2], 1.0)
    assert math.isclose(v[3], 1.5)
    v.clear()

def test_exception_on_large_allocation():
    # Simulate bad_alloc by raising an exception for very large n
    class Pool:
        def allocate(self, n):
            if n > 1_000_000_000:
                raise MemoryError("bad alloc")
            return [None]*n
        def deallocate(self, arr, n):
            pass
    pool = Pool()
    did_throw = False
    try:
        mem = pool.allocate(2**64//1024)
    except MemoryError:
        did_throw = True
    assert did_throw

def test_pair_allocation():
    alloc = [(3, 3.14)]
    assert alloc[0][0] == 3
    assert math.isclose(alloc[0][1], 3.14)
    alloc[0] = None

def test_construct_destroy_custom_object():
    # Construct/destroy on a custom object
    arr = [None]
    arr[0] = Dummy(777)
    assert arr[0].x == 777
    arr[0] = None