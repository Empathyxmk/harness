import rajinipp

def test_public_version_and_str():
    # Test __version__ and __version_str__ existence and structure (not substring)
    assert hasattr(rajinipp, "__version__")
    assert hasattr(rajinipp, "__version_str__")
    # Instead of checking for a substring, check length or format
    assert isinstance(rajinipp.__version_str__, str)
    assert rajinipp.__version_str__.startswith("rajini")
    # Test __all__ type and non-empty
    assert hasattr(rajinipp, "__all__")
    assert isinstance(rajinipp.__all__, list)
    assert len(rajinipp.__all__) > 0

def test_public_rpp_runner_imported():
    # Test type using a different assertion
    from rajinipp.runner import RppRunner
    assert type(rajinipp.rpp).__name__ == "RppRunner"