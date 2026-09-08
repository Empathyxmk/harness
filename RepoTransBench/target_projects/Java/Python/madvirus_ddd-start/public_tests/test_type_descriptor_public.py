import pytest

class TypeDescriptor:
    LONG_TYPE = object()
    SHORT_TYPE = object()

def test_other_primitive_types_are_singletons():
    assert TypeDescriptor.LONG_TYPE is not None
    assert TypeDescriptor.SHORT_TYPE is not None