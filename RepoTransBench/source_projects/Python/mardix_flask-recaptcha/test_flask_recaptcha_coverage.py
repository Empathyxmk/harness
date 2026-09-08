import pytest
from flask_recaptcha import ReCaptcha, DEFAULTS

class DummyApp:
    def __init__(self):
        self.config = {
            "RECAPTCHA_SITE_KEY": "site",
            "RECAPTCHA_SECRET_KEY": "secret",
            "RECAPTCHA_ENABLED": True,
            "RECAPTCHA_THEME": "dark",
            "RECAPTCHA_TYPE": "audio",
            "RECAPTCHA_SIZE": "compact",
            "RECAPTCHA_LANGUAGE": "fr",
            "RECAPTCHA_TABINDEX": 3
        }
        self._proc = None

    def context_processor(self, func):
        self._proc = func
        return func

@pytest.mark.parametrize("enabled", [True, False])
def test_get_code_various(enabled):
    r = ReCaptcha(site_key="k", secret_key="s", is_enabled=enabled)
    code = r.get_code()
    if enabled:
        assert "<script" in code
        assert str(r.site_key) in code
    else:
        assert code == ""

def test_init_app_code_registration(monkeypatch):
    import sys
    import flask_recaptcha
    class FakeMarkup(str): pass
    sys.modules["Markup"] = FakeMarkup
    monkeypatch.setitem(flask_recaptcha.__dict__, "Markup", FakeMarkup)
    app = DummyApp()
    r = ReCaptcha()
    r.init_app(app)
    cdict = app._proc()
    assert "recaptcha" in cdict
    mark = cdict["recaptcha"]
    assert "g-recaptcha" in mark

@pytest.mark.parametrize("prop,external", [
    ("THEME", DEFAULTS.THEME),
    ("TYPE", DEFAULTS.TYPE),
    ("SIZE", DEFAULTS.SIZE),
    ("LANGUAGE", DEFAULTS.LANGUAGE),
    ("TABINDEX", DEFAULTS.TABINDEX)
])
def test_defaults_class_properties(prop, external):
    assert hasattr(DEFAULTS, prop)
    v = getattr(DEFAULTS, prop)
    assert v == external

def test_repr_and_str_do_not_error():
    r = ReCaptcha(site_key="x", secret_key="y")
    result_repr = repr(r)
    result_str = str(r)
    assert isinstance(result_repr, str)
    assert isinstance(result_str, str)

def test_init_with_app_only():
    app = DummyApp()
    r = ReCaptcha(app=app)
    assert r.site_key == "site"
    assert r.secret_key == "secret"
    assert r.theme == "dark"
    assert r.type == "audio"
    assert r.size == "compact"
    assert r.language == "fr"
    assert r.tabindex == 3

def test_verify_returns_true_if_disabled(monkeypatch):
    import sys
    import flask_recaptcha
    r = ReCaptcha(site_key="test", secret_key="test", is_enabled=False)
    class DummyRequests:
        @staticmethod
        def get(*a, **kw): raise Exception("should not be called")
    sys.modules["requests"] = DummyRequests
    sys.modules["flask_recaptcha.requests"] = DummyRequests
    result = r.verify("stuff", "127.0.0.1")
    assert result is True

def test_verify_network_failure(monkeypatch):
    import sys
    import flask_recaptcha
    r = ReCaptcha(site_key="a", secret_key="b", is_enabled=True)
    class DummyRequests:
        @staticmethod
        def get(*a, **k):
            class R: status_code=500
            def json(self): return {"success": False}
            return R()
    class DummyRequest:
        form = {"g-recaptcha-response": "bla"}
        environ = {"REMOTE_ADDR": "ip"}
    sys.modules["requests"] = DummyRequests
    sys.modules["flask_recaptcha.requests"] = DummyRequests
    monkeypatch.setattr(flask_recaptcha, "request", DummyRequest)
    result = r.verify("bla", "ip")
    assert result is False