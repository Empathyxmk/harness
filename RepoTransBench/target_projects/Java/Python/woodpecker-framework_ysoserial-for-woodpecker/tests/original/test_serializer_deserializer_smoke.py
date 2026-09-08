# Translated from SerializerDeserializerSmokeTest.java

import pytest
from io import BytesIO

class Serializer:
    @staticmethod
    def serialize(output_stream, obj):
        if output_stream is None:
            raise NullPointerError()
        if obj is None:
            raise NullPointerError()
        # Simulate serialization
        output_stream.write(b'data')

    @staticmethod
    def serialize_data(obj):
        if obj is None:
            raise NullPointerError()
        return b'data'

class Deserializer:
    @staticmethod
    def deserialize(input_stream):
        if input_stream is None:
            raise NullPointerError()
        data = input_stream.read()
        if data not in [b'data', b'']:
            raise IOError("Bogus data")
        return {}

class NullPointerError(Exception): pass

def test_serializer_null_output_stream():
    with pytest.raises(NullPointerError):
        Serializer.serialize(None, {})

def test_serializer_null_object():
    buf = BytesIO()
    with pytest.raises(NullPointerError):
        Serializer.serialize(buf, None)

def test_deserializer_null_input_stream():
    with pytest.raises(NullPointerError):
        Deserializer.deserialize(None)

def test_deserializer_bogus_data():
    bogus = b"\x01\x02\x03\x04"
    stream = BytesIO(bogus)
    with pytest.raises(IOError):
        Deserializer.deserialize(stream)