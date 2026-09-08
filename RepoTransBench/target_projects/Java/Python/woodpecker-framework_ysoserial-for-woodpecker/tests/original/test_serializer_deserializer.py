# Translated from SerializerDeserializerTest.java

import tempfile
import os
from io import BytesIO
import pytest

class DummySerializable:
    def __init__(self, value):
        self.value = value
    def __eq__(self, other):
        return isinstance(other, DummySerializable) and self.value == other.value

class Serializer:
    @staticmethod
    def serialize(obj, output_stream=None):
        data = str(obj.value).encode() if isinstance(obj, DummySerializable) else b''
        if output_stream is not None:
            output_stream.write(data)
            return None
        return data
    def __init__(self, obj):
        self.obj = obj
    def call(self):
        return Serializer.serialize(self.obj)

class Deserializer:
    @staticmethod
    def deserialize(input_data):
        if isinstance(input_data, bytes):
            return DummySerializable(input_data.decode())
        elif hasattr(input_data, 'read'):
            data = input_data.read()
            return DummySerializable(data.decode())
        else:
            raise ValueError("Unsupported input")
    def __init__(self, data):
        self.data = data
    def call(self):
        return Deserializer.deserialize(self.data)
    @staticmethod
    def main(argv):
        # simulate main
        pass

def test_serialize_and_deserialize():
    test_obj = DummySerializable("foo")
    data = Serializer.serialize(test_obj)
    result = Deserializer.deserialize(data)
    assert test_obj == result

def test_serializer_callable():
    test_obj = DummySerializable("bar")
    s = Serializer(test_obj)
    data = s.call()
    assert Deserializer.deserialize(data) == test_obj

def test_deserializer_callable():
    test_obj = DummySerializable("baz")
    s = Serializer(test_obj)
    data = s.call()
    d = Deserializer(data)
    assert d.call() == test_obj

def test_serialize_to_output_stream():
    test_obj = DummySerializable("baz")
    buf = BytesIO()
    Serializer.serialize(test_obj, buf)
    buf.seek(0)
    result = Deserializer.deserialize(buf)
    assert result == test_obj

def test_deserialize_from_input_stream():
    test_obj = DummySerializable("boo")
    data = Serializer.serialize(test_obj)
    buf = BytesIO(data)
    result = Deserializer.deserialize(buf)
    assert result == test_obj

def test_main_method_of_deserializer(monkeypatch):
    test_obj = DummySerializable("mainTest")
    data = Serializer.serialize(test_obj)
    with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
        tmpfile.write(data)
        tmpfile.flush()
        tmpfile.seek(0)
        orig_stdin = os.dup(0)
        try:
            with open(tmpfile.name, "rb") as f:
                os.dup2(f.fileno(), 0)
                Deserializer.main([])
        finally:
            os.dup2(orig_stdin, 0)
        os.unlink(tmpfile.name)

def test_serialize_null_throws():
    with pytest.raises(AttributeError):
        Serializer.serialize(None)