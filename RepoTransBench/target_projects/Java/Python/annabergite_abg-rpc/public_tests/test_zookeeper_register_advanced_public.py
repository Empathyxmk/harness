def simulate_register(key, value):
    return key.startswith("public-") and value.startswith("public-")

def test_register_advanced_public():
    key = "public-advanced-key"
    value = "public-advanced-value"
    is_registered = simulate_register(key, value)
    assert is_registered, "Should register advanced public info"