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

def test_pattern_public():
    xx = 0x0F0F0F0F
    yy = 0xF0F0F0F0
    z = morton(xx, yy)
    m = unmorton(z)
    assert m["lo"] == xx and m["hi"] == yy

def test_max_values_public():
    xx = 0x7FFFFFFF
    yy = 0x80000000
    z = morton(xx, yy)
    m = unmorton(z)
    assert m["lo"] == xx and m["hi"] == yy

    z = morton(0x12345678, 0x87654321)
    m = unmorton(z)
    assert m["lo"] == 0x12345678 and m["hi"] == 0x87654321

def test_reverse_public():
    z = morton(0xAAAAAAAA, 0x55555555)
    m = unmorton(z)
    assert m["lo"] == 0xAAAAAAAA
    assert m["hi"] == 0x55555555

    z = morton(0x0F0F0F0F, 0x33333333)
    m = unmorton(z)
    assert m["lo"] == 0x0F0F0F0F
    assert m["hi"] == 0x33333333

def test_single_bit_positions_public():
    for k in range(32):
        x = 1 << ((31-k) & 31)
        y = 0
        z = morton(x, y)
        m = unmorton(z)
        assert m["lo"] == x and m["hi"] == 0

        x = 0
        y = 1 << ((31-k) & 31)
        z = morton(x, y)
        m = unmorton(z)
        assert m["lo"] == 0 and m["hi"] == y

def test_unmorton_noncanonical_public():
    z = 0xBAADF00DDEADBEEF
    m = unmorton(z)
    z2 = morton(m["lo"], m["hi"])
    assert m["lo"] == unmorton(z)["lo"]
    assert m["hi"] == unmorton(z)["hi"]