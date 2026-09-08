import pytest
import random

try:
    from bitarray_py.bitarray import BitArray
except ImportError:
    BitArray = None

def test_public_copy_different_sizes():
    arr = BitArray(40)
    arr.set_region(0, 10)
    def _test_copy(arr2, to, arr1, frm, length):
        str1 = arr1.to_str()
        corr = arr2.to_str()
        corr = list(corr)
        for i in range(length):
            if (frm + i) < len(str1) and (to + i) < len(corr):
                corr[to+i] = str1[frm + i]
        arr2.copy(to, arr1, frm, length)
        str2 = arr2.to_str()
        assert ''.join(corr) == str2

    _test_copy(arr, 5, arr, 0, 10)
    _test_copy(arr, 20, arr, 5, 15)
    _test_copy(arr, 25, arr, 0, 5)

    length = arr.length
    shift = 4
    arr.resize(length + shift)
    _test_copy(arr, shift, arr, 0, length)
    _test_copy(arr, 0, arr, shift, length)

def test_public_get_bits():
    arr = BitArray(80)
    arr.randomize(0.2)
    def _get_bits(arr, start, end):
        setbits = arr.get_bits(start, end)
        flat = arr.to_list()[start:end]
        expected = [i for i, b in enumerate(flat, start) if b]
        assert setbits == expected

    _get_bits(arr, 0, 0)
    _get_bits(arr, 0, 80)
    _get_bits(arr, 80, 80)
    _get_bits(arr, 15, 70)