import pytest

class TypeDescriptor:
    BOOLEAN_TYPE = object()
    BYTE_TYPE = object()
    CHAR_TYPE = object()
    DOUBLE_TYPE = object()
    FLOAT_TYPE = object()
    INT_TYPE = object()

def test_primitive_types_are_singletons():
    assert TypeDescriptor.BOOLEAN_TYPE is not None
    assert TypeDescriptor.BYTE_TYPE is not None
    assert TypeDescriptor.CHAR_TYPE is not None
    assert TypeDescriptor.DOUBLE_TYPE is not None
    assert TypeDescriptor.FLOAT_TYPE is not None
    assert TypeDescriptor.INT_TYPE is not None