import pytest
import pyttsx3

def test_init_returns_engine():
    engine = pyttsx3.init(driverName="dummy")
    assert hasattr(engine, "say")
    assert hasattr(engine, "runAndWait")
    assert hasattr(engine, "stop")

def test_init_returns_cached_instance():
    eng1 = pyttsx3.init(driverName="dummy")
    eng2 = pyttsx3.init(driverName="dummy")
    assert eng1 is eng2

def test_init_with_debug_flag():
    eng = pyttsx3.init(driverName="dummy", debug=True)
    assert hasattr(eng, "say")  # Should still be Engine

def test_speak_calls_init_and_engine_methods(monkeypatch):
    calls = {}
    class DummyEngine:
        def __init__(self):
            calls['init'] = True
        def say(self, text): calls['say']=text
        def runAndWait(self): calls['run']=True
    monkeypatch.setattr(pyttsx3, "init", lambda *a, **kw: DummyEngine())
    pyttsx3.speak("text")
    assert calls == {"init": True, "say": "text", "run": True}