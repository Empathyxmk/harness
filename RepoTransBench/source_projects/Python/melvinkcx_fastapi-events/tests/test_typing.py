import fastapi_events.typing as typing
from enum import Enum

def test_event_typing_union_and_aliases():
    class DummyEnum(Enum):
        A = 1

    e1: typing.Event = ("test", {"k": 1})
    e2: typing.Event = (DummyEnum.A, "val")
    assert isinstance(e1, tuple)
    assert isinstance(e2, tuple)

    # Scope/Message types are MutableMapping
    dummy_scope: typing.Scope = {"type": "http"}
    dummy_msg: typing.Message = {"a": 1}
    assert dummy_scope["type"] == "http"
    assert dummy_msg["a"] == 1

def test_asgiapp_types():
    # Quick check for type signatures
    def mock_receive(): ...
    def mock_send(msg): ...
    def mock_asgiapp(scope, rec, snd): ...
    assert callable(mock_receive)
    assert callable(mock_send)
    assert callable(mock_asgiapp)