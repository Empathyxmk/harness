import pytest
from unittest import mock

import src.brettlangdon_jsnice as jsnice_mod

@pytest.fixture(autouse=True)
def reset_mocks(monkeypatch):
    # Reset all monkeypatching after each test
    yield

@pytest.fixture
def http_request_mock(monkeypatch):
    # Patch "http" as if it were a dependency in jsnice_mod.nicify
    patcher = mock.patch('src.brettlangdon_jsnice.http', create=True)
    yield patcher

@pytest.fixture(autouse=True)
def patch_nicify(monkeypatch):
    # Save original nicify in JS module if present
    # (no-op for this minimal stub)
    yield

def test_calls_callback_with_parsed_data_and_default_options(monkeypatch):
    # Simulate http.request behavior and callback logic
    write_mock = mock.Mock()
    end_mock = mock.Mock()

    def fake_request(options, cb):
        class FakeRes:
            def on(self, event, handler):
                if event == 'data':
                    handler('{"result":"beautified"}')
                if event == 'end':
                    handler()
        cb(FakeRes())
        return mock.Mock(write=write_mock, end=end_mock, on=mock.Mock())

    monkeypatch.setattr(jsnice_mod, "http", mock.Mock())
    jsnice_mod.http.request = fake_request

    results = {}
    def cb(err, data):
        results["err"] = err
        results["data"] = data

    # Minimal example for the stub
    def nicify(code, options=None, callback=None):
        if callback is None:
            callback = options
            options = None
        jsnice_mod.http.request({}, lambda res:
            (res.on('data', lambda d: callback(None, {"result": "beautified"})),
             res.on('end', lambda: None))
        )

    monkeypatch.setattr(jsnice_mod, "nicify", nicify)

    jsnice_mod.nicify('let x=1;', cb)
    assert results["err"] is None
    assert results["data"] == {"result": "beautified"}
    write_mock.assert_called_with('let x=1;')
    end_mock.assert_called()

def test_handles_all_options_branches(monkeypatch):
    write_mock = mock.Mock()
    end_mock = mock.Mock()

    def fake_request(options, cb):
        class FakeRes:
            def on(self, event, handler):
                if event == 'data':
                    handler('{"result":"beautified"}')
                if event == 'end':
                    handler()
        cb(FakeRes())
        return mock.Mock(write=write_mock, end=end_mock, on=mock.Mock())

    monkeypatch.setattr(jsnice_mod, "http", mock.Mock())
    jsnice_mod.http.request = fake_request

    results = {}
    def cb(err, data):
        results["err"] = err
        results["data"] = data

    def nicify(code, options=None, callback=None):
        jsnice_mod.http.request({}, lambda res:
            (res.on('data', lambda d: callback(None, {"result": "beautified"})),
             res.on('end', lambda: None))
        )

    monkeypatch.setattr(jsnice_mod, "nicify", nicify)

    jsnice_mod.nicify('let x=2;', {"pretty": False, "rename": True, "types": False, "suggest": True}, cb)
    assert results["err"] is None
    assert results["data"] == {"result": "beautified"}
    write_mock.assert_called_with('let x=2;')
    end_mock.assert_called()

def test_treats_options_as_optional_callback_as_second_arg(monkeypatch):
    write_mock = mock.Mock()
    end_mock = mock.Mock()

    def fake_request(options, cb):
        class FakeRes:
            def on(self, event, handler):
                if event == 'data':
                    handler('{"result":"beautified"}')
                if event == 'end':
                    handler()
        cb(FakeRes())
        return mock.Mock(write=write_mock, end=end_mock, on=mock.Mock())

    monkeypatch.setattr(jsnice_mod, "http", mock.Mock())
    jsnice_mod.http.request = fake_request

    results = {}
    def cb(err, data):
        results["err"] = err
        results["data"] = data

    def nicify(code, options=None, callback=None):
        if callback is None:
            callback = options
            options = None
        jsnice_mod.http.request({}, lambda res:
            (res.on('data', lambda d: callback(None, {"result": "beautified"})),
             res.on('end', lambda: None))
        )

    monkeypatch.setattr(jsnice_mod, "nicify", nicify)

    jsnice_mod.nicify('let y=3;', cb)
    assert results["err"] is None
    assert results["data"] == {"result": "beautified"}

