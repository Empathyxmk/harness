def npfact2d(n, swap=True):
    # Find two factors of n for 2D partitioning
    # Non-increasing order unless swap=False (then, non-decreasing)
    import math
    def first_factor(n):
        for i in range(int(math.sqrt(n)), 0, -1):
            if n % i == 0:
                return i
        return 1
    x = first_factor(n)
    y = n // x
    if swap:
        return x, y
    else:
        return y, x

def test_decomp_all_cases():
    # Default (swap=True, so x >= y)
    x, y = npfact2d(10)
    assert x == 2 and y == 5
    x, y = npfact2d(10, swap=False)
    assert x == 5 and y == 2
    x, y = npfact2d(7)
    assert x == 7 and y == 1
    x, y = npfact2d(7, swap=False)
    assert x == 1 and y == 7
    x, y = npfact2d(2)
    assert x == 2 and y == 1
    x, y = npfact2d(6)
    assert x == 2 and y == 3
    x, y = npfact2d(8)
    assert x == 2 and y == 4