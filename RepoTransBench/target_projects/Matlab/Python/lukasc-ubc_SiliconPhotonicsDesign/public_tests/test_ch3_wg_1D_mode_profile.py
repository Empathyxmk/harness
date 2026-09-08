def dummy_mode_profile_public(arr):
    if len(arr) == 0:
        return 0
    else:
        return sum(arr)

def test_mode_profile_public():
    res = dummy_mode_profile_public([4, 5, 6])
    assert res == 15

def test_mode_empty_public():
    res = dummy_mode_profile_public([])
    assert res == 0