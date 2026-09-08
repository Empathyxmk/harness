import pytest

class Options:
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = Options()
        return cls._instance

def test_options_singleton_public():
    instanceA = Options.getInstance()
    instanceB = Options.getInstance()
    assert instanceA is instanceB  # Different memory references would signal broken singleton
    assert instanceA is not None   # Should not be null

def test_options_address_public():
    ptr1 = Options.getInstance()
    ptr2 = Options.getInstance()
    assert ptr1 is ptr2  # Must be the same object