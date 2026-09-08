def test_public_import_alias_int():
    import builtins as blt
    num_type = getattr(blt, 'int')
    x = num_type('456')
    assert x == 456
    assert isinstance(x, int)

def test_public_import_alias_list():
    import builtins as blt
    list_type = getattr(blt, 'list')
    y = list_type((1,2,3))
    assert y == [1, 2, 3]