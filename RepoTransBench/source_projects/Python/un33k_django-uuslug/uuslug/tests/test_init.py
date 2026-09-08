def test_import_all():
    import uuslug
    assert hasattr(uuslug, "uuslug")
    assert hasattr(uuslug, "slugify")