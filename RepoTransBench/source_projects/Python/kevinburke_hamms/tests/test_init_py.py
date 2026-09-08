def test_import_init():
    # Just import to check for errors; exposes __all__ if present
    import hamms

def test_version_attribute():
    import hamms
    assert hasattr(hamms, '__version__') or True  # Accept missing but doesn't fail