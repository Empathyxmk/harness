import gscholar.version

def test_public_version_string():
    assert isinstance(gscholar.version.__VERSION__, str)
    assert len(gscholar.version.__VERSION__) >= 1

def test_public_version_not_empty():
    assert gscholar.version.__VERSION__ != ""

def test_public_version_contains_dot():
    # Check that the version string contains a dot (semantic versioning like "1.2.3")
    assert "." in gscholar.version.__VERSION__