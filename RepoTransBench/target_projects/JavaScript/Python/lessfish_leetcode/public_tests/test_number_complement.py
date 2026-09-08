import pytest

# from src.number_complement import find_complement

def find_complement(num):
    if num == 0:
        return 1
    mask = 1
    temp = num
    while temp:
        mask <<= 1
        temp >>= 1
    return (mask - 1) ^ num

class TestFindComplementPublic:
    def test_returns_complement_of_another_positive_number(self):
        assert find_complement(10) == 5   # 1010 -> 0101
        assert find_complement(6) == 1    # 110 -> 001
        assert find_complement(15) == 0   # 1111 -> 0000
        assert find_complement(9) == 6    # 1001 -> 0110

    def test_edge_cases_still_expect_1_for_0(self):
        assert find_complement(0) == 1