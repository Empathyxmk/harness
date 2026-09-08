import warnings

def test_public_warns_user():
    with warnings.catch_warnings(record=True) as w:
        warnings.warn("example warning!", UserWarning)
        assert any("example warning!" in str(warn.message) for warn in w)
        assert any(issubclass(warn.category, UserWarning) for warn in w)

def test_public_warns_deprecation():
    with warnings.catch_warnings(record=True) as w:
        warnings.warn("deprecated soon", DeprecationWarning)
        assert any("deprecated soon" in str(warn.message) for warn in w)
        assert any(issubclass(warn.category, DeprecationWarning) for warn in w)