from protontricks import _version

def test_version_attributes():
    assert hasattr(_version, "__version__")
    assert hasattr(_version, "version")
    assert isinstance(_version.version, str)
    assert isinstance(_version.version_tuple, tuple)
    assert _version.__version__ == '0.0.0'
    assert _version.version_tuple == (0, 0, 0)