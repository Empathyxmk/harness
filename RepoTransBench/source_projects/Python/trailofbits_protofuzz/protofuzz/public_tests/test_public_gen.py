import pytest
from protofuzz import gen

def test_message_generator_simple_public(monkeypatch):
    # Use different DummyField name and different dummy_valgen
    class DummyField:
        def __init__(self, name):
            self.name = name
            self.cpp_type = 2
            self.label = 1
            self.message_type = None

    class DummyDesc:
        def __init__(self):
            self.fields = [DummyField("y")]

    class DummyMsg:
        DESCRIPTOR = DummyDesc()
    dummy_valgen = lambda t, f=None: iter([99, 100])
    objs = list(gen.message_generator(DummyMsg, dummy_valgen, max_messages=2))
    assert isinstance(objs[0], DummyMsg) and isinstance(objs[1], DummyMsg)

def test_message_generator_with_message_type_public(monkeypatch):
    class AnotherDummyMessageType:
        DESCRIPTOR = type("Desc", (), {"fields": []})()

    class DummyField:
        def __init__(self, name, message_type=True):
            self.name = name
            self.cpp_type = 20
            self.label = 1
            self.message_type = AnotherDummyMessageType if message_type else None

    class DummyDesc:
        def __init__(self):
            self.fields = [DummyField("different", message_type=True)]

    class DummyMsgParent:
        DESCRIPTOR = DummyDesc()
        def __init__(self):
            self.different = None

    dummy_valgen = lambda t, f=None: iter([AnotherDummyMessageType()])
    out = list(gen.message_generator(DummyMsgParent, dummy_valgen, max_messages=1))
    assert isinstance(out[0], DummyMsgParent)

@pytest.mark.parametrize("label, expected", [(1, list), (2, list), (3, list)])
def test__assign_to_field_public(label, expected):
    class DummyObj:
        pass
    obj = DummyObj()
    field = type("F", (), {"label": label, "name": "bar"})
    value = 77
    out = gen._assign_to_field(obj, field, value)
    assert isinstance(out, expected)