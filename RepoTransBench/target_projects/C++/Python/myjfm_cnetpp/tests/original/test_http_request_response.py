import pytest

# Mocks for cnetpp.http module
class HttpRequest:
    class MethodType:
        kGet = "GET"
        kPost = "POST"
        kHead = "HEAD"
        kUnknown = "UNKNOWN"

    class Version:
        kVersion11 = "HTTP/1.1"
        kVersion10 = "HTTP/1.0"

    class ErrorType:
        kOk = "OK"
        kStartLineNotComplete = "START_LINE_NOT_COMPLETE"
        kMethodNotFound = "METHOD_NOT_FOUND"
        kVersionUnsupported = "VERSION_UNSUPPORTED"

    _byname = {"GET": MethodType.kGet, "POST": MethodType.kPost, "HEAD": MethodType.kHead}
    _names = {MethodType.kGet: "GET", MethodType.kPost: "POST", MethodType.kHead: "HEAD", MethodType.kUnknown: None}

    def __init__(self):
        self._method = self.MethodType.kUnknown
        self._uri = "/"
        self._version = self.Version.kVersion11
        self._path = "/"
        self._query = ""

    @staticmethod
    def GetMethodName(method):
        return HttpRequest._names.get(method, None)

    @staticmethod
    def GetMethodByName(name):
        return HttpRequest._byname.get(name, HttpRequest.MethodType.kUnknown)

    def set_method(self, method):
        self._method = method

    def method(self):
        return self._method

    def set_uri(self, uri):
        self._uri = uri

    def uri(self):
        return self._uri

    def Reset(self):
        self._method = self.MethodType.kUnknown
        self._uri = "/"

    def ParseStartLine(self, line, error_ptr=None):
        tokens = line.strip().split()
        error = None
        if len(tokens) == 0:
            if error_ptr is not None:
                error_ptr[0] = self.ErrorType.kStartLineNotComplete
            return False
        if len(tokens) == 1:
            if error_ptr is not None:
                error_ptr[0] = self.ErrorType.kStartLineNotComplete
            return False
        if len(tokens) == 2:
            method = tokens[0]
            uri = tokens[1]
            if method not in self._byname:
                if error_ptr is not None:
                    error_ptr[0] = self.ErrorType.kMethodNotFound
                return False
            self._method = self._byname[method]
            self._uri = uri
            if error_ptr is not None:
                error_ptr[0] = self.ErrorType.kOk
            return True
        elif len(tokens) == 3:
            method, uri, version = tokens
            if method not in self._byname:
                if error_ptr is not None:
                    error_ptr[0] = self.ErrorType.kMethodNotFound
                return False
            if version not in (self.Version.kVersion10, self.Version.kVersion11):
                if error_ptr is not None:
                    error_ptr[0] = self.ErrorType.kVersionUnsupported
                return False
            self._method = self._byname[method]
            self._uri = uri
            if error_ptr is not None:
                error_ptr[0] = self.ErrorType.kOk
            return True
        else:
            return False

    def set_http_version(self, version):
        self._version = version

    def AppendStartLineToString(self, out):
        s = "{} {} {}".format(self._method, self._uri, self._version)
        out += s
        return out

class HttpResponse:
    class StatusCode:
        kOk = 200
        kNotFound = 404
        kUnknown = 0

    _codes = {
        StatusCode.kOk: "OK",
        StatusCode.kNotFound: "Not Found",
        StatusCode.kUnknown: "Unknown Status"
    }

    @staticmethod
    def GetReasonPhrase(code):
        return HttpResponse._codes.get(code, "Unknown Status")

def test_GetMethodNameAndByName():
    assert HttpRequest.GetMethodName(HttpRequest.MethodType.kGet) == "GET"
    assert HttpRequest.GetMethodName(HttpRequest.MethodType.kPost) == "POST"
    assert HttpRequest.GetMethodName(HttpRequest.MethodType.kUnknown) is None
    assert HttpRequest.GetMethodByName("GET") == HttpRequest.MethodType.kGet
    assert HttpRequest.GetMethodByName("POST") == HttpRequest.MethodType.kPost
    assert HttpRequest.GetMethodByName("UNKNOWN") == HttpRequest.MethodType.kUnknown
    assert HttpRequest.GetMethodByName("get") == HttpRequest.MethodType.kUnknown

def test_Reset():
    req = HttpRequest()
    req.set_method(HttpRequest.MethodType.kPost)
    req.set_uri("/abc")
    req.Reset()
    assert req.method() == HttpRequest.MethodType.kUnknown
    assert req.uri() == "/"

def test_ParseStartLineSuccessAndFailure():
    req = HttpRequest()
    error = [None]

    line = "GET / HTTP/1.1"
    assert req.ParseStartLine(line, error)
    assert req.method() == HttpRequest.MethodType.kGet
    assert req.uri() == "/"
    assert error[0] == HttpRequest.ErrorType.kOk

    line = "POST /abc"
    assert req.ParseStartLine(line, None)
    assert req.method() == HttpRequest.MethodType.kPost
    assert req.uri() == "/abc"

    line = "SOMETHING"
    assert not req.ParseStartLine(line, error)
    assert error[0] == HttpRequest.ErrorType.kStartLineNotComplete

    line = "WHATEVER / HTTP/1.1"
    assert not req.ParseStartLine(line, error)
    assert error[0] == HttpRequest.ErrorType.kMethodNotFound

    line = "GET / HTTP/9.9"
    assert not req.ParseStartLine(line, error)
    assert error[0] == HttpRequest.ErrorType.kVersionUnsupported

    line = "HEAD / HTTP/1.0"
    assert req.ParseStartLine(line, error)
    assert req.method() == HttpRequest.MethodType.kHead

    assert req.ParseStartLine("GET / HTTP/1.1", None)

def test_AppendStartLineToString():
    req = HttpRequest()
    req.set_method(HttpRequest.MethodType.kGet)
    req.set_uri("/xyz")
    req.set_http_version(HttpRequest.Version.kVersion11)
    out = ""
    out = req.AppendStartLineToString(out)
    assert "GET" in out
    assert "/xyz" in out
    assert "HTTP/1.1" in out

def test_StatusReasonPhrase():
    assert HttpResponse.GetReasonPhrase(HttpResponse.StatusCode.kOk) == "OK"
    assert HttpResponse.GetReasonPhrase(HttpResponse.StatusCode.kNotFound) == "Not Found"
    assert HttpResponse.GetReasonPhrase(HttpResponse.StatusCode.kUnknown) == "Unknown Status"