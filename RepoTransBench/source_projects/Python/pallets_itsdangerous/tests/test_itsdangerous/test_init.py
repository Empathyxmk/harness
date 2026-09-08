import itsdangerous
import warnings

def test_version_is_string():
    # __version__ might be present as attribute; must not raise or fail
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        version = getattr(itsdangerous, "__version__", None)
        assert isinstance(version, str)
        # Make sure the deprecation warning is issued but does not cause test failure
        assert any(issubclass(warning.category, DeprecationWarning) for warning in w)

def test_importlib_version():
    # This is the recommended method per deprecation message
    import importlib.metadata
    v = importlib.metadata.version("itsdangerous")
    assert isinstance(v, str) and "." in v