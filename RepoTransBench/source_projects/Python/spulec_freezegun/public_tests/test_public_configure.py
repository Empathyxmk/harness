def test_public_configure_env(monkeypatch):
    key = "PUBLIC_FG_TEST_ENVVAR"
    monkeypatch.setenv(key, "enabled")
    import os
    assert os.getenv(key) == "enabled"
    monkeypatch.delenv(key)
    assert os.getenv(key) is None

def test_public_configure_setattr_reversibility():
    class Dummy:
        pass
    d = Dummy()
    setattr(d, "foo", 77)
    assert getattr(d, "foo") == 77
    delattr(d, "foo")
    assert not hasattr(d, "foo")