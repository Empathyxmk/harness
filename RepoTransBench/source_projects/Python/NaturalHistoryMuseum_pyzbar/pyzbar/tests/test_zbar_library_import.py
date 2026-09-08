def test_zbar_library_import():
    import pyzbar.zbar_library as zl
    # Don't require __version__, just ensure import
    assert hasattr(zl, "__file__")