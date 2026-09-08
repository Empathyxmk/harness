def test_import_zbar_library_public():
    # Test alternate import of zbar_library, assert type of attribute
    import pyzbar.zbar_library as zl
    assert hasattr(zl, "__file__")
    assert isinstance(zl.__name__, str)