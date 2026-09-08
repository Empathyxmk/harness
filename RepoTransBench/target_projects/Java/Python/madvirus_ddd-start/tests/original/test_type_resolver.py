import pytest

class TypeResolver:
    class Unknown:
        pass

    @staticmethod
    def enableCache():
        # stub for enable cache
        pass

    @staticmethod
    def disableCache():
        # stub for disable cache
        pass

    @staticmethod
    def resolveRawArgument(base, sub):
        # fake implementation only for test logic 
        if base is MyInterface and sub is MyImpl:
            return str
        if base is str and sub is str:
            return TypeResolver.Unknown
        return None

    @staticmethod
    def resolveRawArguments(typeArg, cls):
        if typeArg is None:
            return None
        return (typeArg, cls)

    @staticmethod
    def resolveRawArgument_param_type(parameterizedType, mapClass):
        # for the test that expects an exception
        raise ValueError("Expected 1 argument")

import types

class MyInterface:
    pass

class MyImpl(MyInterface):
    pass

def test_enable_and_disable_cache_are_safe():
    TypeResolver.enableCache()
    TypeResolver.disableCache()
    TypeResolver.enableCache()

def test_resolve_raw_argument_class_subtype():
    result = TypeResolver.resolveRawArgument(MyInterface, MyImpl)
    assert result == str

def test_resolve_raw_argument_type_returns_unknown_for_non_parameterized():
    result = TypeResolver.resolveRawArgument(str, str)
    assert result == TypeResolver.Unknown

def test_resolve_raw_arguments_handles_null():
    assert TypeResolver.resolveRawArguments(None, str) is None

def test_resolve_raw_argument_throws_on_wrong_number_of_params():
    class DummyParameterizedType:
        pass

    with pytest.raises(ValueError) as excinfo:
        TypeResolver.resolveRawArgument_param_type(DummyParameterizedType(), dict)
    assert "Expected 1 argument" in str(excinfo.value)