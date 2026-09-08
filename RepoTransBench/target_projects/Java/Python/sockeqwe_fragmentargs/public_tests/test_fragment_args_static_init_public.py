import pytest

from tests.original.test_fragment_args import FragmentArgs

def test_inject_handles_classnotfoundexception_public_case():
    FragmentArgs.autoMappingInjector = None
    FragmentArgs.injectFromBundle("alternatePublicData")
    assert FragmentArgs.autoMappingInjector is None

def test_inject_handles_instantiationexception_public():
    FragmentArgs.autoMappingInjector = None
    FragmentArgs.injectFromBundle(555)
    assert FragmentArgs.autoMappingInjector is None