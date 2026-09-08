def test_import_all_public():
    import uuslug
    assert hasattr(uuslug, "uuslug")
    assert hasattr(uuslug, "slugify")
    # Additional variation: check for __version__
    assert hasattr(uuslug, "__version__")