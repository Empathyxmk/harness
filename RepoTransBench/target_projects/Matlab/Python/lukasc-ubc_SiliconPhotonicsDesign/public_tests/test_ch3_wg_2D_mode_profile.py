def dummy_2d_sum_public(m):
    if m is None or len(m) == 0:
        return 0
    total = 0
    for row in m:
        total += sum(row)
    return total

def test_2d_sum_public():
    m = [[1, 3], [5, 7]]
    res = dummy_2d_sum_public(m)
    assert res == 16

def test_2d_sum_empty_public():
    res = dummy_2d_sum_public([])
    assert res == 0