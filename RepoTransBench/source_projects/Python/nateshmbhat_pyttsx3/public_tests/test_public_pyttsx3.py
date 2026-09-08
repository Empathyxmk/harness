import pytest
import pyttsx3

@pytest.fixture
def monkey_alt_init(monkeypatch):
    class AnotherDummyEngine:
        def __init__(self, driverName=None, debug=False): self.driverName = driverName
        def say(self, text): return text[::-1]
        def runAndWait(self): return "executed"
        def stop(self): return "halted"
        def __getattr__(self, name): return lambda *a, **k: "default"
    monkeypatch.setattr(pyttsx3, "Engine", AnotherDummyEngine)
    monkeypatch.setattr(pyttsx3, "_activeEngines", {})
    return AnotherDummyEngine

def test_public_init_and_engine(monkey_alt_init):
    engine = pyttsx3.init(driverName="diffdummy")
    assert engine.driverName == "diffdummy"

def test_public_engine_cache(monkey_alt_init):
    e1 = pyttsx3.init(driverName="cachetestA")
    e2 = pyttsx3.init(driverName="cachetestA")
    assert e1 is e2

def test_public_engine_unique(monkey_alt_init):
    e1 = pyttsx3.init(driverName="uniqueA")
    e2 = pyttsx3.init(driverName="uniqueB")
    assert e1 is not e2

def test_public_engine_methods(monkey_alt_init):
    e1 = pyttsx3.init(driverName="diffdummy")
    assert e1.say("bar") == "rab"
    assert e1.runAndWait() == "executed"
    assert e1.stop() == "halted"