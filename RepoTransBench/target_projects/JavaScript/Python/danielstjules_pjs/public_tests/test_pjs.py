import pytest

class TestPjsPublic:
    def test_map_values_correctly_with_different_input(self):
        arr = [10, 20, 30]
        result = list(map(lambda x: x * 2, arr))
        assert result == [20, 40, 60]

    def test_filter_even_numbers_with_different_data(self):
        arr = [15, 22, 37, 44]
        result = list(filter(lambda x: x % 2 == 0, arr))
        assert result == [22, 44]

    def test_reduce_array_with_sum_with_different_numbers(self):
        arr = [8, 16, 24]
        from functools import reduce
        result = reduce(lambda acc, x: acc + x, arr, 0)
        assert result == 48