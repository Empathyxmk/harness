# Test translated from test03_public.cpp

def square(x: int) -> int:
    return x * x

def sum_array(arr, size):
    total = 0
    for i in range(size):
        total += arr[i]
    return total

def test_square():
    # Python has no static_assert, but we use assert for test equivalent
    assert square(3) == 9, "square(3) != 9"
    assert square(-5) == 25, "square(-5) != 25"
    assert square(7) == 49
    assert square(0) == 0

def test_sum_array():
    arr1 = [10, 20, 30]
    arr2 = [-7, 0, 7, 14]
    assert sum_array(arr1, 3) == 60, "sum_array(arr1) != 60"
    assert sum_array(arr2, 4) == 14, "sum_array(arr2) != 14"
    assert sum_array(arr1, 3) == 60
    assert sum_array(arr2, 4) == 14