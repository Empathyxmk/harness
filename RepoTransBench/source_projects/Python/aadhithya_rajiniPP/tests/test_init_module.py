import rajinipp

def test_version_and_str():
    # Test __version__ and __version_str__ existence and contents
    assert hasattr(rajinipp, "__version__")
    assert hasattr(rajinipp, "__version_str__")
    assert "rajini++" in rajinipp.__version_str__
    # Test __all__ presence
    assert hasattr(rajinipp, "__all__")

def test_rpp_runner_imported():
    # rpp should be an instance of runner.RppRunner
    from rajinipp.runner import RppRunner
    assert isinstance(rajinipp.rpp, RppRunner)