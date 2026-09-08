import math

def is_sorted(numbers):
    last_num = -math.inf
    for num in numbers:
        if num < last_num:
            return False
        last_num = num
    return True

def print_ints(numbers):
    print(', '.join(str(x) for x in numbers))

def contain_same_ints(arr1, arr2):
    arr1_sorted = sorted(arr1)
    arr2_sorted = sorted(arr2)
    return arr1_sorted == arr2_sorted

def test_helpers():
    assert is_sorted([1, 2, 3, 4, 100])
    assert not is_sorted([5,4,3,2])
    assert contain_same_ints([1,2,3], [3,2,1])
    assert not contain_same_ints([1,2,3], [1,2,2,3])