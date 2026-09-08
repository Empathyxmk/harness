import pytest

def maxbits_length(arr, n):
    """Returns the minimal number of bits needed to encode the largest value in arr[0:n]."""
    if n == 0:
        return 0
    maxval = max(arr[:n])
    return maxval.bit_length()

def simdmaxbitsd1(offset, arr):
    """Returns the max number of bits needed to encode the *difference* between consecutive elements plus offset."""
    n = len(arr)
    if n == 0:
        return 0
    prev = offset
    maxdiff = 0
    for v in arr:
        diff = v - prev
        maxdiff = max(maxdiff, diff)
        prev = v
    return max(1, maxdiff.bit_length())  # In C, always at least 1

def test_maxbits_length_all_zeros():
    zeros = [0] * 128
    assert maxbits_length(zeros, 128) == 0

def test_maxbits_length_all_same():
    vals = [77] * 128
    assert maxbits_length(vals, 128) == 7  # 77 is 7 bits

def test_maxbits_length_single():
    oneval = [255]
    assert maxbits_length(oneval, 1) == 8

def test_simdmaxbitsd1_strictly_increasing():
    a = [i for i in range(128)]
    assert simdmaxbitsd1(0, a) == 1

def test_simdmaxbitsd1_large_difference():
    a = [0]
    for i in range(1, 128):
        a.append(a[-1] + 10000)
    b = simdmaxbitsd1(0, a)
    assert b > 0 and b <= 32