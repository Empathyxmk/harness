# Translated from SerializerDeserializerSmokePublicTest.java

import io

class Serializer:
    @staticmethod
    def serialize(obj, output_stream):
        # Trivial serialization: int, uses pickle-like strategy
        output_stream.write(str(obj.n).encode() if obj is not None else b'')

class Deserializer:
    @staticmethod
    def deserialize(input_stream):
        b = input_stream.read()
        return TestObj(int(b.decode())) if b else None

class TestObj:
    def __init__(self, n):
        self.n = n
    def get_n(self):
        return self.n

def test_int_serialization():
    obj = TestObj(9876)
    out = io.BytesIO()
    Serializer.serialize(obj, out)
    out.seek(0)
    o = Deserializer.deserialize(out)
    assert isinstance(o, TestObj)
    assert o.get_n() == 9876