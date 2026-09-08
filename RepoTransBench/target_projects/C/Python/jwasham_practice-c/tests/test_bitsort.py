import pytest

N = 64
a = [0] * (1 + N // 32)

def set_bit(i):
    idx = i >> 5
    off = i & 0x1F
    a[idx] |= (1 << off)

def clr_bit(i):
    idx = i >> 5
    off = i & 0x1F
    a[idx] &= ~(1 << off)

def test_bit(i):
    idx = i >> 5
    off = i & 0x1F
    return (a[idx] & (1 << off)) != 0

def test_bitsort_basic():
    for i in range(N):
        clr_bit(i)
    for i in range(0, N, 2):  # set even bits
        set_bit(i)
    for i in range(N):
        if i%2 == 0:
            assert test_bit(i)
        else:
            assert not test_bit(i)
    for i in range(N):
        clr_bit(i)
    for i in range(N):
        assert not test_bit(i)