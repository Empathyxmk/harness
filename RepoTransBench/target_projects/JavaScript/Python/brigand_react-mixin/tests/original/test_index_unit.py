import pytest
from src import index

def test_should_throw_if_statics_with_same_key_present():
    class MyClass:
        foo = 1
    mixin = {"statics": {"foo": 2}}
    with pytest.raises(index.StaticsConflictError):
        index.onClass(MyClass, mixin)

def test_assign_static_props_from_mixin_if_not_present_on_class():
    class MyClass:
        pass
    mixin = {"statics": {"stuff": 42}}
    index.onClass(MyClass, mixin)
    assert getattr(MyClass, "stuff", None) == 42

def test_merges_propTypes_and_defaultProps_with_MANY_MERGED_LOOSE():
    class MyClass:
        pass
    called_spy = {"called": False}
    def spy():
        called_spy["called"] = True
        return {}
    mixinObj = {
        "propTypes": {},
        "defaultProps": {},
        "getDefaultProps": spy
    }
    index.onClass(MyClass, mixinObj)
    assert isinstance(getattr(MyClass, "defaultProps", None), dict)
    assert called_spy["called"] is True

def test_should_handle_mixin_mixins():
    class MyClass:
        pass
    subMixin = {"contextTypes": {"a": lambda: True}}
    topMixin = {"mixins": [subMixin], "contextTypes": {"b": lambda: True}}
    index.onClass(MyClass, topMixin)
    ct = getattr(MyClass, "contextTypes", {})
    assert "a" in ct
    assert "b" in ct

def test_setInitialState_adds_method_to_UNSAFE_componentWillMount_if_not_already_present():
    from src import index as reactMixinMod
    def getInitialState(self):
        return {"a": 1}
    testMixin = { "getInitialState": getInitialState }
    class TestClass:
        def __init__(self):
            self.state = {}
    TestClass.prototype = {}
    reactMixinMod.onClass(TestClass, testMixin)
    assert callable(getattr(TestClass, "UNSAFE_componentWillMount", None))
    testInstance = TestClass()
    TestClass.UNSAFE_componentWillMount(testInstance)
    assert testInstance.state["a"] == 1

def test_setInitialState_wraps_original_UNSAFE_componentWillMount_if_present():
    didCall = {"called": False}
    def getInitialState(self):
        return {"b": 2}
    def original_UNSAFE(self):
        didCall["called"] = True
    testMixin = { "getInitialState": getInitialState, "UNSAFE_componentWillMount": original_UNSAFE }
    class TestClass:
        def __init__(self):
            self.state = {}
    TestClass.prototype = {}
    index.onClass(TestClass, testMixin)
    testInstance = TestClass()
    TestClass.UNSAFE_componentWillMount(testInstance)
    assert testInstance.state["b"] == 2
    assert didCall["called"] is True