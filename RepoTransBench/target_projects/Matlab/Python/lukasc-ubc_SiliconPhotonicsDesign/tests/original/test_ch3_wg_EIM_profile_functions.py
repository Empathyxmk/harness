def dummy_eim(h, w, n):
    if w == 0:
        return n
    else:
        return (h / w) + n

def test_eim_profile_main():
    out = dummy_eim(10, 2, 1)
    assert out == 4

def test_edge_case_zero_w():
    out = dummy_eim(2, 0, 2)
    assert out == 2