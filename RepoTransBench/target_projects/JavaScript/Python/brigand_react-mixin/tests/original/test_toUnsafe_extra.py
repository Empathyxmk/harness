import pytest
from src.toUnsafe import toUnsafe

def test_copy_mixin_only_componentWillMount():
    mixin = {
        "componentWillMount": lambda: 42
    }
    result = toUnsafe(mixin)
    assert result.get("componentWillMount") is None
    assert callable(result.get("UNSAFE_componentWillMount"))
    assert result["UNSAFE_componentWillMount"]() == 42

def test_copy_mixin_only_componentWillReceiveProps():
    called = {"called": False}
    def fn():
        called["called"] = True
    mixin = { "componentWillReceiveProps": fn }
    result = toUnsafe(mixin)
    assert result.get("componentWillReceiveProps") is None
    assert result["UNSAFE_componentWillReceiveProps"] is fn

def test_copy_mixin_only_componentWillUpdate():
    called = {"called": False}
    def fn():
        called["called"] = True
    mixin = { "componentWillUpdate": fn }
    result = toUnsafe(mixin)
    assert result.get("componentWillUpdate") is None
    assert result["UNSAFE_componentWillUpdate"] is fn

def test_do_not_set_unsafe_keys_if_missing():
    mixin = { "a": 1, "b": 2 }
    result = toUnsafe(mixin)
    assert result.get("UNSAFE_componentWillMount") is None
    assert result.get("UNSAFE_componentWillReceiveProps") is None
    assert result.get("UNSAFE_componentWillUpdate") is None

def test_retain_all_other_properties():
    cmwm = lambda: 2
    mixin = { "componentWillMount": cmwm, "somethingElse": 55 }
    result = toUnsafe(mixin)
    assert result["somethingElse"] == 55