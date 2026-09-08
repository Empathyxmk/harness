def test_push_back_pointer_public():
    v = []
    a = 7
    b = 19

    v.append(b)  # push b first
    v.append(a)  # then a

    assert v[0] == 19
    assert v[1] == 7