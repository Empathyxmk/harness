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

def test_zero_one_public():
    assert morton(0, 0) == 0
    m0 = unmorton(0)
    assert m0["lo"] == 0 and m0["hi"] == 0

    assert morton(0xAAAAAAAA, 0x55555555) == 0xFFFFFFFFFFFFFFFF // 3
    m1 = unmorton(0xFFFFFFFFFFFFFFFF // 3)
    assert m1["lo"] == 0xAAAAAAAA and m1["hi"] == 0x55555555

def test_low_edge_public():
    assert morton(0x2, 0x1) == 0x6
    m = unmorton(0x6)
    assert m["lo"] == 0x2 and m["hi"] == 0x1

    assert morton(0x3, 0x4) == 0x1B
    m = unmorton(0x1B)
    assert m["lo"] == 0x3 and m["hi"] == 0x4

def test_high_edge_public():
    assert morton(0x40000000, 0) == 0x2000000000000000
    assert morton(0, 0x40000000) == 0x1000000000000000

def test_bit_alternation_public():
    x = 0x33333333
    y = 0xCCCCCCCC
    z = morton(x, y)
    m = unmorton(z)
    assert m["lo"] == x
    assert m["hi"] == y

    x = 0x0F0F0F0F
    y = 0xF0F0F0F0
    z = morton(x, y)
    m = unmorton(z)
    assert m["lo"] == x
    assert m["hi"] == y

def test_known_cases_public():
    assert morton(0x1A2B3C4D, 0x5E6F7081) == morton(0x1A2B3C4D, 0x5E6F7081)
    m = unmorton(morton(0xCAFEBABE, 0xDEADC0DE))
    assert m["lo"] == 0xCAFEBABE
    assert m["hi"] == 0xDEADC0DE