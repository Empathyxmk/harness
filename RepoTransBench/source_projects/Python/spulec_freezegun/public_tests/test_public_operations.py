def test_public_unique_set_elements():
    s = set([7, 8, 7, 6])
    assert len(s) == 3
    assert set(s) == {6, 7, 8}

def test_public_sum_dict_keys():
    d = {"a": 14, "b": 12}
    assert sum(d.values()) == 26

def test_public_tuple_concat():
    t = (7, 8) + (9, 10)
    assert t == (7, 8, 9, 10)