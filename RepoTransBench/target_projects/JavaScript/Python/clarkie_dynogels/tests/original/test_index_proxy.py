def test_proxy_require_lib(monkeypatch):
    import types
    lib = types.SimpleNamespace(a=1, b=2)
    top = types.SimpleNamespace(a=1, b=2)
    assert sorted(top.__dict__.keys()) == sorted(lib.__dict__.keys())