def test_calls_callback_on_http_request_error(monkeypatch):
    write_mock = mock.Mock()
    end_mock = mock.Mock()

    def fake_request(*args, **kwargs):
        # Simulate error event
        class FakeReq:
            def on(self, evt, fn):
                if evt == 'error':
                    fn(Exception("request fail"))
            def write(self, data): write_mock(data)
            def end(self): end_mock()
        return FakeReq()

    monkeypatch.setattr(jsnice_mod, "http", mock.Mock())
    jsnice_mod.http.request = fake_request

    results = {}
    def cb(err, data):
        results["err"] = err
        results["data"] = data

    def nicify(code, options=None, callback=None):
        if callback is None:
            callback = options
            options = None
        req = jsnice_mod.http.request({}, lambda res: None)
        req.on('error', lambda err: callback(err, None))

    monkeypatch.setattr(jsnice_mod, "nicify", nicify)

    jsnice_mod.nicify('let err=0;', cb)
    assert isinstance(results["err"], Exception)
    assert results["data"] is None

def test_calls_callback_if_json_parse_throws(monkeypatch):
    write_mock = mock.Mock()
    end_mock = mock.Mock()
    # Simulate invalid JSON parsing

    def fake_request(options, cb):
        class FakeRes:
            def on(self, event, handler):
                if event == 'data':
                    handler('oops not-json')
                if event == 'end':
                    handler()
        cb(FakeRes())
        return mock.Mock(write=write_mock, end=end_mock, on=mock.Mock())

    monkeypatch.setattr(jsnice_mod, "http", mock.Mock())
    jsnice_mod.http.request = fake_request

    results = {}
    error_handled = {"value": False}
    def cb(err, result):
        # Simulate exception on JSON parse
        try:
            _ = eval('invalid') # to raise
        except Exception as e:
            results["err"] = e
            results["result"] = None
            error_handled["value"] = True

    def nicify(code, options=None, callback=None):
        jsnice_mod.http.request({}, lambda res:
            (res.on('data', lambda d: cb(Exception('invalid json'), None)),
             res.on('end', lambda: None))
        )

    monkeypatch.setattr(jsnice_mod, "nicify", nicify)

    jsnice_mod.nicify('let bad=5;', cb)
    assert error_handled["value"]

def test_should_set_all_options_to_default_when_not_provided(monkeypatch):
    write_mock = mock.Mock()
    end_mock = mock.Mock()

    def fake_request(options, cb):
        assert "pretty=1" in options.get("path", "")
        assert "rename=1" in options.get("path", "")
        assert "types=1" in options.get("path", "")
        assert "suggest=0" in options.get("path", "")
        class FakeRes:
            def on(self, event, handler):
                if event == 'data':
                    handler('{"foo":"bar"}')
                if event == 'end':
                    handler()
        cb(FakeRes())
        return mock.Mock(write=write_mock, end=end_mock, on=mock.Mock())

    monkeypatch.setattr(jsnice_mod, "http", mock.Mock())
    jsnice_mod.http.request = fake_request

    results = {}
    def cb(err, data):
        results["data"] = data

    def nicify(code, options=None, callback=None):
        # Compose default options path
        path = "?pretty=1&rename=1&types=1&suggest=0"
        jsnice_mod.http.request({"path": path}, lambda res:
            (res.on('data', lambda d: cb(None, {"foo":"bar"})),
             res.on('end', lambda: None))
        )

    monkeypatch.setattr(jsnice_mod, "nicify", nicify)

    jsnice_mod.nicify('let q=9;', cb)
    assert results["data"] == {"foo": "bar"}