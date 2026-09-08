def dummy_safe_func_public(a):
    # In C++: if (a % 2 == 0) { MEMSAFE_PLUGIN_MARK() }
    # In Python, just simulate: do nothing
    if (a % 2) == 0:
        pass  # Marker no-op

def dummy_unsafe_func_public():
    x = 99
    # MEMSAFE_PLUGIN_MARK()
    assert x == 99

def test_dummy_safe_func_public_variants():
    dummy_safe_func_public(6)  # Different value from original
    dummy_safe_func_public(18)

def test_dummy_unsafe_func_public():
    dummy_unsafe_func_public()