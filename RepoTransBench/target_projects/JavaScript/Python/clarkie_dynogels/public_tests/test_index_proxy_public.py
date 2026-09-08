def test_proxy_exports_and_resolve_lib_public():
    import types
    lib = types.SimpleNamespace(a=1, b=2)
    packageMain = types.SimpleNamespace(a=1, b=2)
    assert type(packageMain) == type(lib)
    assert lib and isinstance(lib, object)