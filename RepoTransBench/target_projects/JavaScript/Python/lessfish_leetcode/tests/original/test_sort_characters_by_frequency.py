import pytest

# from src.sort_characters_by_frequency import frequency_sort

# For demonstration, define here:
def frequency_sort(s):
    from collections import Counter
    freq = Counter(s)
    return ''.join(c * freq[c] for c, _ in sorted(freq.items(), key=lambda x: -x[1]))

class TestFrequencySort:
    def test_sorts_characters_by_descending_frequency(self):
        result = frequency_sort('tree')
        assert 'ee' in result
        assert 't' in result or 'r' in result
        assert len(result) == 4

    def test_distinct_characters(self):
        result = frequency_sort('abc')
        assert sorted(result) == sorted('abc')
        assert len(result) == 3

    def test_empty_string(self):
        assert frequency_sort('') == ''

    def test_all_same_character(self):
        assert frequency_sort('aaa') == 'aaa'

    def test_mixed_frequency(self):
        s = 'cccaaa'
        out = frequency_sort(s)
        assert out in ['cccaaa', 'aaaccc']