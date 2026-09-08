def test_push_back_pointer():
    v = []
    value = 42
    pointer = value  # In Python, just use value, no pointers
    v.append(pointer)  # Should append '42'
    assert len(v) == 1
    assert v[0] == 42