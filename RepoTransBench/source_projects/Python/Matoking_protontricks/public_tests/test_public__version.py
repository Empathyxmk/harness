from protontricks import _version

def test_public_version_attributes():
    assert hasattr(_version, "__version__")
    assert hasattr(_version, "version")
    assert isinstance(_version.version, str)
    assert isinstance(_version.version_tuple, tuple)
    # Use different assertions for public test that are still valid.
    assert _version.__version__.count(".") == 2
    assert len(_version.version_tuple) == 3
    assert _version.__version__.startswith(str(_version.version_tuple[0]))