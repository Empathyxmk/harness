import pytest
import sys
from maestro import lifecycle, exceptions

def test_base_lifecycle_helper():
    helper = lifecycle.BaseLifecycleHelper()
    with pytest.raises(NotImplementedError):
        helper.test(None)

def test_retrying_lifecycle_helper_success(monkeypatch):
    class Dummy(lifecycle.RetryingLifecycleHelper):
        callcount = 0
        def _test(self, container=None):
            Dummy.callcount += 1
            return Dummy.callcount > 2
    d = Dummy(attempts=3)
    assert d.test(None) is True

def test_retrying_lifecycle_helper_fail(monkeypatch):
    class Dummy(lifecycle.RetryingLifecycleHelper):
        def _test(self, container=None):
            return False
    d = Dummy(attempts=2, delay=0)
    assert d.test(None) is False

def test_tcp_port_pinger_repr(monkeypatch):
    t = lifecycle.TCPPortPinger("host", 1234, 2)
    repr_str = repr(t)
    assert "PortPing" in repr_str

def test_tcp_port_pinger_test(monkeypatch):
    t = lifecycle.TCPPortPinger("localhost", 9, 1)
    assert t._test() in [True, False]  # Should not raise

def test_tcp_port_pinger_from_config_success(monkeypatch):
    class DummyShip:
        ip = '127.0.0.1'
    class DummyContainer:
        ship = DummyShip()
        name = 'c'
        ports = {'80': {'external': [None, '1234/tcp']}}
    conf = {'port': '80', 'max_wait': 2}
    t = lifecycle.TCPPortPinger.from_config(DummyContainer(), conf)
    assert isinstance(t, lifecycle.TCPPortPinger)

def test_tcp_port_pinger_from_config_no_port(monkeypatch):
    class DummyContainer:
        ports = {}
        name = "foo"
    conf = {'port': '5432'}
    with pytest.raises(exceptions.InvalidLifecycleCheckConfigurationException):
        lifecycle.TCPPortPinger.from_config(DummyContainer(), conf)

def test_tcp_port_pinger_from_config_udp(monkeypatch):
    class DummyShip:
        ip = '0.0.0.0'
    class DummyContainer:
        ship = DummyShip()
        name = 'x'
        ports = {'80': {'external': [None, '9999/udp']}}
    conf = {'port': '80'}
    with pytest.raises(exceptions.InvalidLifecycleCheckConfigurationException):
        lifecycle.TCPPortPinger.from_config(DummyContainer(), conf)

def test_script_executor_envfrom(monkeypatch):
    import subprocess
    class DummySubprocess:
        calls = []
        @staticmethod
        def call(cmd, env=None):
            DummySubprocess.calls.append(cmd)
            return 0
        @staticmethod
        def Popen(cmd, stdin=None):
            class DummyP:
                def communicate(self, data): return (None, None)
                def wait(self): return 0
            return DummyP()
    monkeypatch.setattr(subprocess, 'call', DummySubprocess.call)
    monkeypatch.setattr(subprocess, 'Popen', DummySubprocess.Popen)
    s = lifecycle.ScriptExecutor(command="echo test", env={'A': '1'}, attempts=1, envfrom='env')
    assert s._test() is True
    s2 = lifecycle.ScriptExecutor(command="echo test", env={'A': '1'}, attempts=1, envfrom='stdin')
    assert s2._test() is True

def test_script_executor_envfrom_invalid():
    s = lifecycle.ScriptExecutor(command="ls", env={}, attempts=1, envfrom='bad')
    with pytest.raises(ValueError):
        s._test()

def test_script_executor_from_config():
    class DummyContainer:
        env = {'FOO':'bar'}
    conf = {'command': "ls", 'attempts': 1}
    s = lifecycle.ScriptExecutor.from_config(DummyContainer(), conf)
    assert isinstance(s, lifecycle.ScriptExecutor)