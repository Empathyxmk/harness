import pytest
import pyttsx3

@pytest.fixture
def monkey_alt_init_for_api(monkeypatch):
    class YetAnotherDummyEngine:
        def __init__(self, driverName=None, debug=False): self.name = driverName
        def start(self): return "hello"
        def finish(self): return "goodbye"
    monkeypatch.setattr(pyttsx3, "Engine", YetAnotherDummyEngine)
    monkeypatch.setattr(pyttsx3, "_activeEngines", {})
    return YetAnotherDummyEngine

def test_public_engine_creation(monkey_alt_init_for_api):
    engine = pyttsx3.init(driverName="publicengine")
    assert engine.name == "publicengine"

def test_public_engine_singleton(monkey_alt_init_for_api):
    e1 = pyttsx3.init(driverName="publicdummyA")
    e2 = pyttsx3.init(driverName="publicdummyA")
    assert e1 is e2

def test_public_engine_different(monkey_alt_init_for_api):
    e1 = pyttsx3.init(driverName="public1")
    e2 = pyttsx3.init(driverName="public2")
    assert e1 is not e2