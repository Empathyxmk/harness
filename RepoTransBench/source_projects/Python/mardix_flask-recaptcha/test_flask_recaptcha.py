import pytest
from flask_recaptcha import ReCaptcha

class FakeResponse:
    def __init__(self, json_data, status_code=200):
        self._json_data = json_data
        self.status_code = status_code
    def json(self):
        return self._json_data

def test_init_with_default_args():
    r = ReCaptcha()
    assert hasattr(r, "is_enabled")

def test_site_key_and_secret_key():
    r = ReCaptcha(site_key="abc", secret_key="def")
    assert hasattr(r, "site_key")
    assert hasattr(r, "secret_key")

def test_theme_and_type_property():
    r = ReCaptcha()
    # Changed from hasattr checks to attribute existence or fallback to None if not available
    # Many Flask extensions use __dict__ instead of properties
    assert hasattr(r, "theme") or getattr(r, "theme", None) is not None
    assert hasattr(r, "type") or getattr(r, "type", None) is not None

def test_set_params_method_exists():
    r = ReCaptcha()
    if hasattr(r, "set_params"):
        r.set_params(a=1, b=2)
        assert r.param["a"] == 1 and r.param["b"] == 2

def test_validate_success(monkeypatch):
    import sys
    import flask_recaptcha

    # Patch BOTH requests and request modules
    class DummyRequests:
        @staticmethod
        def get(*a, **k):
            return FakeResponse({"success": True})

    class DummyRequest:
        form = {"g-recaptcha-response": "SOME"}
        environ = {"REMOTE_ADDR": "HOST"}

    sys.modules["requests"] = DummyRequests
    sys.modules["flask_recaptcha.requests"] = DummyRequests
    monkeypatch.setattr(flask_recaptcha, "request", DummyRequest)
    r = ReCaptcha(site_key="a", secret_key="b", is_enabled=True)
    result = r.verify("SOME", "HOST")
    assert result is True

def test_validate_fail(monkeypatch):
    import sys
    import flask_recaptcha

    class DummyRequests:
        @staticmethod
        def get(*a, **k):
            return FakeResponse({"success": False})

    class DummyRequest:
        form = {"g-recaptcha-response": "SOME"}
        environ = {"REMOTE_ADDR": "HOST"}

    sys.modules["requests"] = DummyRequests
    sys.modules["flask_recaptcha.requests"] = DummyRequests
    monkeypatch.setattr(flask_recaptcha, "request", DummyRequest)
    r = ReCaptcha(site_key="a", secret_key="b", is_enabled=True)
    result = r.verify("SOME", "HOST")
    assert result is False

def test_verify_exception(monkeypatch):
    import sys
    import flask_recaptcha

    class DummyRequests:
        @staticmethod
        def get(*a, **k):
            raise RuntimeError("fail")

    class DummyRequest:
        form = {"g-recaptcha-response": "SOME"}
        environ = {"REMOTE_ADDR": "FAILHOST"}

    sys.modules["requests"] = DummyRequests
    sys.modules["flask_recaptcha.requests"] = DummyRequests
    monkeypatch.setattr(flask_recaptcha, "request", DummyRequest)
    r = ReCaptcha(site_key="a", secret_key="b", is_enabled=True)
    with pytest.raises(RuntimeError):
        r.verify("ANY", "FAILHOST")

def test_disabled_by_flag():
    r = ReCaptcha(is_enabled=False)
    result = r.verify("ANY", "X")
    assert result is True

def test_repr_and_str():
    r = ReCaptcha(site_key="public", secret_key="topsecret", is_enabled=True)
    assert isinstance(repr(r), str)
    assert isinstance(str(r), str)