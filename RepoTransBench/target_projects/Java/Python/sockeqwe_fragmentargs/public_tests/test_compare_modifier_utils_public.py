def test_compare_modifiers_public_variant():
    PUBLIC = 0x0001
    PRIVATE = 0x0002
    STATIC = 0x0008

    combined = PUBLIC | STATIC
    assert (combined & PUBLIC) != 0
    assert (combined & STATIC) != 0
    assert (combined & PRIVATE) == 0