import pytest

from tests.original.test_fragment_args import FragmentArgs

def test_inject_handles_classnotfoundexception():
    # ensure static field is null
    FragmentArgs.autoMappingInjector = None
    # injectFromBundle should catch the exception and not throw
    FragmentArgs.injectFromBundle(object())
    # autoMappingInjector remains None
    assert FragmentArgs.autoMappingInjector is None

def test_inject_handles_instantiationexception():
    # ensure static field is null
    FragmentArgs.autoMappingInjector = None
    # injectFromBundle should catch the exception
    FragmentArgs.injectFromBundle(object())
    # autoMappingInjector remains None
    assert FragmentArgs.autoMappingInjector is None