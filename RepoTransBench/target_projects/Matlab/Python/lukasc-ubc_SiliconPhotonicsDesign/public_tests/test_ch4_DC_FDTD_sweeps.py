def dummy_sweep_public(a, b):
    if len(a) == 0 or len(b) == 0:
        return 0
    else:
        return sum([i + j for i, j in zip(a, b)])

def test_sweep_success_public():
    x = [10, 20, 30]
    y = [1, 3, 5]
    res = dummy_sweep_public(x, y)
    assert res == sum([i + j for i, j in zip(x, y)])

def test_empty_input_public():
    res = dummy_sweep_public([], [])
    assert res == 0