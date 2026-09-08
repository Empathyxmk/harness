import pytest

# Suppose the function to test is in src/number_complement.py
# from src.number_complement import find_complement

# For demonstration, define here:
def find_complement(num):
    if num == 0:
        return 1
    mask = 1
    temp = num
    while temp:
        mask <<= 1
        temp >>= 1
    return (mask - 1) ^ num

class TestFindComplement:
    def test_returns_complement_of_a_positive_number(self):
        assert find_complement(5) == 2    # 101 -> 010
        assert find_complement(1) == 0    # 1 -> 0
        assert find_complement(8) == 7    # 1000 -> 0111
        assert find_complement(0) == 1    # 0 -> 1

    def test_returns_0_for_0(self):
        assert find_complement(0) == 1