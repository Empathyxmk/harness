import types
import pytest

import tests.utils as utils

class DummyContainer:
    def __init__(self, logs_bytes=b"publiclog", raise_on_top=False, raise_on_exec_run=False):
        self._top = {"Processes": [["1","2","3","4","5","6","7", "gunicorn -b :8080 -w 2 pubapp:app"]]}
        self._exec_run_out = types.SimpleNamespace(output=b'{"publickey": "publicvalue"}')
        self._logs_bytes = logs_bytes
        self._raise_on_top = raise_on_top
        self._raise_on_exec_run = raise_on_exec_run
        self._stop_called = False
        self._remove_called = False

    def top(self):
        if self._raise_on_top:
            raise RuntimeError("Dummy top error")
        return self._top

    def exec_run(self, cmd):
        if self._raise_on_exec_run:
            raise RuntimeError("Dummy exec_run error")
        return self._exec_run_out

    def logs(self):
        return self._logs_bytes

    def stop(self):
        self._stop_called = True

    def remove(self):
        self._remove_called = True

def test_wait_for_gunicorn_found():
    c = DummyContainer()
    result = utils.wait_for_gunicorn(c, sleep_time=0.01, timeout=0.06)
    assert result is True

def test_wait_for_gunicorn_absent():
    c = DummyContainer()
    c._top = {"Processes": [["python worker.py"]]}
    result = utils.wait_for_gunicorn(c, sleep_time=0.01, timeout=0.03)
    assert result is False

def test_get_config_from_container_ok():
    c = DummyContainer()
    r = utils.get_config_from_container(c, "/myconf.json")
    assert "publickey" in r

def test_get_config_from_container_exec_run_fails():
    c = DummyContainer(raise_on_exec_run=True)
    r = utils.get_config_from_container(c, "/notarealpath")
    assert r is None

def test_print_container_logs_output(capsys):
    c = DummyContainer()
    utils.print_container_logs(c)
    captured = capsys.readouterr()
    assert "Container logs:" in captured.out

def test_cleanup_container_stops_and_removes():
    c = DummyContainer()
    utils.cleanup_container(c)
    assert c._stop_called
    assert c._remove_called