import pytest

def test_CPP2DConsumer_basic_public():
    fakeFileName = "dummy_input_public.cpp"
    assert fakeFileName == "dummy_input_public.cpp"
    # Cannot really instantiate external-only C++ class in Python