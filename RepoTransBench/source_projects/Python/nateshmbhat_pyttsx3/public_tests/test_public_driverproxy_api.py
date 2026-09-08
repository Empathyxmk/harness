import types
import threading
import pytest
from pyttsx3 import driver

class AnotherDummyEngine:
    # Add methods so DriverProxy notify can work without error
    def __init__(self):
        self.notified = []
    def _notify(self, topic, **kwargs):
        self.notified.append((topic, kwargs))

class AnotherDummyDriver:
    def __init__(self, proxy):
        self.proxy = proxy
        self.said = []
        self.stopped = False
        self.busy = None

    def startLoop(self):
        pass
    def endLoop(self):
        pass
    def say(self, text, name):
        self.said.append((text, name))
    def stop(self):
        self.stopped = True
    def setBusy(self, value):
        self.busy = value
    def notify(self, data):
        pass

def base_driverproxy_for_magic(test_name="queue", driver_cls=AnotherDummyDriver):
    """
    Helper for creating as-complete-as-possible DriverProxy object for tests
    """
    eng = AnotherDummyEngine()
    orig_import_module = driver.importlib.import_module
    driver.importlib.import_module = lambda name: types.SimpleNamespace(buildDriver=lambda proxy: driver_cls(proxy))
    try:
        proxy = driver.DriverProxy(eng, test_name, debug=True)
    finally:
        driver.importlib.import_module = orig_import_module
    return proxy

def test_public_driverproxy_init(monkeypatch):
    monkeypatch.setattr(driver.importlib, "import_module", lambda name: types.SimpleNamespace(buildDriver=lambda proxy: AnotherDummyDriver(proxy)))
    eng = AnotherDummyEngine()
    p = driver.DriverProxy(eng, "otherdummy", debug=True)
    assert isinstance(p._driver, AnotherDummyDriver)
    assert p._engine is eng
    assert p._busy is True

def test_public_driverproxy_del():
    proxy = base_driverproxy_for_magic("del", AnotherDummyDriver)
    try:
        proxy.__del__()
    except Exception:
        assert False, "Del should not raise"

def test_public_driverproxy_push_and_pump():
    proxy = base_driverproxy_for_magic("push", AnotherDummyDriver)
    # Directly manipulate internal queue for demonstration of different data
    proxy._push(lambda x: x.upper(), ("fox",))
    proxy._push(lambda y: y[::-1], ("bottle",))
    # Use the internal queue, then manually drain it
    # As there is no .pump() in pyttsx3==2.90 DriverProxy, we process manually
    collected = []
    while proxy._queue:
        func, args, name = proxy._queue.pop(0)
        collected.append(func(*args))
    assert collected[0] == "FOX"
    assert collected[1] == "elttob"

def test_public_driverproxy_notify():
    proxy = base_driverproxy_for_magic("notify", AnotherDummyDriver)
    # invoke notify with a special topic and option
    proxy.notify("pub_new_notify", key="val")
    assert proxy._engine.notified[-1][0] == "pub_new_notify"
    assert proxy._engine.notified[-1][1]["key"] == "val"

def test_public_driverproxy_setbusy_and_isbusy():
    proxy = base_driverproxy_for_magic("busy", AnotherDummyDriver)
    proxy.setBusy(False)
    assert proxy.isBusy() is False
    proxy.setBusy(True)
    assert proxy.isBusy() is True

def test_public_driverproxy_say():
    class SayDriver(AnotherDummyDriver):
        def __init__(self, proxy):
            super().__init__(proxy)
            self.said_items = []
        def say(self, text, name):
            self.said_items.append((text, name))
    proxy = base_driverproxy_for_magic("say", SayDriver)
    proxy.say("Hi from public!", "pTestName")
    found = any(
        q[0].__self__ is proxy._driver and q[1][0] == "Hi from public!" and q[2] == "pTestName"
        for q in proxy._queue
    )
    assert found

def test_public_driverproxy_stop():
    # Do not assert on _queue (stop may not queue in pyttsx3), check stopped flag instead
    class StopDriver(AnotherDummyDriver):
        def __init__(self, proxy):
            super().__init__(proxy)
            self.times_stopped = 0
        def stop(self):
            self.times_stopped += 1
    proxy = base_driverproxy_for_magic("stop", StopDriver)
    proxy._driver.times_stopped = 0
    proxy.stop()
    # If proxy.stop() queues, the actual driver.stop won't be called until the queue is processed,
    # so let's drain the queue and execute the function if it matches stop
    while proxy._queue:
        func, args, name = proxy._queue.pop(0)
        if hasattr(func, '__self__') and isinstance(func.__self__, StopDriver) and func.__name__ == 'stop':
            func()
    assert proxy._driver.times_stopped == 1