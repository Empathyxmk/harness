import pytest
import types
from pyttsx3 import driver

class DummyDriver:
    def __init__(self, proxy):
        self.destroyed = False
        self.text_spoken = None
        self.say_called = []
        self.busy = True
    def destroy(self):
        self.destroyed = True
        return True
    def say(self, text):
        self.text_spoken = text
        self.say_called.append(text)
    def stop(self):
        return "stopped"

class DummyEngine:
    def __init__(self):
        self.notifications = []
    def _notify(self, topic, **kw):
        # Just record notification
        self.notifications.append((topic, kw))

def test_driverproxy_init(monkeypatch):
    monkeypatch.setattr(driver.importlib, "import_module", lambda name: types.SimpleNamespace(buildDriver=lambda proxy: DummyDriver(proxy)))
    eng = DummyEngine()
    p = driver.DriverProxy(eng, "dummy", debug=False)
    assert isinstance(p._driver, DummyDriver)
    assert p._engine is eng
    assert p._busy is True
    assert p._queue == []

def test_driverproxy_del(monkeypatch):
    called = {}
    class DummyDrv(DummyDriver):
        def destroy(self_): called['yes']=1
    monkeypatch.setattr(driver.importlib, "import_module", lambda name: types.SimpleNamespace(buildDriver=lambda proxy: DummyDrv(proxy)))
    eng = DummyEngine()
    p = driver.DriverProxy(eng, "dummy", debug=False)
    del p  # Should call destroy on underlying driver

def test_driverproxy_push_and_pump(monkeypatch):
    monkeypatch.setattr(driver.importlib, "import_module", lambda name: types.SimpleNamespace(buildDriver=lambda proxy: DummyDriver(proxy)))
    eng = DummyEngine()
    proxy = driver.DriverProxy(eng, "dummy", debug=True)
    proxy._busy = False
    called = []
    def meth1(text): called.append(text)
    proxy._queue = []
    proxy._push(meth1, ("hello",), name="tid")
    # meth1 should be called and queue is empty now
    assert called == ["hello"]

def test_driverproxy_notify(monkeypatch):
    monkeypatch.setattr(driver.importlib, "import_module", lambda name: types.SimpleNamespace(buildDriver=lambda proxy: DummyDriver(proxy)))
    eng = DummyEngine()
    p = driver.DriverProxy(eng, "dummy", debug=False)
    p._name = "abc"
    p.notify("test_topic", foo=123)
    assert eng.notifications[-1][0] == "test_topic"
    assert eng.notifications[-1][1]["foo"] == 123
    assert eng.notifications[-1][1]["name"] == "abc"

def test_driverproxy_setbusy_and_isbusy(monkeypatch):
    monkeypatch.setattr(driver.importlib, "import_module", lambda name: types.SimpleNamespace(buildDriver=lambda proxy: DummyDriver(proxy)))
    eng = DummyEngine()
    p = driver.DriverProxy(eng, "dummy", debug=False)
    p.setBusy(False)
    assert not p.isBusy()
    p.setBusy(True)
    assert p.isBusy()

def test_driverproxy_say(monkeypatch):
    class DummyDrv(DummyDriver):
        def say(self_, text):
            self_.text_spoken = "spoken"
    monkeypatch.setattr(driver.importlib, "import_module", lambda name: types.SimpleNamespace(buildDriver=lambda proxy: DummyDrv(proxy)))
    eng = DummyEngine()
    p = driver.DriverProxy(eng, "dummy", debug=False)
    p._busy = False
    p.say("abc", "tid")
    # should call DummyDrv.say

def test_driverproxy_stop(monkeypatch):
    class DummyDrv(DummyDriver):
        def stop(self_): self_.stopped = True
    monkeypatch.setattr(driver.importlib, "import_module", lambda name: types.SimpleNamespace(buildDriver=lambda proxy: DummyDrv(proxy)))
    eng = DummyEngine()
    p = driver.DriverProxy(eng, "dummy", debug=False)
    # test stop with empty queue
    p._queue = []
    p.stop()