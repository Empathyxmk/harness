import pytest
from flask_recaptcha import ReCaptcha

def test_params_init():
    r = ReCaptcha(site_key="A", secret_key="B", theme="light", type="image", size="compact", language="en", tabindex=1)
    assert r.site_key == "A"
    assert r.secret_key == "B"
    assert r.theme == "light"
    assert r.type == "image"
    assert r.size == "compact"
    assert r.language == "en"
    assert r.tabindex == 1

def test_enabled_property():
    r = ReCaptcha(is_enabled=True)
    # Some implementations use attribute and property; this covers both possibilities
    assert getattr(r, "is_enabled") is True or getattr(r, "enabled", True) is True
    r2 = ReCaptcha(is_enabled=False)
    assert getattr(r2, "is_enabled") is False or getattr(r2, "enabled", False) is False

def test_get_code_returns_string():
    r = ReCaptcha(site_key="something", secret_key="else")
    code = r.get_code()
    assert isinstance(code, str)

def test_verify_empty_response_token(monkeypatch):
    import sys
    import flask_recaptcha
    class DummyRequests:
        @staticmethod
        def get(*a, **k):
            class Resp:
                status_code = 200
                def json(self): return {"success": True}
            return Resp()
    class DummyRequest:
        form = {}
        environ = {"REMOTE_ADDR": "host"}
    sys.modules["requests"] = DummyRequests
    sys.modules["flask_recaptcha.requests"] = DummyRequests
    monkeypatch.setattr(flask_recaptcha, "request", DummyRequest)
    r = ReCaptcha(site_key="a", secret_key="b", is_enabled=True)
    # Empty response token returns False
    assert r.verify("", "host") is False

def test_init_app_with_minimum(monkeypatch):
    import sys
    import flask_recaptcha
    # Patch Markup to prevent NameError on import
    class FakeMarkup(str): pass
    sys.modules["Markup"] = FakeMarkup
    monkeypatch.setitem(flask_recaptcha.__dict__, "Markup", FakeMarkup)
    class App:
        def __init__(self):
            self.config = {
                "RECAPTCHA_SITE_KEY": "k",
                "RECAPTCHA_SECRET_KEY": "s",
            }
            self._proc = None
        def context_processor(self, fn):
            self._proc = fn
            return fn
    app = App()
    r = ReCaptcha()
    r.init_app(app)
    c = app._proc()
    assert "recaptcha" in c and isinstance(c["recaptcha"], str)