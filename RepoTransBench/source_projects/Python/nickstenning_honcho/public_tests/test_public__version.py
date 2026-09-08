from honcho._version import __version__, version, __version_tuple__, version_tuple

def test_public_version_values():
    assert __version__ == version
    assert __version_tuple__ == version_tuple

def test_public_version_struct():
    # Intentionally different, check that version is string and tuple is proper type
    assert isinstance(__version__, str)
    assert isinstance(__version_tuple__, tuple)