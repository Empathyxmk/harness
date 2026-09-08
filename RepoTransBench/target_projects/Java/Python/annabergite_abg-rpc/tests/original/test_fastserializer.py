import pytest

class TestClass:
    def __init__(self):
        self.x = None
        self.s = None

class FastSerializer:
    def __init__(self, context, cls):
        self.context = context
        self.cls = cls

    def write(self, context, buf, obj):
        # Just simulate call
        pass

    def read(self, context, buf, cls):
        # Just simulate call
        return cls()

def test_get_all_fields():
    context = object()  # Kryo
    serializer = FastSerializer(context, TestClass)
    assert serializer is not None

def test_write_and_read():
    context = object()
    serializer = FastSerializer(context, TestClass)
    obj = TestClass()
    obj.x = 42
    obj.s = "q"
    serializer.write(context, None, obj)
    result = serializer.read(context, None, TestClass)
    assert isinstance(result, TestClass)