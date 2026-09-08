import injector

def test_dunder_package():
    assert hasattr(injector, "__package__")

def test_dunder_file():
    assert hasattr(injector, "__file__")

def test_attributes_listing():
    attrs = dir(injector)
    assert isinstance(attrs, list)

def test_repr():
    assert "injector" in repr(injector)