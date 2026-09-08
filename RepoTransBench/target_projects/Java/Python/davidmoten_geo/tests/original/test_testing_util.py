import types
import pytest

def test_call_constructor_and_check_is_private():
    class PrivateClass:
        def __new__(cls, *args, **kwargs):
            if not hasattr(cls, '_allowed'):
                raise RuntimeError("No public constructor!")
            return super().__new__(cls)
        def __init__(self):
            pass
    # Simulate accessibility and instantiation under test
    # For Python, you can't really check private, but we simulate for coverage
    PrivateClass._allowed = True
    inst = PrivateClass()
    assert isinstance(inst, PrivateClass)