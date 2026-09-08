import pytest
import random
import string

import sys

# The following would import your BitArray implementation
try:
    from bitarray_py.bitarray import BitArray
except ImportError:
    BitArray = None  # Use a local stub if absent

def cumm_sum(num):
    return num * ((num+1)//2) + (0 if num & 1 else num//2)

def random_bits(length, prob=0.5):
    # Returns list of bools
    return [random.random() < prob for _ in range(length)]

def as_str(bits):
    # Convert list of bools to str
    return ''.join('1' if b else '0' for b in bits)

@pytest.fixture(autouse=True)
def seed_rand():
    random.seed(12345)

def test_copy():
    arr_len = 200
    arr = BitArray(arr_len)
    arr.set_region(0, 20)

    # Helper: create and compare two bitarrays
    def _test_copy(arr2, to, arr1, frm, length):
        str1 = arr1.to_str()
        corr = arr2.to_str()
        corr = list(corr)
        for i in range(length):
            if (frm + i) < len(str1) and (to + i) < len(corr):
                corr[to+i] = str1[frm + i]
        # Perform actual copy
        arr2.copy(to, arr1, frm, length)
        str2 = arr2.to_str()
        assert ''.join(corr) == str2

    _test_copy(arr, 30, arr, 0, 15)
    _test_copy(arr, 50, arr, 0, 50)
    _test_copy(arr, 100, arr, 0, 100)

    length = arr.length
    shift = 3
    arr.resize(length + shift)
    _test_copy(arr, shift, arr, 0, length)
    _test_copy(arr, 0, arr, shift, length)

def test_get_bits():
    arr = BitArray(200)
    arr.randomize(0.5)
    # must define BitArray.get_bits(start, end) -> list of set indices
    def _get_bits(arr, start, end):
        setbits = arr.get_bits(start, end)
        flat = arr.to_list()[start:end]
        expected = [i for i, b in enumerate(flat, start) if b]
        assert setbits == expected

    _get_bits(arr, 0, 0)
    _get_bits(arr, 0, 200)
    _get_bits(arr, 200, 200)
    _get_bits(arr, 50, 150)

def test_arithmetic():
    arr1 = BitArray(100)
    arr2 = BitArray(100)

    for i in range(0, 99, 3):
        arr1.set_bit(i)
        arr2.set_bit(i)
        arr2.set_bit(i+1)

    arr1.add_uint64(1)
    arr1.sub_uint64(1)
    arr1.add(arr1, arr2)
    arr1.subtract(arr1, arr2)
    arr1.subtract(arr1, arr1)
    arr1.add(arr1, arr2)
    arr1.add(arr1, arr2)

def test_first_last_bit_set():
    arr = BitArray(100)
    def _check_first_last_bit_set(arr, not_zero, first, last):
        fs, first_bit = arr.find_first_set_bit()
        ls, last_bit = arr.find_last_set_bit()
        assert fs == not_zero
        assert ls == not_zero
        if not_zero:
            assert first_bit == first
            assert last_bit == last
        else:
            assert first_bit == 0
            assert last_bit == 0

    _check_first_last_bit_set(arr, False, 0, 0)
    arr.set_bits([0, 5, 24, 64, 80, 99])
    _check_first_last_bit_set(arr, True, 0, 99)
    arr.clear_bits([0, 99])
    _check_first_last_bit_set(arr, True, 5, 80)
    arr.clear_bits([5, 80])
    _check_first_last_bit_set(arr, True, 24, 64)
    arr.clear_bits([24, 64])
    _check_first_last_bit_set(arr, False, 0, 0)
    arr.set_bit(0)
    _check_first_last_bit_set(arr, True, 0, 0)
    # Loop
    bits = [0, 1, 31, 62, 63, 64, 65, 98, 99]
    for pos in bits:
        arr.clear_all()
        arr.set_bit(pos)
        _check_first_last_bit_set(arr, True, pos, pos)

def test_next_prev_bit_set():
    arr = BitArray(100)
    def _test_find_next_bit(arr, offset):
        found, pos = arr.find_next_set_bit(offset)
        arr.toggle_all()
        found2, pos2 = arr.find_next_clear_bit(offset)
        arr.toggle_all()
        assert found == found2
        assert pos == pos2
        return found, pos

    def _test_find_prev_bit(arr, offset):
        found, pos = arr.find_prev_set_bit(offset)
        arr.toggle_all()
        found2, pos2 = arr.find_prev_clear_bit(offset)
        arr.toggle_all()
        assert found == found2
        assert pos == pos2
        return found, pos

    # Empty
    for idx in [0, 50, 99]:
        found, pos = _test_find_next_bit(arr, idx)
        assert not found and pos == 0
        found, pos = _test_find_prev_bit(arr, idx)
        assert not found and pos == 0

    arr.set_bit(0)
    found, pos = _test_find_prev_bit(arr, 0)
    assert not found and pos == 0
    found, pos = _test_find_next_bit(arr, 0)
    assert found and pos == 0

    arr.set_bit(99)
    found, pos = _test_find_prev_bit(arr, 99)
    assert found and pos == 0
    found, pos = _test_find_next_bit(arr, 99)
    assert found and pos == 99

    arr.set_bits([10, 20, 64])
    found, pos = _test_find_prev_bit(arr, 99)
    assert found and pos == 64
    found, pos = _test_find_prev_bit(arr, 64)
    assert found and pos == 20
    found, pos = _test_find_next_bit(arr, 1)
    assert found and pos == 10
    found, pos = _test_find_next_bit(arr, 11)
    assert found and pos == 20

    # Automated loop
    indices = [0, 1, 2, 5, 24, 50, 51, 64, 80, 99]
    nidx = len(indices)
    for n in range(nidx+1):
        arr.clear_all()
        for i in range(n):
            arr.set_bit(indices[i])
        for i in range(n):
            found, pos = _test_find_next_bit(arr, indices[i])
            assert found
            assert pos == indices[i]
            if indices[i]+1 < arr.length:
                found, pos = _test_find_next_bit(arr, indices[i]+1)
                if i+1 < n:
                    assert found and pos == indices[i+1]
                else:
                    assert not found
    for n in range(nidx+1):
        arr.clear_all()
        for i in range(n):
            arr.set_bit(indices[nidx-i-1])
        for i in range(n):
            found, pos = _test_find_prev_bit(arr, indices[nidx-i-1])
            if i+1 < n:
                assert found and pos == indices[nidx-i-2]
            else:
                assert not found

def test_parity():
    arr = BitArray(100)
    assert arr.parity() == 0
    arr.set_bits([0, 5, 24, 64, 80, 99])
    assert arr.parity() == 0
    arr.clear_bit(24)
    assert arr.parity() == 1
    arr.clear_bit(99)
    assert arr.parity() == 0
    arr.clear_bit(0)
    assert arr.parity() == 1

def test_interleave():
    arr1 = BitArray(5)
    arr1.set_bits([0, 2])
    arr2 = BitArray(5)
    arr2.set_bits([1, 4])
    result = BitArray(10)
    result.interleave(arr1, arr2)
    # Expected: arr1 bits in even, arr2 in odd positions
    exp = ['0']*10
    a1s = arr1.to_list()
    a2s = arr2.to_list()
    for i in range(5):
        exp[2*i] = '1' if a1s[i] else '0'
        exp[2*i+1] = '1' if a2s[i] else '0'
    got = result.to_str()
    assert got == ''.join(exp)