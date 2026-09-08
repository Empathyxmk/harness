import pytest

def test_property_load_different_key():
    props = {}
    props["public.test.key"] = "publicValue"
    assert props.get("public.test.key") is not None
    assert props.get("public.test.key") == "publicValue"
    assert props.get("nonexistent.key") is None