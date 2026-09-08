import pytest
from src.toUnsafe import toUnsafe

def test_copy_only_componentWillMount_different_return_data_public():
    def fn(): return 99
    mixin = {
        "componentWillMount": fn
    }
    result = toUnsafe(mixin)
    assert result.get("componentWillMount") is None
    assert callable(result.get("UNSAFE_componentWillMount"))
    assert result["UNSAFE_componentWillMount"]() == 99

def test_copy_only_componentWillReceiveProps_different_fn_public():
    called = {"called": False}
    def fn():
        called["called"] = True
        return "public_test"
    mixin = {
        "componentWillReceiveProps": fn
    }
    result = toUnsafe(mixin)
    assert result.get("componentWillReceiveProps") is None
    assert result["UNSAFE_componentWillReceiveProps"] is fn
    assert result["UNSAFE_componentWillReceiveProps"]() == "public_test"
    assert called["called"]

def test_copy_only_componentWillUpdate_different_fn_public():
    def fn(): return 789
    mixin = {
        "componentWillUpdate": fn
    }
    result = toUnsafe(mixin)
    assert result.get("componentWillUpdate") is None
    assert result["UNSAFE_componentWillUpdate"] is fn
    assert result["UNSAFE_componentWillUpdate"]() == 789

def test_not_set_unsafe_keys_if_original_keys_missing_different_keys_public():
    mixin = {"foo": 3, "bar": 4}
    result = toUnsafe(mixin)
    assert result.get("UNSAFE_componentWillMount") is None
    assert result.get("UNSAFE_componentWillReceiveProps") is None
    assert result.get("UNSAFE_componentWillUpdate") is None

def test_retain_all_other_properties_different_other_prop_value_public():
    def cmwm(): return 5
    mixin = {
        "componentWillMount": cmwm,
        "anotherThing": 101
    }
    result = toUnsafe(mixin)
    assert result.get("anotherThing") == 101