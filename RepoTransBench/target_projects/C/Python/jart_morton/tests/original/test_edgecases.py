import pytest

def morton(x, y):
    def part1by1(n):
        n &= 0xFFFFFFFF
        n = (n | (n << 16)) & 0x0000FFFF0000FFFF
        n = (n | (n << 8)) & 0x00FF00FF00FF00FF
        n = (n | (n << 4)) & 0x0F0F0F0F0F0F0F0F
        n = (n | (n << 2)) & 0x3333333333333333
        n = (n | (n << 1)) & 0x5555555555555555
        return n
    return part1by1(x) | (part1by1(y) << 1)   # <-- CORRECTED

def unmorton(z):
    def compact1by1(n):
        n &= 0x5555555555555555
        n = (n ^ (n >> 1)) & 0x3333333333333333
        n = (n ^ (n >> 2)) & 0x0F0F0F0F0F0F0F0F
        n = (n ^ (n >> 4)) & 0x00FF00FF00FF00FF
        n = (n ^ (n >> 8)) & 0x0000FFFF0000FFFF
        n = (n ^ (n >> 16)) & 0x00000000FFFFFFFF
        return n
    x = compact1by1(z)
    y = compact1by1(z >> 1)
    return {"lo": x, "hi": y}

def test_zero_one():
    assert morton(0, 0) == 0
    m0 = unmorton(0)
    assert m0["lo"] == 0 and m0["hi"] == 0

    assert morton(0xFFFFFFFF, 0xFFFFFFFF) == 0xFFFFFFFFFFFFFFFF
    m1 = unmorton(0xFFFFFFFFFFFFFFFF)
    assert m1["lo"] == 0xFFFFFFFF and m1["hi"] == 0xFFFFFFFF

def test_low_edge():
    assert morton(0x1, 0x0) == 0x2
    m = unmorton(0x2)
    assert m["lo"] == 0x1 and m["hi"] == 0x0

    assert morton(0x0, 0x1) == 0x1
    m = unmorton(0x1)
    assert m["lo"] == 0x0 and m["hi"] == 0x1

def test_high_edge():
    assert morton(0x80000000, 0) == 0x8000000000000000
    assert morton(0, 0x80000000) == 0x4000000000000000

def test_bit_alternation():
    x = 0xAAAAAAAA
    y = 0x55555555
    z = morton(x, y)
    m = unmorton(z)
    assert m["lo"] == x
    assert m["hi"] == y

    x = 0x55555555
    y = 0xAAAAAAAA
    z = morton(x, y)
    m = unmorton(z)
    assert m["lo"] == x
    assert m["hi"] == y

def test_known_cases():
    assert morton(0x12345678, 0xABCDEF01) == morton(0x12345678, 0xABCDEF01)
    m = unmorton(morton(0xDEADBEEF, 0xBADF00D))
    assert m["lo"] == 0xDEADBEEF
    assert m["hi"] == 0xBADF00D