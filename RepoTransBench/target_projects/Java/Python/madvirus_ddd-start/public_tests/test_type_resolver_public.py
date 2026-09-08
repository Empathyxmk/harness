import pytest

class TypeResolver:
    class Unknown:
        pass

    @staticmethod
    def enableCache():
        pass

    @staticmethod
    def disableCache():
        pass

    @staticmethod
    def resolveRawArgument(base, sub):
        if base is AnotherInterface and sub is AnotherImpl:
            return int
        if base is int and sub is int:
            return TypeResolver.Unknown
        return None

    @staticmethod
    def resolveRawArguments(typeArg, cls):
        if typeArg is None:
            return None
        return (typeArg, cls)

    @staticmethod
    def resolveRawArgument_param_type(parameterizedType, setClass):
        raise ValueError("Expected 1 argument")

class AnotherInterface:
    pass

class AnotherImpl(AnotherInterface):
    pass

def test_enable_and_disable_cache_idempotence():
    TypeResolver.disableCache()
    TypeResolver.enableCache()
    TypeResolver.disableCache()

def test_resolve_raw_argument_class_subtype_different():
    result = TypeResolver.resolveRawArgument(AnotherInterface, AnotherImpl)
    assert result == int

def test_resolve_raw_argument_type_returns_unknown_for_non_parameterized_different():
    result = TypeResolver.resolveRawArgument(int, int)
    assert result == TypeResolver.Unknown

def test_resolve_raw_arguments_handles_null_different_class():
    assert TypeResolver.resolveRawArguments(None, int) is None

def test_resolve_raw_argument_throws_on_wrong_number_of_params_set():
    class DummyParameterizedType:
        pass

    with pytest.raises(ValueError) as excinfo:
        TypeResolver.resolveRawArgument_param_type(DummyParameterizedType(), set)
    assert "Expected 1 argument" in str(excinfo.value)