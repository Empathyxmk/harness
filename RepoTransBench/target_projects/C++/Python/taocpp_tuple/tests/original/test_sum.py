import pytest

from src.tuple_ops import sum, IntegerSequence, static_assert

def test_sum_basics():
    # Equivalent to C++ static_assert(sum<int, 1,2,3>::value == 6, "");
    static_assert(sum(int, 1, 2, 3) == 6)
    static_assert(sum(int, -1, -2, -3) == -6)
    static_assert(sum(int, 1, -1) == 0)
    static_assert(sum(int, 4, 5, 6) == 15)
    static_assert(sum(int, ) == 0)
    static_assert(sum(int, ) == 0)
    static_assert(sum(int, 1, 2, 3) == 6)
    static_assert(sum(int, 4, 5, 6) == 15)
    static_assert(sum(int, 1, -1) == 0)
    assert sum(int, 4, 5, 6) == 15

    # Equivalent to sum<unsigned, ...>
    static_assert(sum(int, 5, 5) == 10)    # unsigned in C++ but Python single int type
    static_assert(sum(int, ) == 0)

def test_sum_integer_sequence():
    seq = IntegerSequence(int, 2, 3, 4)
    static_assert(sum(seq) == 9)
    assert sum(seq) == 9