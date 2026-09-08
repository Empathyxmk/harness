import pytest

def simdmin(arr):
    return min(arr)

def simdmax(arr):
    return max(arr)

def simdsum(arr):
    return sum(arr)

def simdbitcpy(dst, src, n):
    for i in range(n):
        dst[i] = src[i]

def test_simdmin():
    assert simdmin([100, 150, 20, 37]) == 20
    assert simdmin([300, 222, 444, 123]) == 123
    assert simdmin([1234, 5678, 9012, 3456]) == 1234
    assert simdmin([90, 80, 70, 60]) == 60

def test_simdmax():
    assert simdmax([9, 99, 888, 7]) == 888
    assert simdmax([100, 84, 56, 120]) == 120
    assert simdmax([1111, 2222, 3333, 4444]) == 4444
    assert simdmax([17, 19, 11, 23]) == 23

def test_simdsum():
    assert simdsum([1, 2, 3, 4]) == 10
    assert simdsum([5, 10, 15, 20]) == 50
    assert simdsum([0, 0, 0, 0]) == 0
    assert simdsum([1000, 2000, 3000, 4000]) == 10000

def test_simdbitcpy():
    src = [0xF0F0F0F0, 0x0F0F0F0F, 0xCCCCCCCC, 0x33333333]
    dst = [0, 0, 0, 0]
    simdbitcpy(dst, src, 4)
    assert dst == src