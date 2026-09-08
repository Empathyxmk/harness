import pytest
import pyttsx3

@pytest.fixture
def monkey_init(monkeypatch):
    class DummyEngine:
        def __init__(self, driverName=None, debug=False): self.driverName = driverName
        def say(self, text): return text
        def runAndWait(self): return "ran"
        def stop(self): return "stopped"
        def __getattr__(self, name): return lambda *a, **k: None
    monkeypatch.setattr(pyttsx3, "Engine", DummyEngine)
    monkeypatch.setattr(pyttsx3, "_activeEngines", {})
    return DummyEngine

def test_init_and_engine(monkey_init):
    engine = pyttsx3.init(driverName="dummy")
    assert engine.driverName == "dummy"
    # Don't call speak, it's not a top-level function with driverName arg

def test_engine_cache(monkey_init):
    e1 = pyttsx3.init(driverName="dummy")
    e2 = pyttsx3.init(driverName="dummy")
    assert e1 is e2

def test_engine_unique(monkey_init):
    e1 = pyttsx3.init(driverName="dummy1")
    e2 = pyttsx3.init(driverName="dummy2")
    assert e1 is not e2

def test_engine_methods(monkey_init):
    e1 = pyttsx3.init(driverName="dummy")
    assert e1.say("foo") == "foo"
    assert e1.runAndWait() == "ran"
    assert e1.stop() == "stopped"