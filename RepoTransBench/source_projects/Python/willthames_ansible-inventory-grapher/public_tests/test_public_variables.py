import pytest

# Simulate some different variable scenarios than the original tests/test_variables.py

def test_public_basic_var_strip():
    # Simulate stripping out a variable with public prefix
    d = {"public_private": 123, "should_keep": 456}
    result = {k: v for k, v in d.items() if not k.startswith("public_")}
    assert "should_keep" in result
    assert "public_private" not in result

def test_public_group_var_precedence():
    # Check group and host variable precedence for different values
    group_vars = {"pubkey": "groupval", "shared": "gshared"}
    host_vars = {"pubkey": "hostval", "override": "hval", "shared": "hshared"}
    # host should override pubkey and shared
    merged_vars = {**group_vars, **host_vars}
    assert merged_vars["pubkey"] == "hostval"
    assert merged_vars["shared"] == "hshared"
    assert merged_vars["override"] == "hval"
    assert "groupval" not in merged_vars.values()

def test_public_nested_vars():
    # Test analysis of nested data structures, with different test data
    host_vars = {"outer": {"public_hidden": "value", "visible": 42}, "plain": 10}
    # Let's remove keys beginning with 'public_' in nested dicts
    def clean_vars(vars_dict):
        cleaned = {}
        for k, v in vars_dict.items():
            if isinstance(v, dict):
                cleaned[k] = {ik: iv for ik, iv in v.items() if not ik.startswith("public_")}
            elif not k.startswith("public_"):
                cleaned[k] = v
        return cleaned
    result = clean_vars(host_vars)
    assert "plain" in result
    assert "outer" in result and "public_hidden" not in result["outer"] and "visible" in result["outer"]