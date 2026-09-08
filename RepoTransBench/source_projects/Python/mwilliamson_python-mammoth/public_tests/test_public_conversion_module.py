import pytest
from mammoth import conversion

class DummyDocument:
    pass

def test_result_from_document_and_messages_public():
    messages = ["public message"]
    doc = DummyDocument()
    result = conversion.Result(doc, messages)
    assert result.value == doc
    assert result.messages == messages

def test_to_result_returns_existing_result_public():
    r = conversion.Result("Y", ["msg2"])
    out = conversion._to_result(r)
    assert out is r

def test_to_result_wraps_value_public():
    val = 9876
    out = conversion._to_result(val)
    assert isinstance(out, conversion.Result)
    assert out.value == val
    assert out.messages == []

def test_result_repr_public():
    messages = ["foo", "bar"]
    doc = DummyDocument()
    result = conversion.Result(doc, messages)
    repr_str = repr(result)
    assert "DummyDocument" in repr_str and "foo" in repr_str and "bar" in repr_str