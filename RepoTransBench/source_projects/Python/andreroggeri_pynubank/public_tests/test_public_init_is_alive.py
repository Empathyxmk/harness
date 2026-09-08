from pynubank import __version__, is_alive

def test_is_alive_public():
    assert is_alive() is True

def test_version_exists_public():
    assert isinstance(__version__, str)
    assert "." in __version__