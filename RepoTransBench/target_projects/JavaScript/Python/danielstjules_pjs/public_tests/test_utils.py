import pytest

class TestUtilsPublic:
    def test_check_all_elements_in_array_are_positive(self):
        arr = [2, 4, 6, 8]
        result = all(x > 0 for x in arr)
        assert result is True

    def test_find_element_greater_than_specific_value(self):
        arr = [12, 28, 19, 31]
        result = next((x for x in arr if x > 20), None)
        assert result == 28