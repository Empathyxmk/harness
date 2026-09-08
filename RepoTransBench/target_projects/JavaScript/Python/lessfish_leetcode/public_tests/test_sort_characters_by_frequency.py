import pytest
from collections import Counter

# from src.sort_characters_by_frequency import frequency_sort

def frequency_sort(s):
    freq = Counter(s)
    # Sort characters by frequency, descending; order among equals for test is flexible
    items = sorted(freq.items(), key=lambda x: -x[1])
    return ''.join(c * freq[c] for c, _ in items)

def string_has_frequencies(res, freq_obj):
    actual_freq = {}
    for ch in res:
        actual_freq[ch] = actual_freq.get(ch, 0) + 1
    for k in freq_obj:
        if actual_freq.get(k, 0) != freq_obj[k]:
            return False
    for k in actual_freq:
        if actual_freq[k] != freq_obj.get(k, 0):
            return False
    return True

class TestFrequencySortPublic:
    def test_example_s_eefffggh(self):
        res = frequency_sort("eefffggh")
        assert len(res) == 8
        assert string_has_frequencies(res, {'e': 2, 'f': 3, 'g': 2, 'h': 1})
        assert res[0] == 'f'

    def test_ties_in_character_multiple_2s(self):
        s = "ppqqrr"
        res = frequency_sort(s)
        assert len(res) == 6
        assert string_has_frequencies(res, {'p':2, 'q':2, 'r':2})
        assert res[0] in ['p', 'q', 'r']

    def test_s_xyzxyzx(self):
        res = frequency_sort("xyzxyzx")
        assert len(res) == 7
        assert string_has_frequencies(res, {'x':3, 'y':2, 'z':2})
        assert res[0] == 'x'

    def test_all_unique(self):
        res = frequency_sort("klmnop")
        assert len(res) == 6
        assert string_has_frequencies(res, {'k':1,'l':1,'m':1,'n':1,'o':1,'p':1})

    def test_one_char(self):
        assert frequency_sort("z") == "z"

    def test_mixed_case(self):
        # "CCDddcceeE": C:2, D:1, d:2, c:2, e:2, E:1
        res = frequency_sort("CCDddcceeE")
        assert len(res) == 10
        assert string_has_frequencies(res, {'C':2, 'D':1, 'd':2, 'c':2, 'e':2, 'E':1})

    def test_empty_string(self):
        assert frequency_sort("") == ""