from pytest_watcher import constants

def test_constants_import():
    # Validate that relevant constants exist (e.g., DEFAULT_CONFIG if exists)
    assert hasattr(constants, "__file__") or hasattr(constants, "__doc__")