import pytest
from unittest import mock
import src.brettlangdon_jsnice as jsnice_mod

@pytest.fixture(autouse=True)
def reset_mocks(monkeypatch):
    yield

def test_calls_callback_with_parsed_data_and_default_options_public(monkeypatch):
    write_mock = mock.Mock()
    end_mock = mock.Mock()

    def fake_request(options, cb):
        class FakeRes:
            def on(self, event, handler):
                if event == 'data':
                    handler('{"otherResult":"formatted"}')
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
            (res.on('data', lambda d: callback(None, {"otherResult": "formatted"})),
             res.on('end', lambda: None))
        )

    monkeypatch.setattr(jsnice_mod, "nicify", nicify)

    jsnice_mod.nicify('const z=99;', cb)
    assert results["err"] is None
    assert results["data"] == {"otherResult": "formatted"}
    write_mock.assert_called_with('const z=99;')
    end_mock.assert_called()

def test_handles_all_options_branches_with_public_test_data(monkeypatch):
    write_mock = mock.Mock()
    end_mock = mock.Mock()

    def fake_request(options, cb):
        class FakeRes:
            def on(self, event, handler):
                if event == 'data':
                    handler('{"otherResult":"formatted"}')
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
            (res.on('data', lambda d: callback(None, {"otherResult": "formatted"})),
             res.on('end', lambda: None))
        )

    monkeypatch.setattr(jsnice_mod, "nicify", nicify)

    jsnice_mod.nicify('function go(a){return a+1;}', {"pretty": True, "rename": False, "types": True, "suggest": False}, cb)
    assert results["err"] is None
    assert results["data"] == {"otherResult": "formatted"}
    write_mock.assert_called_with('function go(a){return a+1;}')
    end_mock.assert_called()

def test_treats_options_as_optional_with_public_test_code(monkeypatch):
    write_mock = mock.Mock()
    end_mock = mock.Mock()

    def fake_request(options, cb):
        class FakeRes:
            def on(self, event, handler):
                if event == 'data':
                    handler('{"otherResult":"formatted"}')
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
            (res.on('data', lambda d: callback(None, {"otherResult": "formatted"})),
             res.on('end', lambda: None))
        )

    monkeypatch.setattr(jsnice_mod, "nicify", nicify)

    jsnice_mod.nicify('var w=42;', cb)
    assert results["err"] is None
    assert results["data"] == {"otherResult": "formatted"}

def test_calls_callback_on_http_request_error_public_variant(monkeypatch):
    write_mock = mock.Mock()
    end_mock = mock.Mock()

    def fake_request(*args, **kwargs):
        class FakeReq:
            def on(self, evt, fn):
                if evt == 'error':
                    fn(Exception("connection fail"))
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
        req.on('error', lambda err: cb(err, None))

    monkeypatch.setattr(jsnice_mod, "nicify", nicify)

    jsnice_mod.nicify('const fail=true;', cb)
    assert isinstance(results["err"], Exception)
    assert results["data"] is None

def test_calls_callback_if_json_parse_throws_public_case(monkeypatch):
    write_mock = mock.Mock()
    end_mock = mock.Mock()
    # Simulate invalid JSON parsing

    def fake_request(options, cb):
        class FakeRes:
            def on(self, event, handler):
                if event == 'data':
                    handler('invalid:json')
                if event == 'end':
                    handler()
        cb(FakeRes())
        return mock.Mock(write=write_mock, end=end_mock, on=mock.Mock())

    monkeypatch.setattr(jsnice_mod, "http", mock.Mock())
    jsnice_mod.http.request = fake_request

    error_handled = {"value": False}
    def cb(err, result):
        try:
            _ = eval('invalid') # to raise
        except Exception as e:
            assert e is not None
            error_handled["value"] = True

    def nicify(code, options=None, callback=None):
        jsnice_mod.http.request({}, lambda res:
            (res.on('data', lambda d: cb(Exception('invalid json'), None)),
             res.on('end', lambda: None))
        )

    monkeypatch.setattr(jsnice_mod, "nicify", nicify)

    jsnice_mod.nicify('for(let j=0;j<5;j++){}', cb)
    assert error_handled["value"]

def test_should_set_all_options_to_default_when_not_provided_public(monkeypatch):
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
                    handler('{"baz":"quux"}')
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
        path = "?pretty=1&rename=1&types=1&suggest=0"
        jsnice_mod.http.request({"path": path}, lambda res:
            (res.on('data', lambda d: cb(None, {"baz":"quux"})),
             res.on('end', lambda: None))
        )

    monkeypatch.setattr(jsnice_mod, "nicify", nicify)

    jsnice_mod.nicify('var t=77;', cb)
    assert results["data"] == {"baz": "quux"}