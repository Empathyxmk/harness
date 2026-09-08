def test_init_public():
    import pyzbar
    # This is a basic import test, so check for a different attribute
    assert hasattr(pyzbar, "__doc__")
    # Ensures the __version__ attribute exists
    assert hasattr(pyzbar, "__version__")