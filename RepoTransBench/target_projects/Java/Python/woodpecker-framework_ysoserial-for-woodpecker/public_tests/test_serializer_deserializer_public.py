# Translated from SerializerDeserializerPublicTest.java

import io

class Dummy:
    def __init__(self, value):
        self.value = value
    def get_value(self):
        return self.value

class Serializer:
    @staticmethod
    def serialize(obj, output_stream):
        output_stream.write(obj.value.encode() if obj is not None else b"")

class Deserializer:
    @staticmethod
    def deserialize(input_stream):
        b = input_stream.read()
        return Dummy(b.decode()) if b else None

def test_serialize_deserialize_simple():
    dummy = Dummy("public_test_1")
    out = io.BytesIO()
    Serializer.serialize(dummy, out)
    out.seek(0)
    obj = Deserializer.deserialize(out)
    assert isinstance(obj, Dummy)
    assert obj.get_value() == "public_test_1"

def test_serialize_deserialize_null():
    out = io.BytesIO()
    Serializer.serialize(None, out)
    out.seek(0)
    obj = Deserializer.deserialize(out)
    assert obj is None