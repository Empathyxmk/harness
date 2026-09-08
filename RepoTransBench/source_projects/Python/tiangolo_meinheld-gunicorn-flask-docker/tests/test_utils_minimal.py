import types
import pytest

import tests.utils as utils

class DummyContainer:
    def __init__(self, logs_bytes=b"logdata", raise_on_top=False, raise_on_exec_run=False):
        self._top = {"Processes": [["a","b","c","d","e","f","g", "gunicorn -c conf.py app:app"]]}
        self._exec_run_out = types.SimpleNamespace(output=b'{"newkey": "newvalue"}')
        self._logs_bytes = logs_bytes
        self._raise_on_top = raise_on_top
        self._raise_on_exec_run = raise_on_exec_run
        self._stop_called = False
        self._remove_called = False

    def top(self):
        if self._raise_on_top:
            raise RuntimeError("Simulate top error")
        return self._top

    def exec_run(self, cmd):
        if self._raise_on_exec_run:
            raise RuntimeError("Simulate exec_run error")
        return self._exec_run_out

    def logs(self):
        return self._logs_bytes

    def stop(self):
        self._stop_called = True

    def remove(self):
        self._remove_called = True

def test_wait_for_gunicorn_gunicorn_found():
    c = DummyContainer()
    result = utils.wait_for_gunicorn(c, sleep_time=0.01, timeout=0.05)
    assert result is True

def test_wait_for_gunicorn_gunicorn_notfound():
    c = DummyContainer()
    c._top = {"Processes": [["python app.py"]]}
    result = utils.wait_for_gunicorn(c, sleep_time=0.01, timeout=0.03)
    assert result is False

def test_get_config_from_container_success():
    c = DummyContainer()
    r = utils.get_config_from_container(c, "/etc/config.json")
    assert "newkey" in r

def test_get_config_from_container_exec_run_fail():
    c = DummyContainer(raise_on_exec_run=True)
    r = utils.get_config_from_container(c, "/fakepath")
    assert r is None

def test_print_container_logs_prints(capsys):
    c = DummyContainer()
    utils.print_container_logs(c)
    captured = capsys.readouterr()
    assert "Container logs:" in captured.out

def test_cleanup_container_calls_methods():
    c = DummyContainer()
    utils.cleanup_container(c)
    assert c._stop_called
    assert c._remove_called