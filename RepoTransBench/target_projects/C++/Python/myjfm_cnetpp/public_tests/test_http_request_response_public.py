import pytest

class HttpRequest:
    def __init__(self):
        self._method = ""
        self._path = ""
        self._query = ""
        self._version = ""

    def set_method(self, val):
        self._method = val

    def set_path(self, val):
        self._path = val

    def set_query(self, val):
        self._query = val

    def set_version(self, val):
        self._version = val

    def method(self):
        return self._method

    def path(self):
        return self._path

    def query(self):
        return self._query

    def version(self):
        return self._version

class HttpResponse:
    def __init__(self):
        self._status_code = 0
        self._reason_phrase = ""

    def set_status_code(self, code):
        self._status_code = code

    def set_reason_phrase(self, reason):
        self._reason_phrase = reason

    def status_code(self):
        return self._status_code

    def reason_phrase(self):
        return self._reason_phrase

def test_method_path_query_version():
    req = HttpRequest()
    req.set_method("PUT")
    req.set_path("/public/test")
    req.set_query("a=5&b=7")
    req.set_version("HTTP/1.0")
    assert req.method() == "PUT"
    assert req.path() == "/public/test"
    assert req.query() == "a=5&b=7"
    assert req.version() == "HTTP/1.0"

def test_status_code_and_reason():
    resp = HttpResponse()
    resp.set_status_code(404)
    resp.set_reason_phrase("Not Found Public")
    assert resp.status_code() == 404
    assert resp.reason_phrase() == "Not Found Public"