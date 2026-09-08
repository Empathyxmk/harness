import pytest

def custom_sum_array(arr): # Python lists already inherently provide length, so no 'len' arg needed for sum()
    return sum(arr)

def test_custom_full_sum_array_public():
    print("Running public test_custom_full_public.c ...")
    arr1 = [3, 6, 9]
    arr2 = [-2, 4, 10, 0]
    assert custom_sum_array(arr1) == 18, f"Expected 18, got {custom_sum_array(arr1)}"
    assert custom_sum_array(arr2) == 12, f"Expected 12, got {custom_sum_array(arr2)}"
    print("test_custom_full_public passed!")