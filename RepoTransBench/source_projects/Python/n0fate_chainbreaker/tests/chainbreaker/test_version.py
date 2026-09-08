import chainbreaker.version

def test_version_str():
    assert isinstance(chainbreaker.version.__version__, str)
    assert chainbreaker.version.__version__.count(".") >= 1