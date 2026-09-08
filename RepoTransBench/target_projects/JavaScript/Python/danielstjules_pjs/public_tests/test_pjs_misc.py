import pytest

class TestPjsMiscPublic:
    def test_join_array_elements_with_custom_separator(self):
        arr = ['cat', 'dog', 'bird']
        result = ' | '.join(arr)
        assert result == 'cat | dog | bird'

    def test_reverse_array_with_different_values(self):
        arr = [4, 5, 6, 7]
        arr.reverse()
        assert arr == [7, 6, 5, 4]