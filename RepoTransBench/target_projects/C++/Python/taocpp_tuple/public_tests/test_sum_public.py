import pytest

from src.tuple_ops import sum, IntegerSequence, static_assert

def test_sum_basics_public():
    static_assert(sum(int, 4, 5, 6) == 15)
    static_assert(sum(int, 10, 20) == 30)         # unsigned in C++, works as int here
    static_assert(sum(int, ) == 0)
    static_assert(sum(int, -4, -5, -6) == -15)
    static_assert(sum(int, 7, -7) == 0)
    assert sum(int, 8, 9, 10) == 27

def test_sum_integer_sequence_public():
    seq = IntegerSequence(int, 5, 6, 7)
    static_assert(sum(seq) == 18)
    assert sum(seq) == 18