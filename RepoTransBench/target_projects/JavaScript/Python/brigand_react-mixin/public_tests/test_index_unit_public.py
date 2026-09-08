import pytest
from src import index

def test_should_throw_if_statics_same_key_present_both_class_and_mixin_different_key_public():
    class MyOtherClass:
        bar = 7
    mixin = {"statics": {"bar": 8}}
    with pytest.raises(index.StaticsConflictError):
        index.onClass(MyOtherClass, mixin)

def test_assign_static_props_from_mixin_if_not_present_different_key_value_public():
    class MyOtherClass:
        pass
    mixin = {"statics": {"extra": 99}}
    index.onClass(MyOtherClass, mixin)
    assert getattr(MyOtherClass, "extra", None) == 99

def test_merges_propTypes_and_defaultProps_using_MANY_MERGED_LOOSE_different_spy_public():
    class MyOtherClass:
        pass
    called = {"called": False}
    def spy():
        called["called"] = True
        return {"newProp": "abc"}
    mixinObj = {
        "propTypes": {"newProp": lambda: True},
        "defaultProps": {"newProp": "abc"},
        "getDefaultProps": spy
    }
    index.onClass(MyOtherClass, mixinObj)
    assert isinstance(getattr(MyOtherClass, "defaultProps", None), dict)
    assert called["called"] is True
    assert "newProp" in MyOtherClass.defaultProps
    assert MyOtherClass.defaultProps["newProp"] == "abc"

def test_should_handle_mixin_mixins_different_keys_public():
    class OtherClass:
        pass
    subMixin = {"contextTypes": {"c": lambda: True}}
    topMixin = {
        "mixins": [subMixin],
        "contextTypes": {"d": lambda: True}
    }
    index.onClass(OtherClass, topMixin)
    ct = getattr(OtherClass, "contextTypes", {})
    assert "c" in ct
    assert "d" in ct

def test_setInitialState_adds_UNSAFE_componentWillMount_if_not_already_present_different_state_key_public():
    from src import index as reactMixinMod
    def getInitialState(self):
        return {"x": 50}
    testMixin = {
        "getInitialState": getInitialState
    }
    class PublicTestClass:
        def __init__(self):
            self.state = {}
    PublicTestClass.prototype = {}
    reactMixinMod.onClass(PublicTestClass, testMixin)
    assert callable(getattr(PublicTestClass, "UNSAFE_componentWillMount", None))
    testInstance = PublicTestClass()
    PublicTestClass.UNSAFE_componentWillMount(testInstance)
    assert testInstance.state["x"] == 50

def test_setInitialState_wraps_original_UNSAFE_componentWillMount_if_present_different_key_and_check_public():
    called = {"called": False}
    def getInitialState(self):
        return {"z": 77}
    def unsafe(self):
        called["called"] = True
    testMixin = {
        "getInitialState": getInitialState,
        "UNSAFE_componentWillMount": unsafe
    }
    class PublicClass:
        def __init__(self):
            self.state = {}
    PublicClass.prototype = {}
    index.onClass(PublicClass, testMixin)
    instance = PublicClass()
    PublicClass.UNSAFE_componentWillMount(instance)
    assert instance.state["z"] == 77
    assert called["called"] is True