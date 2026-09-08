import pytest
import types
from protofuzz import gen

def test_message_generator_simple(monkeypatch):
    # Just test that it can call the generator with a basic dummy protocol message
    class DummyField:
        def __init__(self, name):
            self.name = name
            self.cpp_type = 1
            self.label = 1
            self.message_type = None

    class DummyDesc:
        def __init__(self):
            self.fields = [DummyField("x")]

    class DummyMsg:
        DESCRIPTOR = DummyDesc()
    dummy_valgen = lambda t, f=None: iter([1, 2])
    objs = list(gen.message_generator(DummyMsg, dummy_valgen, max_messages=2))
    assert isinstance(objs[0], DummyMsg) and isinstance(objs[1], DummyMsg)

def test_message_generator_with_message_type(monkeypatch):
    class DummyMessageType:
        DESCRIPTOR = type("Desc", (), {"fields": []})()

    class DummyField:
        def __init__(self, name, message_type=True):
            self.name = name
            self.cpp_type = 10
            self.label = 1
            self.message_type = DummyMessageType if message_type else None

    class DummyDesc:
        def __init__(self):
            self.fields = [DummyField("another", message_type=True)]

    class DummyMsgParent:
        DESCRIPTOR = DummyDesc()
        def __init__(self):
            self.another = None

    dummy_valgen = lambda t, f=None: iter([DummyMessageType()])
    out = list(gen.message_generator(DummyMsgParent, dummy_valgen, max_messages=1))
    assert isinstance(out[0], DummyMsgParent)

@pytest.mark.parametrize("label, expected", [(1, list), (2, list), (3, list)])
def test__assign_to_field(label, expected):
    class DummyObj:
        pass
    obj = DummyObj()
    field = type("F", (), {"label": label, "name": "foo"})
    value = 42
    out = gen._assign_to_field(obj, field, value)
    assert isinstance(out, expected)