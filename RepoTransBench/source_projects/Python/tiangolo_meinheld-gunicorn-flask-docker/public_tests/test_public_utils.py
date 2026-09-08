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
            _top = {"Processes": [["z","y","x","w","v","u","t","python manage.py"]]}
        else:
            _top = top or {"Processes": [["1","2","3","4","5","6","7", "gunicorn -w 3 -b :5000 anotherapp:app"]]}
        self._top = _top
        self._exec_run_out = exec_run_out or types.SimpleNamespace(output=b'{"bar": 43}')
        self._logs_bytes = logs_bytes or b"Different logs"
        self._stop_called = False
        self._remove_called = False
        self._raise_on_top = raise_on_top
        self._raise_on_exec_run = raise_on_exec_run

    def top(self):
        if self._raise_on_top:
            raise Exception("Top method failed for container")
        return self._top

    def exec_run(self, cmd):
        if self._raise_on_exec_run:
            raise Exception("exec_run simulated failure")
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
                from docker.errors import NotFound as NF
                raise NF("container not present")
            return self._container

    def __init__(self, container=None, notfound=False):
        self.containers = self.Containers(container=container, notfound=notfound)


def test_get_process_names():
    c = DummyContainer()
    res = utils.get_process_names(c)
    assert isinstance(res, list)
    assert "gunicorn -w 3 -b :5000 anotherapp:app" in res

def test_get_process_names_empty():
    c = DummyContainer(has_gunicorn=False)
    res = utils.get_process_names(c)
    assert isinstance(res, list)
    assert res == []

def test_get_gunicorn_conf_path():
    top = {"Processes": [["1","2","3","4","5","6","7", "gunicorn -c custom_conf.py anotherapp:app"]]}
    c = DummyContainer(top=top)
    path = utils.get_gunicorn_conf_path(c)
    assert path == "custom_conf.py"

def test_get_gunicorn_conf_path_no_gunicorn():
    c = DummyContainer(has_gunicorn=False)
    with pytest.raises(IndexError):
        utils.get_gunicorn_conf_path(c)

def test_get_config():
    dummy_out = types.SimpleNamespace(output=b'{"baz":99}')
    c = DummyContainer(exec_run_out=dummy_out)
    config = utils.get_config(c)
    assert config["baz"] == 99

def test_get_config_exec_run_error():
    c = DummyContainer(raise_on_exec_run=True)
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
    res = utils.remove_previous_container(client)
    assert res is None

def test_get_logs():
    c = DummyContainer(logs_bytes=b"xyz789")
    logs = utils.get_logs(c)
    assert logs == "xyz789"

def test_get_response_text1(monkeypatch):
    monkeypatch.setenv("PYTHON_VERSION", "3.10")
    msg = utils.get_response_text1()
    assert "3.10" in msg

def test_get_logs_utf8_error(monkeypatch):
    class Container:
        def logs(self):
            return b"\xfe"
    c = Container()
    with pytest.raises(UnicodeDecodeError):
        utils.get_logs(c)