import pytest

class TestPjsReducePublic:
    def test_multiply_array_elements_via_reduce(self):
        arr = [2, 3, 4]
        from functools import reduce
        result = reduce(lambda acc, x: acc * x, arr, 1)
        assert result == 24

    def test_find_minimum_of_array(self):
        arr = [11, 3, 7, 2]
        result = min(arr)
        assert result == 2