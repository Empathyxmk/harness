import pytest

def morton(x, y):
    # Interleave bits of x and y. Returns 64-bit Morton code
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
    # De-interleave bits from 64-bit Morton code into lo (x) and hi (y).
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

def rand32():
    # Knuth LCG as in the C code
    rand32.lcg = (rand32.lcg * 6364136223846793005 + 1442695040888963407) & 0xFFFFFFFFFFFFFFFF
    return (rand32.lcg >> 32) & 0xFFFFFFFF
rand32.lcg = 1

def test_basic_cases():
    assert morton(0, 0) == 0
    assert morton(0, 1) == 1
    assert morton(1, 0) == 2
    assert morton(1, 1) == 3

    assert morton(0b0011, 0b0000) == 0b1010
    assert morton(0b0000, 0b0011) == 0b0101
    assert morton(0b1100, 0b0011) == 0b10100101

    assert morton(0x347210d1, 0xc6843fad) == 0x5a346a180755e653

def test_morton_unmorton_roundtrip():
    # 2000 x 2000 times as in C code (but with fewer for speed in Python)
    N = 200
    for i in range(N):
        x = rand32()
        for j in range(2):  # limit, or it will be too slow
            y = rand32()
            z = morton(x, y)
            m = unmorton(z)
            assert m["lo"] == x
            assert m["hi"] == y