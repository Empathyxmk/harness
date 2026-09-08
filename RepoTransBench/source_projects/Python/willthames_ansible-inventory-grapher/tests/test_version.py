from ansibleinventorygrapher import version

def test_version_string():
    assert isinstance(version.__version__, str)
    assert "." in version.__version__