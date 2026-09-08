import itsdangerous
import warnings

def test_version_is_string_public():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        version = getattr(itsdangerous, "__version__", None)
        assert isinstance(version, str)
        assert any(issubclass(warning.category, DeprecationWarning) for warning in w)

def test_importlib_version_public():
    import importlib.metadata
    v = importlib.metadata.version("itsdangerous")
    assert isinstance(v, str) and v.count(".") >= 1