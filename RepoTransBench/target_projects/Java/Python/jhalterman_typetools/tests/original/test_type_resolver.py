import pytest
import typing

# Helper: extract type variables from __orig_bases__
def _find_type_args(child, parent):
    if hasattr(child, '__orig_bases__'):
        for base in child.__orig_bases__:
            # handle e.g. MyClass[int]
            if hasattr(base, '__args__') and hasattr(base, '__origin__') and base.__origin__ == parent:
                return base.__args__
    # Fallback: check __mro__ for typing.GenericOrigin
    if hasattr(child, '__mro__'):
        for cls in child.__mro__:
            if hasattr(cls, '__orig_bases__'):
                for base in cls.__orig_bases__:
                    if hasattr(base, '__args__') and hasattr(base, '__origin__') and base.__origin__ == parent:
                        return base.__args__
    return None

class TypeResolver:
    @staticmethod
    def resolveRawArgument(param, subType):
        # Given: the generic base param (e.g., list) and a subclass (subType)
        args = _find_type_args(subType, param)
        if args:
            # For classic generic classes, return the first generic argument's type
            # e.g. MyMutator[int] => int
            # if param is typing.Generic and subType is param[X], this will yield (X,)
            return args[0]
        # If param is a direct subclass of subType
        if issubclass(subType, param):
            return param
        return None

    @staticmethod
    def resolveRawArguments(param, subType):
        args = _find_type_args(subType, param)
        if args:
            return args
        return None

# Tests as before...

def test_should_resolve_argument_for_generic_type():
    T = typing.TypeVar('T')
    class Mutator(typing.Generic[T]):
        pass
    class SomeEntity:
        pass
    class MyMutator(Mutator[int]):
        pass
    # The Java test checks that TypeResolver.resolveRawArgument(Mutator.class, MyMutator.class) == Integer.class
    assert TypeResolver.resolveRawArgument(Mutator, MyMutator) == int

def test_should_resolve_argument_when_parameterized_type_matches():
    A = typing.TypeVar('A')
    class Xpto(typing.Generic[A]):
        pass
    class Zaz(typing.Generic[A]):
        pass
    class ImmutableList(Xpto[int], Zaz[int]):
        pass
    assert TypeResolver.resolveRawArgument(Xpto, ImmutableList) == int

def test_should_resolve_argument_for_object_when_not_generic():
    class Some:
        pass
    assert TypeResolver.resolveRawArgument(list, Some) == list

def test_should_return_none_for_unrelated():
    class A:
        pass
    class B:
        pass
    assert TypeResolver.resolveRawArgument(A, B) is None

def test_should_resolve_arguments_for_baz_from_foo():
    T = typing.TypeVar('T')
    S = typing.TypeVar('S')
    class Foo(typing.Generic[T]):
        pass
    class Baz(Foo[dict], typing.Generic[T, S]):
        pass
    args = TypeResolver.resolveRawArguments(Baz, Foo)
    assert args is not None
    assert args[0] == dict

def test_should_resolve_arguments_for_multi():
    T = typing.TypeVar('T')
    U = typing.TypeVar('U')
    class Base(typing.Generic[T, U]):
        pass
    class Sub(Base[int, str]):
        pass
    args = TypeResolver.resolveRawArguments(Base, Sub)
    assert args == (int, str)

def test_should_return_none_if_no_type_args():
    class MyClass:
        pass
    assert TypeResolver.resolveRawArguments(list, MyClass) is None