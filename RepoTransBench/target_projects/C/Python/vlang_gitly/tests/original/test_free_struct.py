class foo:
    pass

def test_struct_foo_field():
    f = foo()
    f.free = 12345
    assert f.free == 12345