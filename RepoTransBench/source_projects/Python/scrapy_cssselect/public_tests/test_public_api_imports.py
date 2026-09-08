import pytest

def test_import_some_attrs_public():
    import cssselect
    # Choose a different subset of attrs and their presence
    for attr in [
        "GenericTranslator",
        "parse",
        "SelectorError",
        "Selector",
        "HTMLTranslator",
    ]:
        assert hasattr(cssselect, attr)
    # Not testing all as in original, different subset tested

def test_version_public():
    import cssselect
    # Change logic slightly: check non-empty string and __version__
    assert cssselect.VERSION != ""
    assert isinstance(cssselect.__version__, str)
    assert len(cssselect.__version__) > 0