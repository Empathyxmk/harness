from ansibleinventorygrapher import version

def test_public_version_string():
    assert isinstance(version.__version__, str)
    assert version.__version__.count(".") == 2