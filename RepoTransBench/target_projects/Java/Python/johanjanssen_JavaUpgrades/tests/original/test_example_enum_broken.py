from mockito import mock
import pytest

class ExampleEnum:
    pass

def test_enum_with_methods():
    example_enum = mock(ExampleEnum)
    assert example_enum is not None