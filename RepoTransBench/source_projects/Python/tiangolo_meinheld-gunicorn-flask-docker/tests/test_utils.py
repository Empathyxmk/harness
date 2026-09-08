import types
import json
import os
import pytest

import tests.utils as utils


class DummyContainer:
    def __init__(
        self, 
        top=None, 
        exec_run_out=None, 
        logs_bytes=None, 
        has_gunicorn=True,
        raise_on_top=False,
        raise_on_exec_run=False
    ):
        # Simulate output for container.top()
        if not has_gunicorn:
            # No gunicorn processes in output
            _top = {"Processes": [["a","b","c","d","e","f","g","python app.py"]]}
        else:
            _top = top or {"Processes": [["a","b","c","d","e","f","g", "gunicorn -c conf.py app:app"]]}
        self._top = _top
        self._exec_run_out = exec_run_out or types.SimpleNamespace(output=b'{"key": "value"}')
        self._logs_bytes = logs_bytes or b"Some logs"
        self._stop_called = False
        self._remove_called = False
        self._raise_on_top = raise_on_top
        self._raise_on_exec_run = raise_on_exec_run

    def top(self):
        if self._raise_on_top:
            raise Exception("Cannot get top of container")
        return self._top

    def exec_run(self, cmd):
        if self._raise_on_exec_run:
            raise Exception("exec_run failed")
        return self._exec_run_out

    def logs(self):
        return self._logs_bytes

    def stop(self):
        self._stop_called = True

    def remove(self):
        self._remove_called = True


class DummyClient:
    class Containers:
        def __init__(self, container=None, notfound=False):
            self._container = container
            self._notfound = notfound

        def get(self, name):
            if self._notfound:
                # Simulate NotFound
                from docker.errors import NotFound as NF
                raise NF("not found")
            return self._container

    def __init__(self, container=None, notfound=False):
        self.containers = self.Containers(container=container, notfound=notfound)


def test_get_process_names():
    c = DummyContainer()
    res = utils.get_process_names(c)
    assert isinstance(res, list)
    assert "gunicorn -c conf.py app:app" in res

def test_get_process_names_empty():
    # No gunicorn processes
    c = DummyContainer(has_gunicorn=False)
    res = utils.get_process_names(c)
    assert isinstance(res, list)
    assert res == []

def test_get_gunicorn_conf_path():
    c = DummyContainer()
    path = utils.get_gunicorn_conf_path(c)
    assert path == "conf.py"

def test_get_gunicorn_conf_path_no_gunicorn():
    c = DummyContainer(has_gunicorn=False)
    with pytest.raises(IndexError):
        utils.get_gunicorn_conf_path(c)

def test_get_config():
    dummy_out = types.SimpleNamespace(output=b'{"foo":42}')
    c = DummyContainer(exec_run_out=dummy_out)
    config = utils.get_config(c)
    assert config["foo"] == 42

def test_get_config_exec_run_error():
    c = DummyContainer(raise_on_exec_run=True)
    # Should raise due to exec_run error
    with pytest.raises(Exception):
        utils.get_config(c)

def test_remove_previous_container_found():
    c = DummyContainer()
    client = DummyClient(container=c, notfound=False)
    utils.remove_previous_container(client)
    assert c._stop_called
    assert c._remove_called

def test_remove_previous_container_notfound():
    client = DummyClient(notfound=True)
    # Should not raise exception
    res = utils.remove_previous_container(client)
    assert res is None

def test_get_logs():
    c = DummyContainer(logs_bytes=b"abc123")
    logs = utils.get_logs(c)
    assert logs == "abc123"

def test_get_response_text1(monkeypatch):
    monkeypatch.setenv("PYTHON_VERSION", "3.9")
    msg = utils.get_response_text1()
    assert "3.9" in msg

def test_get_logs_utf8_error(monkeypatch):
    class Container:
        def logs(self):
            return b"\xff"
    c = Container()
    with pytest.raises(UnicodeDecodeError):
        # Will raise because b"\xff" is not valid utf-8
        utils.get_logs(c)